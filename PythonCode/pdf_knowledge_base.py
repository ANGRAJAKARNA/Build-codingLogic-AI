# pdf_knowledge_base.py
"""
PDF-Based Python Knowledge Base
Extracts concepts from PDF and answers questions using semantic search.
No API keys required - runs entirely locally.
"""

import os
import re
import pickle
import logging
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for optional dependencies
PDF_AVAILABLE = False
VECTOR_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    logger.warning("PyMuPDF not installed. Run: pip install pymupdf")

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    VECTOR_AVAILABLE = True
except ImportError:
    logger.warning("sentence-transformers/faiss not installed. Run: pip install sentence-transformers faiss-cpu")


class PDFKnowledgeBase:
    """
    A semantic search knowledge base built from PDF documents.
    Uses sentence-transformers for embeddings and FAISS for similarity search.
    """
    
    def __init__(self, cache_dir: str = ".knowledge_cache"):
        """
        Initialize the knowledge base.
        
        Args:
            cache_dir: Directory to store cached embeddings and index
        """
        self.cache_dir = Path(cache_dir)
        self.chunks: List[Dict] = []  # List of {"text": str, "metadata": dict}
        self.embeddings = None
        self.index = None
        self.model = None
        self._ready = False
        self._pdf_name = ""
        
        # Initialize embedding model if available
        if VECTOR_AVAILABLE:
            try:
                logger.info("Loading embedding model (all-MiniLM-L6-v2)...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                self.model = None
    
    def is_ready(self) -> bool:
        """Check if the knowledge base is ready for queries."""
        return self._ready and self.index is not None and self.model is not None
    
    def load_pdf(self, pdf_path: str, force_reload: bool = False) -> bool:
        """
        Load and index a PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            force_reload: If True, ignore cache and reprocess
            
        Returns:
            True if successful, False otherwise
        """
        if not PDF_AVAILABLE:
            logger.error("PyMuPDF not available. Cannot load PDF.")
            return False
        
        if not VECTOR_AVAILABLE:
            logger.error("sentence-transformers/faiss not available. Cannot create index.")
            return False
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return False
        
        self._pdf_name = Path(pdf_path).stem
        cache_file = self.cache_dir / f"{self._pdf_name}.pkl"
        faiss_file = self.cache_dir / f"{self._pdf_name}.faiss"
        mtime_file = self.cache_dir / f"{self._pdf_name}.mtime"
        
        # Check if PDF has been modified since cache was created
        pdf_mtime = os.path.getmtime(pdf_path)
        cache_valid = False
        
        if not force_reload and cache_file.exists() and faiss_file.exists() and mtime_file.exists():
            try:
                with open(mtime_file, 'r') as f:
                    cached_mtime = float(f.read().strip())
                cache_valid = (pdf_mtime == cached_mtime)
                if not cache_valid:
                    logger.info("PDF has been modified - rebuilding cache")
            except Exception:
                cache_valid = False
        
        # Try to load from cache if valid
        if cache_valid and self._load_cache(cache_file, faiss_file):
            logger.info(f"Loaded knowledge base from cache ({len(self.chunks)} chunks)")
            self._ready = True
            return True
        
        # Parse PDF and create index
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            # Extract text from PDF
            raw_text, metadata = self._extract_pdf_text(pdf_path)
            
            if not raw_text:
                logger.error("No text extracted from PDF")
                return False
            
            logger.info(f"Extracted {len(raw_text)} characters from PDF")
            
            # Chunk the text
            self.chunks = self._chunk_text(raw_text, metadata)
            logger.info(f"Created {len(self.chunks)} chunks")
            
            if not self.chunks:
                logger.error("No chunks created from PDF")
                return False
            
            # Create embeddings
            logger.info("Creating embeddings (this may take a few minutes)...")
            texts = [chunk["text"] for chunk in self.chunks]
            self.embeddings = self.model.encode(
                texts, 
                show_progress_bar=True,
                convert_to_numpy=True
            )
            logger.info(f"Created embeddings with shape {self.embeddings.shape}")
            
            # Build FAISS index
            self._build_index()
            logger.info("FAISS index built successfully")
            
            # Save to cache with PDF modification time
            self._save_cache(cache_file, faiss_file, pdf_mtime)
            logger.info("Saved knowledge base to cache")
            
            self._ready = True
            return True
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _extract_pdf_text(self, pdf_path: str) -> Tuple[str, Dict]:
        """Extract text content from PDF with metadata."""
        doc = fitz.open(pdf_path)
        
        full_text = []
        metadata = {
            "title": doc.metadata.get("title", Path(pdf_path).stem),
            "author": doc.metadata.get("author", "Unknown"),
            "pages": len(doc),
            "chapters": []
        }
        
        current_chapter = "Introduction"
        
        for page_num, page in enumerate(doc):
            page_text = page.get_text("text")
            
            # Try to detect chapter headings
            lines = page_text.split('\n')
            for line in lines:
                line = line.strip()
                # Common chapter patterns
                if re.match(r'^(Chapter|CHAPTER)\s+\d+', line):
                    current_chapter = line
                    metadata["chapters"].append({
                        "title": line,
                        "page": page_num + 1
                    })
                elif re.match(r'^\d+\.\s+[A-Z]', line) and len(line) < 100:
                    # Section heading like "1. Introduction"
                    current_chapter = line
            
            # Add page marker for reference
            full_text.append(f"\n[Page {page_num + 1}]\n")
            full_text.append(page_text)
        
        doc.close()
        
        return "\n".join(full_text), metadata
    
    def _chunk_text(
        self, 
        text: str, 
        metadata: Dict,
        chunk_size: int = 500,
        overlap: int = 50
    ) -> List[Dict]:
        """
        Split text into overlapping chunks while preserving context.
        
        Args:
            text: Full text to chunk
            metadata: Document metadata
            chunk_size: Target size for each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        
        # Clean the text
        text = self._clean_text(text)
        
        # Split into paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        current_page = 1
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Track page numbers
            page_match = re.search(r'\[Page (\d+)\]', para)
            if page_match:
                current_page = int(page_match.group(1))
                para = re.sub(r'\[Page \d+\]', '', para).strip()
                if not para:
                    continue
            
            # Check if this is a code block (preserve intact)
            is_code = self._is_code_block(para)
            
            if is_code:
                # Save current chunk if exists
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": {
                            "page": current_page,
                            "type": "text",
                            "source": metadata.get("title", "PDF")
                        }
                    })
                    current_chunk = ""
                
                # Add code block as its own chunk
                chunks.append({
                    "text": para,
                    "metadata": {
                        "page": current_page,
                        "type": "code",
                        "source": metadata.get("title", "PDF")
                    }
                })
            elif len(current_chunk) + len(para) < chunk_size:
                current_chunk += "\n\n" + para if current_chunk else para
            else:
                # Save current chunk
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": {
                            "page": current_page,
                            "type": "text",
                            "source": metadata.get("title", "PDF")
                        }
                    })
                
                # Start new chunk with overlap
                if overlap > 0 and current_chunk:
                    # Keep last part of previous chunk
                    overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else ""
                    current_chunk = overlap_text + "\n\n" + para
                else:
                    current_chunk = para
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {
                    "page": current_page,
                    "type": "text",
                    "source": metadata.get("title", "PDF")
                }
            })
        
        # Filter out very short chunks
        chunks = [c for c in chunks if len(c["text"]) >= 50]
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text extracted from PDF."""
        # Remove excessive whitespace
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove page headers/footers (common patterns)
        text = re.sub(r'\n\d+\s*\n', '\n', text)  # Standalone page numbers
        text = re.sub(r'Python Crash Course.*?\n', '', text)  # Book title headers
        text = re.sub(r'Chapter\s+\d+\s*\n', '', text)  # Chapter headers in middle
        
        # Fix common PDF extraction issues
        text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Hyphenated words across lines
        text = re.sub(r'(?<=[a-z])\n(?=[a-z])', ' ', text)  # Mid-sentence line breaks
        
        # Remove file references that break flow
        text = re.sub(r'\w+\.py\s+', '', text)  # Remove filename.py references
        text = re.sub(r'--snip--', '...', text)  # Replace snip markers
        
        return text.strip()
    
    def _clean_chunk_for_display(self, text: str) -> str:
        """Clean a chunk specifically for display to users."""
        # Remove chapter/page references embedded in text
        text = re.sub(r'^\d+\s+Chapter\s+\d+', '', text)
        text = re.sub(r'Chapter\s+\d+\s+\d+', '', text)
        text = re.sub(r'\s+\d{2,3}\s*$', '', text)  # Trailing page numbers
        text = re.sub(r'Classes\s+\d+', '', text)  # "Classes 167"
        text = re.sub(r'Working with.*?\d+', '', text)  # Section headers with page numbers
        
        # Fix common PDF extraction issues
        # Words that got cut: "you" -> "yo", "your" -> "yor", etc.
        text = re.sub(r'\byo\b(?!u)', 'you', text)
        text = re.sub(r'\byor\b', 'your', text)
        text = re.sub(r'\byou\s*\n\s*', 'you ', text)  # "you" split across lines
        
        # Fix other common word breaks
        text = re.sub(r'cate?gor', 'category', text)
        text = re.sub(r'modif\b', 'modify', text)
        text = re.sub(r'\bman\b(?=\s+real)', 'many', text)  # "man real" -> "many real"
        
        # Clean up code markers  
        text = re.sub(r'\s[uvwxyz]\s', ' ', text)  # Remove annotation markers (u, v, w, etc.)
        text = re.sub(r'^[uvwxyz]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+[uvwxyz]\.', '.', text)
        
        # Fix broken sentences
        text = re.sub(r'\s+\.', '.', text)
        text = re.sub(r'\s+,', ',', text)
        text = re.sub(r'\s+;', ';', text)
        
        # Remove excessive whitespace and newlines
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)
        
        return text.strip()
    
    def _is_code_block(self, text: str) -> bool:
        """Detect if text is likely a code block."""
        code_indicators = [
            r'^\s*(def |class |import |from |if |for |while |try:|except:|with )',
            r'^\s*>>>\s',  # Python REPL
            r'^\s*\$\s',   # Shell commands
            r'^\s*#\s*\w',  # Comments
            r'print\s*\(',
            r'return\s+\w',
            r'\w+\s*=\s*\[',  # List assignment
            r'\w+\s*=\s*\{',  # Dict assignment
        ]
        
        lines = text.split('\n')
        code_line_count = 0
        
        for line in lines:
            for pattern in code_indicators:
                if re.search(pattern, line):
                    code_line_count += 1
                    break
        
        # If more than 30% of lines look like code, treat as code block
        return len(lines) > 0 and (code_line_count / len(lines)) > 0.3
    
    def _build_index(self):
        """Build FAISS index from embeddings."""
        if self.embeddings is None:
            raise ValueError("No embeddings to index")
        
        dimension = self.embeddings.shape[1]
        
        # Use L2 distance (Euclidean) - works well for normalized embeddings
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        self.index.add(np.array(self.embeddings).astype('float32'))
    
    def _save_cache(self, cache_file: Path, faiss_file: Path, pdf_mtime: float = None):
        """Save chunks, embeddings, and index to disk."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Save chunks and embeddings
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'embeddings': self.embeddings,
                'pdf_name': self._pdf_name
            }, f)
        
        # Save FAISS index
        faiss.write_index(self.index, str(faiss_file))
        
        # Save PDF modification time for cache invalidation
        if pdf_mtime is not None:
            mtime_file = self.cache_dir / f"{self._pdf_name}.mtime"
            with open(mtime_file, 'w') as f:
                f.write(str(pdf_mtime))
    
    def _load_cache(self, cache_file: Path, faiss_file: Path) -> bool:
        """Load cached chunks, embeddings, and index."""
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
            
            self.chunks = data['chunks']
            self.embeddings = data['embeddings']
            self._pdf_name = data.get('pdf_name', '')
            
            self.index = faiss.read_index(str(faiss_file))
            
            return True
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
            return False
    
    def query(self, question: str, top_k: int = 3) -> List[Dict]:
        """
        Find the most relevant chunks for a question.
        
        Args:
            question: User's question
            top_k: Number of results to return
            
        Returns:
            List of dictionaries with 'text', 'score', and 'metadata'
        """
        if not self.is_ready():
            return []
        
        # Embed the question
        question_embedding = self.model.encode([question], convert_to_numpy=True)
        
        # Search the index
        distances, indices = self.index.search(
            np.array(question_embedding).astype('float32'),
            top_k
        )
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks) and idx >= 0:
                results.append({
                    'text': self.chunks[idx]['text'],
                    'score': float(distances[0][i]),
                    'metadata': self.chunks[idx]['metadata']
                })
        
        return results
    
    def answer(self, question: str, top_k: int = 5) -> str:
        """
        Generate a well-formatted, coherent answer for a question.
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve (will filter for best)
            
        Returns:
            Formatted markdown response
        """
        if not self.is_ready():
            return self._get_not_ready_message()
        
        results = self.query(question, top_k)
        
        if not results:
            return None  # Signal to use fallback
        
        # Check if results are relevant enough (lower score = more similar for L2)
        best_score = results[0]['score']
        if best_score > 1.2:  # Stricter threshold
            return None  # Signal to use fallback
        
        # Extract topic from question
        topic = self._extract_topic(question)
        
        # Separate code and text chunks
        code_chunks = []
        text_chunks = []
        seen_texts = set()
        
        for result in results:
            text = result['text'].strip()
            
            # Skip if we've seen similar content
            text_key = text[:80].lower()
            if text_key in seen_texts:
                continue
            seen_texts.add(text_key)
            
            # Clean the text for display
            cleaned = self._clean_chunk_for_display(text)
            if len(cleaned) < 30:  # Skip very short chunks
                continue
            
            is_code = result['metadata'].get('type') == 'code' or self._is_code_block(text)
            
            if is_code:
                code_chunks.append({
                    'text': self._format_code_chunk(cleaned),
                    'page': result['metadata'].get('page', 'N/A'),
                    'score': result['score']
                })
            else:
                text_chunks.append({
                    'text': cleaned,
                    'page': result['metadata'].get('page', 'N/A'),
                    'score': result['score']
                })
        
        # Build a coherent response
        response = f"## 📚 {topic.title()} in Python\n\n"
        response += "*From Python Crash Course textbook*\n\n"
        
        has_content = False
        
        # Add explanatory text (best 2 chunks)
        if text_chunks:
            good_sentences = []
            for chunk in text_chunks[:3]:
                sentences = self._extract_sentences(chunk['text'], max_sentences=3)
                if sentences and len(sentences) > 30:
                    good_sentences.append(sentences)
            
            if good_sentences:
                response += "### Explanation\n\n"
                for sentences in good_sentences[:2]:
                    response += f"{sentences}\n\n"
                has_content = True
        
        # Add code examples
        if code_chunks:
            response += "### Code Example\n\n"
            response += "```python\n"
            for chunk in code_chunks[:2]:
                code_text = chunk['text'].strip()
                # Only add if it looks like actual code
                if len(code_text) > 20 and ('def ' in code_text or 'class ' in code_text or '=' in code_text):
                    response += f"{code_text}\n"
                    has_content = True
            response += "```\n\n"
        
        # Add key points if we have enough content
        if text_chunks:
            key_points = self._extract_key_points(text_chunks[0]['text'], topic)
            if key_points:
                response += "### Key Points\n\n"
                for point in key_points:
                    response += f"- {point}\n"
                response += "\n"
                has_content = True
        
        # If we don't have good content, return None to trigger fallback
        if not has_content:
            return None
        
        # Source reference
        pages = sorted(set([c['page'] for c in (text_chunks + code_chunks)[:3] if c['page'] != 'N/A']))
        if pages:
            response += f"\n*📖 See pages: {', '.join(map(str, pages))}*"
        
        return response
    
    def _extract_topic(self, question: str) -> str:
        """Extract the main topic from a question."""
        # Remove common question words
        topic = question.lower()
        for word in ['what is', 'what are', 'how to', 'how do', 'explain', 'tell me about', 
                     'can you', 'please', 'in python', '?', 'a ', 'an ', 'the ']:
            topic = topic.replace(word, '')
        return topic.strip() or "Python"
    
    def _extract_sentences(self, text: str, max_sentences: int = 4) -> str:
        """Extract complete, meaningful sentences from text."""
        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter for complete, meaningful sentences
        good_sentences = []
        for s in sentences:
            s = s.strip()
            # Skip if too short, or starts mid-sentence, or is just a fragment
            if len(s) < 20:
                continue
            if s[0].islower() and not s.startswith('def ') and not s.startswith('class '):
                continue
            if not s[-1] in '.!?':
                continue
            # Skip sentences that are clearly code or references
            if re.match(r'^[a-z_]+\s*[=\[\(]', s):
                continue
            good_sentences.append(s)
            if len(good_sentences) >= max_sentences:
                break
        
        return ' '.join(good_sentences)
    
    def _format_code_chunk(self, text: str) -> str:
        """Clean up code chunk for display."""
        lines = text.split('\n')
        clean_lines = []
        
        for line in lines:
            # Remove annotation markers
            line = re.sub(r'^[uvwxyz]\s+', '', line)
            line = re.sub(r'\s+[uvwxyz]$', '', line)
            # Skip empty lines at start/end, but keep middle ones
            if line.strip() or clean_lines:
                clean_lines.append(line)
        
        # Remove trailing empty lines
        while clean_lines and not clean_lines[-1].strip():
            clean_lines.pop()
        
        return '\n'.join(clean_lines)
    
    def _extract_key_points(self, text: str, topic: str) -> list:
        """Extract key points about a topic from text."""
        points = []
        
        # Look for definitional phrases
        patterns = [
            rf'{topic}\s+(?:is|are)\s+([^.]+\.)',
            rf'(?:a|an|the)\s+{topic}\s+([^.]+\.)',
            r'(?:you can|allows you to|lets you)\s+([^.]+\.)',
            r'(?:this means|in other words)\s+([^.]+\.)',
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches[:2]:
                point = match.strip().capitalize()
                if len(point) > 15 and len(point) < 150:
                    points.append(point)
        
        return points[:4]  # Max 4 key points
    
    def _get_not_ready_message(self) -> str:
        """Return message when knowledge base is not ready."""
        if not PDF_AVAILABLE:
            return "PDF support not available. Install with: `pip install pymupdf`"
        if not VECTOR_AVAILABLE:
            return "Vector search not available. Install with: `pip install sentence-transformers faiss-cpu`"
        if self.model is None:
            return "Embedding model not loaded. Please restart the application."
        return "Knowledge base not initialized. Please load a PDF first."
    
    def get_stats(self) -> Dict:
        """Get statistics about the knowledge base."""
        return {
            "ready": self._ready,
            "pdf_name": self._pdf_name,
            "num_chunks": len(self.chunks),
            "embedding_dim": self.embeddings.shape[1] if self.embeddings is not None else 0,
            "index_size": self.index.ntotal if self.index is not None else 0,
            "pdf_available": PDF_AVAILABLE,
            "vector_available": VECTOR_AVAILABLE
        }


# =============================================================================
# GLOBAL INSTANCE - Singleton pattern for efficiency
# =============================================================================

_knowledge_base: Optional[PDFKnowledgeBase] = None


def get_knowledge_base() -> PDFKnowledgeBase:
    """Get or create the global knowledge base instance."""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = PDFKnowledgeBase()
    return _knowledge_base


def initialize_knowledge_base(pdf_path: str = None, force_reload: bool = False) -> bool:
    """
    Initialize the knowledge base with a PDF.
    
    Args:
        pdf_path: Path to PDF file. If None, tries default location.
        force_reload: Force reprocessing even if cache exists.
        
    Returns:
        True if successful
    """
    kb = get_knowledge_base()
    
    # Try default PDF path if not provided
    if pdf_path is None:
        default_paths = [
            "TextBooks/python-crash-course.pdf",
            "./TextBooks/python-crash-course.pdf",
            "../TextBooks/python-crash-course.pdf",
        ]
        for path in default_paths:
            if os.path.exists(path):
                pdf_path = path
                break
    
    if pdf_path and os.path.exists(pdf_path):
        return kb.load_pdf(pdf_path, force_reload)
    
    logger.warning("No PDF found to initialize knowledge base")
    return False


def query_knowledge(question: str, top_k: int = 3) -> str:
    """
    Query the knowledge base and get a formatted answer.
    
    Args:
        question: User's question
        top_k: Number of relevant chunks to retrieve
        
    Returns:
        Formatted markdown answer
    """
    kb = get_knowledge_base()
    
    if not kb.is_ready():
        # Try to initialize with default PDF
        initialize_knowledge_base()
    
    return kb.answer(question, top_k)


def is_knowledge_base_ready() -> bool:
    """Check if knowledge base is ready for queries."""
    kb = get_knowledge_base()
    return kb.is_ready()


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("PDF Knowledge Base - Test Mode")
    print("=" * 60)
    
    # Initialize
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "TextBooks/python-crash-course.pdf"
    
    print(f"\nInitializing with: {pdf_path}")
    success = initialize_knowledge_base(pdf_path)
    
    if success:
        kb = get_knowledge_base()
        stats = kb.get_stats()
        print(f"\nKnowledge Base Stats:")
        print(f"  - Chunks: {stats['num_chunks']}")
        print(f"  - Embedding dimension: {stats['embedding_dim']}")
        print(f"  - Index size: {stats['index_size']}")
        
        print("\n" + "=" * 60)
        print("Interactive Query Mode (type 'quit' to exit)")
        print("=" * 60)
        
        while True:
            question = input("\nYour question: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if question:
                print("\n" + query_knowledge(question))
    else:
        print("\nFailed to initialize knowledge base.")
        print("Make sure the PDF exists and dependencies are installed:")
        print("  pip install pymupdf sentence-transformers faiss-cpu")


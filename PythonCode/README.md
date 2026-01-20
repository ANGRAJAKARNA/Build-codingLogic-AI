# PyCode AI - Intelligent Python Learning Platform 🤖

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/AI-Powered-purple.svg" alt="AI">
</p>

An AI-powered interactive platform for learning Python programming, test automation, Linux, and networking concepts. Features practice problems, mock interviews, and an intelligent chatbot assistant.

## ✨ Features

### 🎯 Practice Mode
- **50+ Coding Challenges** across multiple difficulty levels (Easy, Medium, Hard)
- **Real-time Code Execution** with secure sandbox environment
- **Instant Feedback** with test case validation
- **Smart Hints** and solution explanations
- **Progress Tracking** with achievements and streaks

### 🎤 Interview Mode
- **Mock Technical Interviews** simulating real coding interviews
- **Multi-stage Interview Flow** (Introduction → Problem Understanding → Solution Design → Implementation → Review)
- **AI Interviewer** that adapts to your responses
- **Performance Scoring** with detailed feedback
- **Interview History** tracking

#### 🎙️ Voice Mode (NEW!)
- **Voice-enabled interviews** - Interviewer speaks questions aloud using Text-to-Speech
- **Self-introduction round** - Start with a 30-second self-introduction
- **Voice responses** - Record your answers using the microphone
- **Automatic transcription** - Speech-to-text converts your voice to text
- **Text fallback** - Type responses if voice is unavailable
- Choose between **Text Mode** or **Voice Mode** when starting an interview

### 🤖 AI Chat Assistant
Comprehensive knowledge base covering:

| Domain | Concepts |
|--------|----------|
| **Python Core** | 47 concepts (lists, dicts, classes, decorators, OOP, etc.) |
| **Advanced Python** | 15 concepts (async/await, dataclasses, pathlib, functools, etc.) |
| **Test Automation** | 46 concepts (Selenium, Robot Framework, pytest, XPath, etc.) |
| **Infrastructure** | 43 concepts (TCP/IP, DNS, HTTP, servers, storage, Nutanix) |
| **Linux** | 24 concepts (systemd, bash, permissions, networking, Docker) |

**Total: 175+ concepts** with detailed explanations, code examples, and best practices.

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/ANGRAJAKARNA/Build-codingLogic-AI.git
cd Build-codingLogic-AI/PythonCode

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Optional: Enable Groq AI
For enhanced AI responses, set up a Groq API key:
```bash
export GROQ_API_KEY="your-api-key-here"
```

### Optional: Enable Voice Mode
Voice mode requires additional system dependencies for audio processing:

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pyaudio  # Pre-built wheels usually work
```

**Verify voice features:**
```python
# Test in Python REPL
from voice_engine import get_voice_capabilities
print(get_voice_capabilities())
# Should show: {'tts_gtts': True, 'stt': True, ...}
```

**Troubleshooting Voice Mode:**
- **"Speech recognition not available"**: Install `SpeechRecognition` and `PyAudio`
- **"gTTS error"**: Check internet connection (gTTS requires network)
- **Microphone not working**: Check browser permissions and system audio settings
- **Offline mode**: Use `pyttsx3` for TTS without internet (lower quality)

## 📁 Project Structure

```
PythonCode/
├── main.py                    # Main Streamlit application
├── builtin_assistant.py       # AI chatbot with 175+ concepts
├── evaluator.py              # Secure code execution sandbox
├── interview_engine.py       # Mock interview system (text & voice)
├── voice_engine.py           # Voice features (TTS/STT) for interviews
├── persistence.py            # User progress storage
├── questions.py              # Practice problem bank
├── ai_service.py             # Groq API integration
├── advanced_concepts.py      # Modern Python 3.7+ concepts
├── infrastructure_concepts.py # Networking/Server/Storage concepts
├── linux_concepts.py         # Linux system administration
├── automation_concepts.py    # Selenium/Robot Framework
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🎨 User Interface

The platform features a modern **Futuristic Neon Cyber** design with:
- Dark theme with cyan/purple accents
- Responsive 2-panel layout
- Interactive code editor with syntax highlighting
- Real-time chat interface with typing indicators
- Collapsible sidebar with quick prompts

## 💡 Usage Examples

### Practice Mode
1. Select a difficulty level (Easy/Medium/Hard)
2. Choose a problem from the list
3. Write your solution in the code editor
4. Click "Run Code" to test against sample cases
5. Click "Submit" for full evaluation

### AI Chat Assistant
Ask questions like:
- "What is a decorator in Python?"
- "Explain async/await"
- "How does TCP work?"
- "What is systemd in Linux?"
- "Explain Selenium WebDriver"

### Interview Mode

#### Text Mode (Default)
1. Select "Interview" mode from the top menu
2. Choose difficulty and interview type
3. Select a problem and click "Start Interview"
4. Follow the AI interviewer's prompts
5. Explain your approach and implement your solution
6. Review detailed feedback and scores

#### Voice Mode (New!)
1. Select "Interview" mode and click "🎙️ Voice Mode"
2. Configure your interview settings
3. Click "🎙️ Start Voice Interview"
4. Listen to the interviewer's greeting (audio plays automatically)
5. Click "I'm Ready - Continue" when comfortable
6. Record your 30-second self-introduction (click microphone icon)
7. Continue with technical questions using voice or text
8. Review your performance feedback

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Service | Groq API (optional) |
| Code Execution | Secure Sandbox |
| Data Storage | JSON files |
| Styling | Custom CSS |
| Text-to-Speech | gTTS (online) / pyttsx3 (offline) |
| Speech-to-Text | SpeechRecognition (Google API) |
| Audio Recording | audio-recorder-streamlit |

## 📊 Concept Coverage

### Python Programming
- Data Structures (Lists, Dicts, Sets, Tuples)
- Control Flow (Loops, Conditionals)
- Functions & Decorators
- Object-Oriented Programming
- Exception Handling
- File I/O
- Async/Await
- Dataclasses
- Type Hints

### Test Automation
- Selenium WebDriver
- Robot Framework
- pytest
- Page Object Model
- XPath & CSS Selectors
- Waits & Synchronization
- Test Reporting

### Infrastructure
- TCP/IP & UDP
- DNS & HTTP/HTTPS
- Server Types & Management
- Storage (SAN, NAS, RAID)
- Nutanix HCI Platform

### Linux Administration
- System Boot Process
- systemd & Services
- File Permissions
- User Management
- Shell Scripting
- Docker/Containers
- Network Configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Naveen Kumar Yellared**
- GitHub: [@ANGRAJAKARNA](https://github.com/ANGRAJAKARNA)

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Groq for AI API services
- The Python community for inspiration

---

<p align="center">
  Made with ❤️ for learners everywhere
</p>


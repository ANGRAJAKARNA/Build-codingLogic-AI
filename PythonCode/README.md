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

## 📁 Project Structure

```
PythonCode/
├── main.py                    # Main Streamlit application
├── builtin_assistant.py       # AI chatbot with 175+ concepts
├── evaluator.py              # Secure code execution sandbox
├── interview_engine.py       # Mock interview system
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
1. Click "Start Interview"
2. Follow the AI interviewer's prompts
3. Explain your thought process
4. Implement your solution
5. Review feedback and scores

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Service | Groq API (optional) |
| Code Execution | Secure Sandbox |
| Data Storage | JSON files |
| Styling | Custom CSS |

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


# 🤖 Lumina-PDF-Bot - Complete Project

## 📋 Project Overview

Ye project **2 architectures** mein available hai:

1. **Monolithic** - Original single application
2. **Microservices** - New distributed architecture

---

## 🏗️ Architecture Options

### Option 1: Monolithic (Simple)
```
Single Streamlit App
├── All code in one place
├── Easy to understand
├── Quick to deploy
└── Good for learning
```

**Use When:**
- Learning RAG systems
- Quick prototyping
- Small projects
- Single developer

**Run:**
```bash
cd pdf_chatbot
streamlit run src/api/app.py
```

---

### Option 2: Microservices (Advanced)
```
4 Independent Services
├── Document Service (8001)
├── Vector Service (8002)
├── LLM Service (8003)
└── Frontend Service (8501)
```

**Use When:**
- Production deployment
- Team collaboration
- Need scalability
- Learning microservices

**Run:**
```bash
cd microservices
start_all.bat
```

---

## 📊 Quick Comparison

| Feature | Monolithic | Microservices |
|---------|-----------|---------------|
| **Complexity** | Low | High |
| **Setup Time** | 2 minutes | 5 minutes |
| **Scalability** | Limited | Excellent |
| **Maintenance** | Medium | Easy |
| **Learning Curve** | Easy | Medium |
| **Production Ready** | Yes | Yes |

---

## 🚀 Quick Start

### For Beginners (Monolithic)
```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
# Create .env with API keys

# 3. Run
streamlit run src/api/app.py
```

### For Advanced (Microservices)
```bash
# 1. Go to microservices
cd microservices

# 2. Install
pip install -r requirements.txt

# 3. Run all services
start_all.bat

# 4. Open browser
http://localhost:8501
```

---

## 📁 Project Structure

```
pdf_chatbot/
│
├── src/                    # Monolithic Application
│   ├── api/               # Streamlit UI
│   ├── core/              # Configuration
│   ├── engine/            # RAG Pipeline
│   ├── handlers/          # LLM Handlers
│   ├── services/          # Business Logic
│   └── utils/             # Utilities
│
├── microservices/         # Microservices Architecture
│   ├── document_service/  # PDF Processing
│   ├── vector_service/    # Embeddings & Search
│   ├── llm_service/       # AI Responses
│   ├── frontend_service/  # UI
│   ├── shared/            # Shared Config
│   ├── README.md          # Microservices Guide
│   ├── ARCHITECTURE.md    # Architecture Details
│   ├── COMPARISON.md      # Detailed Comparison
│   ├── QUICKSTART.md      # Quick Start Guide
│   ├── start_all.bat      # Start Script
│   └── docker-compose.yml # Docker Setup
│
├── data/                  # Data Storage
│   ├── pdfs/             # Uploaded Documents
│   └── vectorstore/      # Vector Embeddings
│
├── requirements.txt       # Monolithic Dependencies
└── README.md             # This File
```

---

## 🎯 Features

### Core Features (Both Architectures)
- ⚡ Lightning fast responses (Groq API)
- 📄 Multi-format support (PDF, DOCX, TXT, MD)
- 🧠 Smart context retrieval (RAG)
- 💬 Chat history management
- 🔌 Multiple LLM providers
- 📊 Document summarization

### Microservices Exclusive
- 🔄 Independent scaling
- 🐳 Docker support
- 📈 Better fault tolerance
- 🔧 Easy maintenance
- 🚀 Production ready

---

## 🛠️ Technology Stack

### Monolithic
```
Frontend: Streamlit
Backend: Python
RAG: LangChain
Embeddings: TF-IDF / HuggingFace
LLM: Groq / OpenAI / OpenRouter
Storage: Local Files
```

### Microservices
```
Frontend: Streamlit (8501)
Services: FastAPI (8001, 8002, 8003)
Communication: HTTP REST
Embeddings: TF-IDF (Scikit-learn)
LLM: Groq / OpenAI / OpenRouter
Deployment: Docker / Kubernetes
```

---

## 📚 Documentation

### Monolithic
- Main README: `README.md` (this file)
- Code Documentation: In-code comments

### Microservices
- Quick Start: `microservices/QUICKSTART.md`
- Architecture: `microservices/ARCHITECTURE.md`
- Comparison: `microservices/COMPARISON.md`
- Full Guide: `microservices/README.md`

---

## 🎓 Learning Path

### Beginner Path
```
1. Start with Monolithic
2. Understand RAG concepts
3. Learn how components work
4. Experiment with features
```

### Advanced Path
```
1. Study Monolithic code
2. Move to Microservices
3. Understand service communication
4. Learn Docker & deployment
5. Scale individual services
```

---

## 🔧 Configuration

Create `.env` file in root:

```env
# LLM Provider (groq, openai, openrouter)
LLM_PROVIDER=groq

# API Keys
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Model Selection
LLM_MODEL=llama-3.1-8b-instant

# Microservices URLs (for microservices only)
DOCUMENT_SERVICE_URL=http://localhost:8001
VECTOR_SERVICE_URL=http://localhost:8002
LLM_SERVICE_URL=http://localhost:8003
```

---

## 🚀 Deployment

### Monolithic Deployment
```bash
# Local
streamlit run src/api/app.py

# Cloud (Streamlit Cloud)
# Push to GitHub and connect
```

### Microservices Deployment
```bash
# Local
start_all.bat

# Docker
docker-compose up -d

# Kubernetes
kubectl apply -f k8s/
```

---

## 🧪 Testing

### Test Monolithic
```bash
streamlit run src/api/app.py
# Open http://localhost:8501
```

### Test Microservices
```bash
cd microservices
python test_services.py
```

---

## 📈 Performance

### Monolithic
- Startup: 5-10 seconds
- Memory: ~500MB
- Response Time: 1-3 seconds

### Microservices
- Startup: 15-20 seconds (all services)
- Memory: ~800MB (total)
- Response Time: 1-3 seconds
- Scalable: Yes (individual services)

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## 📄 License

MIT License - Free to use and modify

---

## 🎯 Use Cases

### Personal Use
- Study notes Q&A
- Research paper analysis
- Book summaries

### Business Use
- Document search
- Knowledge base
- Customer support

### Learning
- RAG systems
- Microservices
- FastAPI
- Docker

---

## 🔗 Links

- **GitHub:** https://github.com/Iamzain804/Lumina-PDF-Bot
- **Groq API:** https://console.groq.com/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Streamlit Docs:** https://docs.streamlit.io/

---

## 💡 Tips

1. **Start Simple:** Begin with monolithic
2. **Learn Concepts:** Understand RAG pipeline
3. **Experiment:** Try different documents
4. **Scale Up:** Move to microservices when ready
5. **Deploy:** Use Docker for production

---

## 🎉 Success Stories

### What You Can Build:
- Personal AI assistant for documents
- Company knowledge base
- Research paper analyzer
- Legal document Q&A
- Medical records search
- Educational content helper

---

## 📞 Support

- **Issues:** GitHub Issues
- **Questions:** GitHub Discussions
- **Email:** Contact via GitHub profile

---

<p align="center">
  <b>Choose Your Path:</b><br><br>
  <a href="#option-1-monolithic-simple">🏢 Monolithic (Simple)</a> | 
  <a href="#option-2-microservices-advanced">🚀 Microservices (Advanced)</a>
</p>

<p align="center">
  Made with ❤️ for the AI Community
</p>

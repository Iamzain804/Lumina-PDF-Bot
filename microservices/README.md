# 🚀 Lumina PDF Bot - Microservices Architecture

## 📋 Architecture Overview

Ye project ab **4 independent microservices** mein divide hai:

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Service                      │
│                  (Streamlit - Port 8501)                 │
└────────────┬────────────┬────────────┬──────────────────┘
             │            │            │
    ┌────────▼───┐  ┌────▼─────┐  ┌──▼──────────┐
    │ Document   │  │ Vector   │  │ LLM         │
    │ Service    │  │ Service  │  │ Service     │
    │ Port 8001  │  │ Port 8002│  │ Port 8003   │
    └────────────┘  └──────────┘  └─────────────┘
```

---

## 🏗️ Services Detail

### 1️⃣ **Document Service** (Port 8001)
**Kaam:** PDF/DOCX/TXT files ko process karna

**Endpoints:**
- `POST /upload` - Document upload
- `GET /documents` - List all documents
- `DELETE /documents/{filename}` - Delete document

**Technology:** FastAPI + PyPDF2

---

### 2️⃣ **Vector Service** (Port 8002)
**Kaam:** Text embeddings create karna aur similarity search

**Endpoints:**
- `POST /create_embeddings` - Embeddings banao
- `POST /search` - Similar chunks dhundo
- `POST /split_text` - Text ko chunks mein todo
- `DELETE /vectors/{doc_id}` - Vectors delete karo

**Technology:** FastAPI + Scikit-learn (TF-IDF)

---

### 3️⃣ **LLM Service** (Port 8003)
**Kaam:** AI responses generate karna

**Endpoints:**
- `POST /generate` - Answer generate karo
- `POST /summarize` - Document summarize karo
- `GET /health` - Health check

**Technology:** FastAPI + Groq/OpenAI/OpenRouter

---

### 4️⃣ **Frontend Service** (Port 8501)
**Kaam:** User interface provide karna

**Features:**
- Document upload UI
- Chat interface
- Real-time responses
- Multi-document support

**Technology:** Streamlit

---

## 🚀 Quick Start

### Method 1: Automated Script (Recommended)

```bash
cd microservices
start_all.bat
```

Ye script automatically:
1. Dependencies install karega
2. Sab services start karega
3. Browser mein frontend khol dega

### Method 2: Manual Start

**Terminal 1 - Document Service:**
```bash
cd microservices/document_service
python app.py
```

**Terminal 2 - Vector Service:**
```bash
cd microservices/vector_service
python app.py
```

**Terminal 3 - LLM Service:**
```bash
cd microservices/llm_service
python app.py
```

**Terminal 4 - Frontend:**
```bash
cd microservices/frontend_service
streamlit run app.py
```

### Method 3: Docker (Optional)

```bash
cd microservices
docker-compose up -d
```

---

## 📦 Installation

```bash
cd microservices
pip install -r requirements.txt
```

---

## ⚙️ Configuration

`.env` file banao root directory mein:

```env
# LLM Provider (groq, openai, openrouter)
LLM_PROVIDER=groq

# API Keys
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Model
LLM_MODEL=llama-3.1-8b-instant
```

---

## 🔧 Testing Services

### Test Document Service:
```bash
curl http://localhost:8001/documents
```

### Test Vector Service:
```bash
curl http://localhost:8002/health
```

### Test LLM Service:
```bash
curl http://localhost:8003/health
```

### Test Frontend:
```
http://localhost:8501
```

---

## 🛑 Stop All Services

```bash
stop_all.bat
```

Ya manually har terminal mein `Ctrl+C` press karo.

---

## 📊 Service Communication Flow

```
1. User uploads PDF → Frontend Service
2. Frontend → Document Service (extract text)
3. Frontend → Vector Service (create embeddings)
4. User asks question → Frontend Service
5. Frontend → Vector Service (search similar chunks)
6. Frontend → LLM Service (generate answer)
7. Frontend → User (display answer)
```

---

## 🎯 Benefits of Microservices

✅ **Scalability:** Har service independently scale ho sakti hai
✅ **Maintainability:** Code organized aur modular hai
✅ **Flexibility:** Kisi bhi service ko easily replace kar sakte ho
✅ **Fault Isolation:** Agar ek service fail ho, baaki chal sakti hain
✅ **Technology Freedom:** Har service different tech use kar sakti hai

---

## 🔄 Monolithic vs Microservices

### Monolithic (Purana):
```
Single App (Port 8501)
├── All code in one place
├── Tightly coupled
└── Hard to scale
```

### Microservices (Naya):
```
4 Independent Services
├── Document Service (8001)
├── Vector Service (8002)
├── LLM Service (8003)
└── Frontend Service (8501)
```

---

## 📝 API Documentation

Har service ka interactive API docs:

- Document Service: http://localhost:8001/docs
- Vector Service: http://localhost:8002/docs
- LLM Service: http://localhost:8003/docs

---

## 🐛 Troubleshooting

**Problem:** Service start nahi ho rahi
**Solution:** Check karo port already use mein to nahi

**Problem:** Connection refused error
**Solution:** Ensure all services running hain

**Problem:** Import errors
**Solution:** `pip install -r requirements.txt` run karo

---

## 📈 Future Enhancements

- [ ] Add authentication & authorization
- [ ] Implement API Gateway
- [ ] Add Redis for caching
- [ ] Add PostgreSQL for metadata
- [ ] Implement message queue (RabbitMQ/Kafka)
- [ ] Add monitoring (Prometheus + Grafana)
- [ ] Add logging service (ELK Stack)

---

## 🤝 Contributing

Contributions welcome! Microservices architecture ko improve karne ke liye PRs submit karo.

---

## 📄 License

MIT License

---

<p align="center">
  Made with ❤️ for Microservices Learning
</p>

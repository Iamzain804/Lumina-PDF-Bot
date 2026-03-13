# 🏗️ Microservices Architecture - Complete Guide

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:8501                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND SERVICE (Streamlit)                  │
│                         Port: 8501                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • File Upload UI                                         │  │
│  │  • Chat Interface                                         │  │
│  │  • Document Management                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────┬──────────────────┬──────────────────┬──────────────────┘
        │                  │                  │
        │ HTTP REST        │ HTTP REST        │ HTTP REST
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│  DOCUMENT    │  │   VECTOR     │  │      LLM         │
│  SERVICE     │  │   SERVICE    │  │    SERVICE       │
│  Port: 8001  │  │  Port: 8002  │  │   Port: 8003     │
├──────────────┤  ├──────────────┤  ├──────────────────┤
│ • PDF Parse  │  │ • Embeddings │  │ • Groq API       │
│ • DOCX Parse │  │ • TF-IDF     │  │ • OpenAI API     │
│ • TXT Parse  │  │ • Search     │  │ • OpenRouter API │
│ • File Store │  │ • Similarity │  │ • Summarization  │
└──────┬───────┘  └──────┬───────┘  └──────────────────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  FILE        │  │   VECTOR     │
│  STORAGE     │  │   STORAGE    │
│  (data/docs) │  │ (data/vecs)  │
└──────────────┘  └──────────────┘
```

---

## 🔄 Request Flow

### 1️⃣ Document Upload Flow
```
User → Frontend → Document Service
                      ↓
                  Extract Text
                      ↓
                  Save to Disk
                      ↓
Frontend ← Response (text, pages)
    ↓
Vector Service
    ↓
Split into Chunks
    ↓
Create Embeddings (TF-IDF)
    ↓
Save Vectors
    ↓
Frontend ← Success
```

### 2️⃣ Question Answering Flow
```
User Question → Frontend
                   ↓
            Vector Service (Search)
                   ↓
         Find Similar Chunks (Top 4)
                   ↓
            Prepare Context
                   ↓
            LLM Service (Generate)
                   ↓
         Generate Answer + Sources
                   ↓
            Frontend ← Display Answer
```

---

## 🎯 Service Responsibilities

### Document Service (8001)
```python
Responsibilities:
├── File Upload & Validation
├── PDF Text Extraction (PyPDF2)
├── DOCX Text Extraction (python-docx)
├── TXT/MD File Reading
├── File Storage Management
└── Document Metadata

Dependencies:
├── FastAPI
├── PyPDF2
├── python-docx
└── python-multipart
```

### Vector Service (8002)
```python
Responsibilities:
├── Text Chunking (RecursiveCharacterTextSplitter)
├── TF-IDF Embeddings Creation
├── Vector Storage (Pickle)
├── Similarity Search (Cosine)
└── Top-K Retrieval

Dependencies:
├── FastAPI
├── scikit-learn
├── numpy
└── pickle
```

### LLM Service (8003)
```python
Responsibilities:
├── Answer Generation
├── Document Summarization
├── Multi-Provider Support (Groq/OpenAI/OpenRouter)
├── Prompt Engineering
└── Source Extraction

Dependencies:
├── FastAPI
├── groq
├── openai
└── python-dotenv
```

### Frontend Service (8501)
```python
Responsibilities:
├── User Interface (Streamlit)
├── Service Orchestration
├── Chat History Management
├── File Upload UI
└── Response Display

Dependencies:
├── streamlit
└── requests
```

---

## 🔌 API Endpoints

### Document Service (8001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload document |
| GET | `/documents` | List all documents |
| DELETE | `/documents/{filename}` | Delete document |

### Vector Service (8002)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create_embeddings` | Create embeddings |
| POST | `/search` | Search similar chunks |
| POST | `/split_text` | Split text into chunks |
| DELETE | `/vectors/{doc_id}` | Delete vectors |

### LLM Service (8003)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate` | Generate answer |
| POST | `/summarize` | Summarize document |
| GET | `/health` | Health check |

---

## 📦 Data Flow

```
┌─────────────┐
│   Upload    │
│   PDF File  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Document Service   │
│  Extracts Text      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Vector Service     │
│  1. Split Text      │
│  2. Create Vectors  │
│  3. Store Vectors   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  User Asks Question │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Vector Service     │
│  Search Top-K       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  LLM Service        │
│  Generate Answer    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Frontend           │
│  Display to User    │
└─────────────────────┘
```

---

## 🚀 Deployment Options

### Option 1: Local Development
```bash
# Start each service in separate terminal
cd microservices
start_all.bat
```

### Option 2: Docker Compose
```bash
cd microservices
docker-compose up -d
```

### Option 3: Kubernetes (Production)
```yaml
# Deploy to K8s cluster
kubectl apply -f k8s/
```

---

## 🔐 Security Considerations

1. **API Keys**: Store in `.env`, never commit
2. **CORS**: Configure properly for production
3. **Rate Limiting**: Add to prevent abuse
4. **Authentication**: Add JWT tokens
5. **Input Validation**: Sanitize all inputs

---

## 📈 Scaling Strategy

### Horizontal Scaling
```
Document Service: 3 replicas
Vector Service: 2 replicas
LLM Service: 2 replicas
Frontend: 2 replicas
```

### Load Balancer
```
NGINX/Traefik
    ↓
Round Robin to Service Replicas
```

---

## 🐛 Debugging

### Check Service Health
```bash
python test_services.py
```

### View Logs
```bash
# Document Service
curl http://localhost:8001/docs

# Vector Service
curl http://localhost:8002/docs

# LLM Service
curl http://localhost:8003/docs
```

---

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- Microservices: https://microservices.io/
- Docker: https://docs.docker.com/
- Streamlit: https://docs.streamlit.io/

---

Made with ❤️ for Learning Microservices Architecture

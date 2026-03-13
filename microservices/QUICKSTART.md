# ⚡ QUICK START GUIDE - Microservices

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
cd microservices
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 min)
Create `.env` file in root directory:
```env
GROQ_API_KEY=your_groq_key_here
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
```

### Step 3: Start All Services (1 min)
```bash
start_all.bat
```

### Step 4: Open Browser (1 min)
```
http://localhost:8501
```

### Step 5: Upload & Chat (1 min)
1. Upload PDF
2. Ask questions
3. Get AI answers!

---

## 🎯 What You Get

### 4 Independent Services:

1. **Document Service (8001)**
   - Handles PDF/DOCX/TXT uploads
   - Extracts text from documents

2. **Vector Service (8002)**
   - Creates embeddings
   - Searches similar content

3. **LLM Service (8003)**
   - Generates AI answers
   - Summarizes documents

4. **Frontend (8501)**
   - Beautiful UI
   - Chat interface

---

## 🧪 Test Services

```bash
python test_services.py
```

Expected Output:
```
✅ Document Service - Running
✅ Vector Service - Running
✅ LLM Service - Running
✅ Frontend Service - Running
```

---

## 🛑 Stop Services

```bash
stop_all.bat
```

---

## 📊 Service URLs

| Service | URL | API Docs |
|---------|-----|----------|
| Document | http://localhost:8001 | /docs |
| Vector | http://localhost:8002 | /docs |
| LLM | http://localhost:8003 | /docs |
| Frontend | http://localhost:8501 | - |

---

## 🐛 Troubleshooting

### Problem: Port already in use
```bash
# Kill all Python processes
taskkill /F /IM python.exe
```

### Problem: Module not found
```bash
pip install -r requirements.txt
```

### Problem: API key error
```bash
# Check .env file exists in root
# Verify API key is correct
```

---

## 🎓 Learn More

- **Architecture:** Read `ARCHITECTURE.md`
- **Comparison:** Read `COMPARISON.md`
- **Full Guide:** Read `README.md`

---

## 💡 Quick Tips

1. **Upload any document:** PDF, DOCX, TXT, MD
2. **Ask natural questions:** "What is this about?"
3. **View sources:** See which pages were used
4. **Multiple documents:** Upload and switch between them

---

## 🎉 Success!

Aapka microservices architecture ready hai!

**Next Steps:**
- Try uploading different documents
- Ask complex questions
- Explore API documentation
- Modify services
- Deploy to cloud

---

Made with ❤️ for Quick Learning

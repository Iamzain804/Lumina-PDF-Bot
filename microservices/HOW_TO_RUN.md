# 🚀 HOW TO RUN - Complete Guide

## ⚡ Quick Start (3 Methods)

---

### **Method 1: PowerShell Script (RECOMMENDED)**

```powershell
# Step 1: Open PowerShell in microservices folder
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices"

# Step 2: Run PowerShell script
.\start_all.ps1
```

**Note:** Agar execution policy error aaye to:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### **Method 2: Batch File (CMD)**

```cmd
# Step 1: Open CMD in microservices folder
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices"

# Step 2: Run batch file
.\start_all.bat
```

---

### **Method 3: Manual Start (4 Terminals)**

#### Terminal 1 - Document Service:
```powershell
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices\document_service"
python app.py
```

#### Terminal 2 - Vector Service:
```powershell
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices\vector_service"
python app.py
```

#### Terminal 3 - LLM Service:
```powershell
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices\llm_service"
python app.py
```

#### Terminal 4 - Frontend:
```powershell
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices\frontend_service"
streamlit run app.py
```

---

## 🔧 Setup (First Time Only)

### Step 1: Install Dependencies
```powershell
cd "e:\zain d drive\pdf rag system\pdf_chatbot\microservices"
pip install -r requirements.txt
```

### Step 2: Create .env File
Create `.env` file in root directory (`pdf_chatbot/.env`):

```env
GROQ_API_KEY=your_groq_key_here
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
```

**Get API Key:**
- Groq: https://console.groq.com/keys
- OpenAI: https://platform.openai.com/api-keys
- OpenRouter: https://openrouter.ai/keys

---

## 🎯 After Starting Services

### Check if Running:
```powershell
python test_services.py
```

Expected Output:
```
✅ Document Service - Running
✅ Vector Service - Running
✅ LLM Service - Running
✅ Frontend Service - Running
```

### Access Services:

| Service | URL |
|---------|-----|
| **Frontend (Main UI)** | http://localhost:8501 |
| Document Service API | http://localhost:8001/docs |
| Vector Service API | http://localhost:8002/docs |
| LLM Service API | http://localhost:8003/docs |

---

## 🛑 Stop Services

### PowerShell:
```powershell
.\stop_all.ps1
```

### CMD:
```cmd
.\stop_all.bat
```

### Manual:
Press `Ctrl+C` in each terminal window

---

## 🐛 Troubleshooting

### Error: "Execution Policy"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Port already in use"
```powershell
# Kill all Python processes
Get-Process python | Stop-Process -Force
```

### Error: "Module not found"
```powershell
pip install -r requirements.txt
```

### Error: "Cannot connect to service"
Wait 10-15 seconds for all services to start, then try again.

---

## 📊 Service Status Check

### Check Individual Service:

**Document Service:**
```powershell
curl http://localhost:8001/documents
```

**Vector Service:**
```powershell
curl http://localhost:8002/health
```

**LLM Service:**
```powershell
curl http://localhost:8003/health
```

**Frontend:**
Open browser: http://localhost:8501

---

## 🎓 Usage Guide

### 1. Upload Document
- Open http://localhost:8501
- Click "Choose file"
- Select PDF/DOCX/TXT/MD
- Click "Process Document"

### 2. Ask Questions
- Type question in chat box
- Press Enter or click Send
- Get AI-powered answer with sources

### 3. Multiple Documents
- Upload multiple files
- Switch between them in sidebar
- Each has separate chat history

---

## 🔄 Development Workflow

### Modify a Service:
```powershell
# 1. Stop that service (Ctrl+C in its terminal)
# 2. Edit code
# 3. Restart service
cd service_folder
python app.py
```

### Test Changes:
```powershell
# Test specific endpoint
curl http://localhost:8001/documents
```

---

## 🐳 Docker Method (Alternative)

### Start with Docker:
```powershell
cd microservices
docker-compose up -d
```

### Stop with Docker:
```powershell
docker-compose down
```

### View Logs:
```powershell
docker-compose logs -f
```

---

## 📝 Common Commands

### Install Dependencies:
```powershell
pip install -r requirements.txt
```

### Update Dependencies:
```powershell
pip install --upgrade -r requirements.txt
```

### Check Python Version:
```powershell
python --version
```

### Check Installed Packages:
```powershell
pip list
```

---

## 🎯 Quick Reference

### Start Services:
```powershell
.\start_all.ps1          # PowerShell
.\start_all.bat          # CMD
```

### Stop Services:
```powershell
.\stop_all.ps1           # PowerShell
.\stop_all.bat           # CMD
```

### Test Services:
```powershell
python test_services.py
```

### Open Frontend:
```
http://localhost:8501
```

---

## 💡 Tips

1. **Always start from microservices folder**
2. **Wait 10-15 seconds for all services to start**
3. **Check test_services.py to verify all running**
4. **Use PowerShell for better experience**
5. **Keep terminal windows open while using**

---

## 🎉 Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file created with API key
- [ ] All 4 services started
- [ ] test_services.py shows all ✅
- [ ] Frontend opens at http://localhost:8501
- [ ] Can upload document
- [ ] Can ask questions
- [ ] Getting AI responses

---

## 📞 Need Help?

### Check Logs:
Each service window shows logs - check for errors

### Common Issues:
1. **Port in use** → Stop all Python processes
2. **Module error** → Reinstall dependencies
3. **API error** → Check .env file and API key
4. **Connection error** → Wait for services to start

---

<p align="center">
  <b>Happy Coding! 🚀</b>
</p>

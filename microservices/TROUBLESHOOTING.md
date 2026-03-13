# 🐛 Troubleshooting Guide

## ✅ Error Fixed: KeyError 'answer'

**Problem:** LLM Service error throw kar rahi thi aur frontend properly handle nahi kar raha tha.

**Solution:** Ab dono services properly error handle karti hain.

---

## 🔄 How to Apply Fix

### Step 1: Stop All Services
```powershell
.\stop_all.ps1
```

### Step 2: Restart Services
```powershell
.\start_all.ps1
```

---

## 🧪 Test After Fix

```powershell
python test_services.py
```

---

## 📋 Common Errors & Solutions

### 1. **KeyError: 'answer'**
**Cause:** LLM service error
**Solution:** 
- Check `.env` file has correct API key
- Verify internet connection
- Restart LLM service

### 2. **Connection Refused**
**Cause:** Service not running
**Solution:**
```powershell
# Check which services are running
python test_services.py

# Restart specific service
cd llm_service
python app.py
```

### 3. **Port Already in Use**
**Cause:** Previous instance still running
**Solution:**
```powershell
# Kill all Python processes
Get-Process python | Stop-Process -Force

# Restart services
.\start_all.ps1
```

### 4. **Module Not Found**
**Cause:** Dependencies not installed
**Solution:**
```powershell
pip install -r requirements.txt
```

### 5. **API Key Error**
**Cause:** Invalid or missing API key
**Solution:**
Check `.env` file:
```env
GROQ_API_KEY=your_actual_key_here
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
```

Get API key from: https://console.groq.com/keys

### 6. **Empty Response**
**Cause:** No context found
**Solution:** Document properly processed nahi hui
```powershell
# Re-upload document
# Check vector service logs
```

---

## 🔍 Debug Individual Service

### Document Service (8001)
```powershell
cd document_service
python app.py
# Check logs for errors
```

### Vector Service (8002)
```powershell
cd vector_service
python app.py
# Check logs for errors
```

### LLM Service (8003)
```powershell
cd llm_service
python app.py
# Check logs for errors
```

### Frontend (8501)
```powershell
cd frontend_service
streamlit run app.py
# Check logs for errors
```

---

## 📊 Check Service Health

### Manual Check:
```powershell
# Document Service
curl http://localhost:8001/documents

# Vector Service  
curl http://localhost:8002/health

# LLM Service
curl http://localhost:8003/health

# Frontend
# Open: http://localhost:8501
```

### Automated Check:
```powershell
python test_services.py
```

---

## 🔧 Reset Everything

```powershell
# 1. Stop all services
.\stop_all.ps1

# 2. Clear data (optional)
Remove-Item -Recurse -Force data\documents\*
Remove-Item -Recurse -Force data\vectors\*

# 3. Reinstall dependencies
pip install --upgrade -r requirements.txt

# 4. Restart services
.\start_all.ps1
```

---

## 📝 Check Logs

Each service window shows real-time logs. Look for:
- ✅ `INFO: Application startup complete`
- ❌ `ERROR:` messages
- ⚠️ `WARNING:` messages

---

## 🎯 Verify Fix Working

1. Start all services
2. Upload a PDF
3. Ask a question
4. Should get proper answer (no KeyError)

---

## 💡 Prevention Tips

1. Always check `.env` file first
2. Verify all services running before use
3. Wait 10-15 seconds after starting services
4. Check logs if something fails
5. Use `test_services.py` regularly

---

## 🆘 Still Having Issues?

### Check:
- [ ] Python version (3.8+)
- [ ] All dependencies installed
- [ ] .env file exists with API key
- [ ] Internet connection working
- [ ] No firewall blocking ports
- [ ] Sufficient disk space

### Get Help:
- Check service logs
- Run `python test_services.py`
- Verify API key is valid
- Try with different document

---

**Error ab fix ho gaya hai! Services restart karo aur try karo! 🚀**

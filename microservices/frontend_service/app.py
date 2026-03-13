"""🎨 Frontend Service - Enhanced Streamlit UI Microservice"""
import streamlit as st
import requests
from datetime import datetime
from typing import Dict, List
import time

# Service URLs
DOCUMENT_SERVICE = "http://localhost:8001"
VECTOR_SERVICE = "http://localhost:8002"
LLM_SERVICE = "http://localhost:8003"

st.set_page_config(
    page_title="Lumina PDF Bot - Microservices",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with Purple, Cyan, White theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #1a0033 0%, #0a0a1f 50%, #001a33 100%);
}

/* Header */
.main-header {
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a855f7 0%, #06b6d4 50%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
}

.subtitle {
    text-align: center;
    color: #06b6d4;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0033 0%, #0d001a 100%);
    border-right: 2px solid #a855f7;
}

[data-testid="stSidebar"] h3 {
    color: #06b6d4;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    border: 2px solid #a855f7;
    background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
    color: white;
    font-weight: 600;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6);
    background: linear-gradient(135deg, #c084fc 0%, #a855f7 100%);
    border-color: #06b6d4;
}

/* Chat Messages */
.stChatMessage {
    background: rgba(168, 85, 247, 0.1);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(6, 182, 212, 0.1);
    border: 2px dashed #06b6d4;
    border-radius: 12px;
    padding: 1rem;
}

/* Info boxes */
.stInfo {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(168, 85, 247, 0.2));
    border-left: 4px solid #06b6d4;
    color: white;
}

/* Success boxes */
.stSuccess {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(6, 182, 212, 0.2));
    border-left: 4px solid #22c55e;
    color: white;
}

/* Error boxes */
.stError {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(168, 85, 247, 0.2));
    border-left: 4px solid #ef4444;
    color: white;
}

/* Warning boxes */
.stWarning {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(6, 182, 212, 0.2));
    border-left: 4px solid #fbbf24;
    color: white;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #a855f7 0%, #06b6d4 100%);
    margin: 1.5rem 0;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #a855f7 !important;
}

/* Input fields */
.stTextInput>div>div>input {
    background: rgba(168, 85, 247, 0.1);
    border: 2px solid #a855f7;
    color: white;
    border-radius: 10px;
}

.stTextInput>div>div>input:focus {
    border-color: #06b6d4;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.5);
}

/* Chat input */
.stChatInputContainer {
    border-top: 2px solid #a855f7;
    background: rgba(26, 0, 51, 0.8);
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #06b6d4;
    font-weight: 700;
}

/* Document cards */
.doc-card {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(6, 182, 212, 0.1));
    border: 2px solid #a855f7;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
}

.doc-card:hover {
    border-color: #06b6d4;
    box-shadow: 0 5px 20px rgba(6, 182, 212, 0.3);
    transform: translateX(5px);
}

/* Status badge */
.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    background: linear-gradient(135deg, #a855f7, #06b6d4);
    color: white;
    margin: 0.25rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1a0033;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #a855f7, #06b6d4);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #c084fc, #22d3ee);
}
</style>
""", unsafe_allow_html=True)

def init_session():
    """Initialize session state"""
    if 'current_doc' not in st.session_state:
        st.session_state.current_doc = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None
    if 'last_question' not in st.session_state:
        st.session_state.last_question = None
    if 'question_processed' not in st.session_state:
        st.session_state.question_processed = False

def upload_document(file) -> Dict:
    """📤 Upload document to Document Service with error handling"""
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(
            f"{DOCUMENT_SERVICE}/upload",
            files=files,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "detail": f"Upload failed with status {response.status_code}"
            }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "detail": "Cannot connect to Document Service. Please ensure it's running on port 8001."
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "detail": "Upload timeout. File might be too large."
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def create_embeddings(doc_id: str, text: str) -> Dict:
    """Create embeddings via Vector Service"""
    try:
        # Split text with smaller chunks for faster processing
        split_response = requests.post(
            f"{VECTOR_SERVICE}/split_text",
            params={"text": text, "chunk_size": 800},
            timeout=10
        )
        chunks = split_response.json()["chunks"]
        
        # Limit chunks for faster processing (max 50 chunks)
        if len(chunks) > 50:
            chunks = chunks[:50]
        
        # Create embeddings
        response = requests.post(
            f"{VECTOR_SERVICE}/create_embeddings",
            json={"doc_id": doc_id, "chunks": chunks},
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def search_document(doc_id: str, query: str, top_k: int = 4) -> List[Dict]:
    """Search document via Vector Service"""
    try:
        response = requests.post(
            f"{VECTOR_SERVICE}/search",
            json={"doc_id": doc_id, "query": query, "top_k": top_k}
        )
        return response.json()["results"]
    except Exception as e:
        return []

def generate_answer(question: str, context: str) -> Dict:
    """Generate answer via LLM Service"""
    try:
        response = requests.post(
            f"{LLM_SERVICE}/generate",
            json={"question": question, "context": context},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": f"❌ LLM Service Error: {response.status_code}\n\nPlease check if LLM service is running on port 8003.",
                "sources": [],
                "confidence": "low"
            }
    except requests.exceptions.ConnectionError:
        return {
            "answer": "❌ Cannot connect to LLM Service.\n\nPlease ensure LLM service is running on port 8003.",
            "sources": [],
            "confidence": "low"
        }
    except requests.exceptions.Timeout:
        return {
            "answer": "❌ LLM Service timeout.\n\nThe request took too long. Please try again.",
            "sources": [],
            "confidence": "low"
        }
    except Exception as e:
        return {
            "answer": f"❌ Error: {str(e)}",
            "sources": [],
            "confidence": "low"
        }

def list_documents() -> List[Dict]:
    """List all documents"""
    try:
        response = requests.get(f"{DOCUMENT_SERVICE}/documents")
        return response.json()["documents"]
    except:
        return []

def main():
    init_session()
    
    # Enhanced Header
    st.markdown('<h1 class="main-header">🤖 Lumina PDF Bot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✨ Microservices Architecture | AI-Powered Document Intelligence ✨</p>', unsafe_allow_html=True)
    
    # Service Status Indicator
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="status-badge">📄 Document Service</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="status-badge">🧠 Vector Service</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="status-badge">🤖 LLM Service</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="status-badge">🌐 Frontend Active</div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📤 Upload Document")
        st.caption("📁 Supported: PDF, DOCX, TXT, MD | Max: 50MB")
        
        uploaded_file = st.file_uploader(
            "Choose file",
            type=["pdf", "txt", "md", "docx"],
            help="Upload your document to start chatting"
        )
        
        if uploaded_file:
            # Show file info
            file_size = uploaded_file.size / 1024 / 1024  # MB
            st.info(f"📄 **{uploaded_file.name}**\n\n📊 Size: {file_size:.2f} MB")
            
            # Check if already processed
            if st.session_state.last_uploaded_file == uploaded_file.name:
                st.success("✅ This document is already processed!")
            
            if st.button("🚀 Process Document", type="primary", disabled=st.session_state.processing):
                # Prevent duplicate processing
                if st.session_state.last_uploaded_file == uploaded_file.name:
                    st.warning("⚠️ Document already processed! Select a different document.")
                elif file_size > 50:
                    st.error("❌ File too large! Maximum size is 50MB.")
                else:
                    st.session_state.processing = True
                    
                    with st.spinner("🔄 Processing document..."):
                        progress_bar = st.progress(0)
                        
                        # Upload document
                        progress_bar.progress(25)
                        result = upload_document(uploaded_file)
                        
                        if result.get("status") == "success":
                            doc_id = result["filename"].split('.')[0]
                            
                            # Create embeddings
                            progress_bar.progress(50)
                            embed_result = create_embeddings(doc_id, result["text"])
                            
                            progress_bar.progress(100)
                            
                            if embed_result.get("status") == "success":
                                st.success("✅ Document processed successfully!")
                                st.balloons()
                                
                                # Mark as processed
                                st.session_state.last_uploaded_file = uploaded_file.name
                                
                                # Clear old chat history for new document
                                st.session_state.chat_history = []
                                st.session_state.current_doc = {
                                    "id": doc_id,
                                    "name": result["filename"],
                                    "pages": result["page_count"]
                                }
                                
                                st.session_state.processing = False
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ Embedding failed: {embed_result.get('detail', 'Unknown error')}")
                                st.session_state.processing = False
                        else:
                            st.error(f"❌ Upload failed: {result.get('detail', 'Unknown error')}")
                            st.session_state.processing = False
                        
                        progress_bar.empty()
        
        st.divider()
        
        # Document list
        st.markdown("### 📚 Document Library")
        docs = list_documents()
        
        if not docs:
            st.info("💭 No documents yet. Upload one to get started!")
        else:
            st.caption(f"📂 {len(docs)} document(s) available")
            
            for doc in docs:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.button(
                            f"📄 {doc['filename']}",
                            key=doc['filename'],
                            use_container_width=True
                        ):
                            # Clear chat history when switching documents
                            st.session_state.chat_history = []
                            st.session_state.current_doc = {
                                "id": doc['filename'].split('.')[0],
                                "name": doc['filename']
                            }
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️", key=f"del_{doc['filename']}", help="Delete"):
                            # Add confirmation
                            st.session_state[f"confirm_delete_{doc['filename']}"] = True
                    
                    # Show file size
                    st.caption(f"📊 {doc.get('size', 'Unknown size')}")
        
        st.divider()
        
        # Current document info
        if st.session_state.current_doc:
            st.markdown("### 📄 Current Document")
            st.info(st.session_state.current_doc['name'])
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Main chat area
    if not st.session_state.current_doc:
        st.info("👈 Upload a document to start chatting!")
    else:
        st.markdown("### 💬 Chat")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg.get("sources"):
                    st.caption(f"📄 Sources: {', '.join(map(str, msg['sources']))}")
        
        # Chat input
        question = st.chat_input("Ask a question...", disabled=st.session_state.processing)
        
        if question and not st.session_state.processing:
            # Check if same question already processed
            if (st.session_state.last_question == question and 
                st.session_state.question_processed):
                st.warning("⚠️ This question was just answered! Check the chat above.")
            else:
                st.session_state.processing = True
                st.session_state.last_question = question
                st.session_state.question_processed = True
                
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                # Search and generate answer
                with st.spinner("Thinking..."):
                    # Search for relevant chunks
                    results = search_document(st.session_state.current_doc["id"], question)
                    
                    # Prepare context
                    context = "\n\n".join([r["chunk"] for r in results])
                    
                    # Generate answer
                    response = generate_answer(question, context)
                    
                    # Add assistant message
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response.get("sources", [])
                    })
                
                st.session_state.processing = False
                st.session_state.question_processed = False
                st.rerun()

if __name__ == "__main__":
    main()

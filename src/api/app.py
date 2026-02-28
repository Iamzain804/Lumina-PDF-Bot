"""📄 Smart PDF Chatbot - Streamlit UI Application"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict

# Import custom modules
from src.core.config import Config
from src.handlers.llm_handler import GroqLLMHandler
from src.engine.vector_store import DocumentVectorStore
from src.services.chat_manager import ChatManager
from src.engine.rag_engine import RAGEngine
from src.utils.utils import validate_pdf, get_file_size

# Page Configuration
st.set_page_config(
    page_title="📄 Smart PDF Chatbot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sidebar-section {
    margin: 1rem 0;
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f0f2f6;
}
.pdf-item {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 0.25rem;
    background-color: white;
}
.success-msg {
    color: #28a745;
    font-weight: bold;
}
.error-msg {
    color: #dc3545;
    font-weight: bold;
}
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    background-color: #fafafa;
}
.user-message {
    background-color: #007bff;
    color: white;
    padding: 0.75rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    margin-left: 20%;
    text-align: right;
}
.assistant-message {
    background-color: #f8f9fa;
    color: #333;
    padding: 0.75rem;
    border-radius: 1rem;
    margin: 0.5rem 0;
    margin-right: 20%;
    border-left: 4px solid #28a745;
}
.source-pill {
    background-color: #17a2b8;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    margin: 0.25rem;
    display: inline-block;
}
.timestamp {
    font-size: 0.7rem;
    color: #6c757d;
    margin-top: 0.25rem;
}
.suggested-question {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 1rem;
    padding: 0.5rem 1rem;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.2s;
}
.suggested-question:hover {
    background-color: #007bff;
    color: white;
}
.welcome-section {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables."""
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'current_pdf' not in st.session_state:
        st.session_state.current_pdf = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = None
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.3
    if 'max_tokens' not in st.session_state:
        st.session_state.max_tokens = 512
    if 'top_k' not in st.session_state:
        st.session_state.top_k = 4
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()

def initialize_components():
    """Initialize all components once."""
    if st.session_state.rag_engine is None:
        try:
            with st.spinner("🔧 Initializing components..."):
                # Load configuration
                config = Config()
                
                # Initialize handlers
                llm_handler = GroqLLMHandler(config)
                vector_store = DocumentVectorStore(config)
                chat_manager = ChatManager()
                
                # Create RAG engine
                st.session_state.rag_engine = RAGEngine(
                    config, llm_handler, vector_store, chat_manager
                )
                
            st.success("✅ Components initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize components: {str(e)}")
            st.stop()

def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp to relative time.
    
    Args:
        timestamp_str: ISO format timestamp string
        
    Returns:
        Formatted relative time string
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        diff = now - timestamp
        
        if diff.seconds < 60:
            return "Just now"
        elif diff.seconds < 3600:
            return f"{diff.seconds // 60} mins ago"
        elif diff.days == 0:
            return f"{diff.seconds // 3600} hours ago"
        else:
            return f"{diff.days} days ago"
    except:
        return "Unknown time"

def display_sources(sources: List[str]) -> str:
    """Display source pages as pills.
    
    Args:
        sources: List of page numbers
        
    Returns:
        HTML string with source pills
    """
    if not sources:
        return ""
    
    pills = []
    for source in sources:
        pills.append(f'<span class="source-pill">Page {source}</span>')
    
    return f'<div style="margin-top: 0.5rem;">{"".join(pills)}</div>'

def display_chat_message(role: str, content: str, metadata: Dict = None):
    """Display a chat message with proper styling.
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        metadata: Additional metadata (sources, timestamp, etc.)
    """
    timestamp = metadata.get('timestamp', '') if metadata else ''
    sources = metadata.get('sources', []) if metadata else []
    
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            👤 {content}
            <div class="timestamp">{format_timestamp(timestamp)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Clean HTML from content and display sources separately
        clean_content = content.replace('<', '&lt;').replace('>', '&gt;')
        
        st.markdown(f"""
        <div class="assistant-message">
            🤖 {clean_content}
            <div class="timestamp">{format_timestamp(timestamp)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display sources as Streamlit pills
        if sources:
            cols = st.columns(len(sources) if len(sources) <= 5 else 5)
            for i, source in enumerate(sources[:5]):
                with cols[i % 5]:
                    st.markdown(f'<span style="background-color: #17a2b8; color: white; padding: 0.25rem 0.5rem; border-radius: 1rem; font-size: 0.8rem; margin: 0.25rem; display: inline-block;">Page {source}</span>', unsafe_allow_html=True)

def get_suggested_questions(pdf_name: str) -> List[str]:
    """Get suggested questions for the current PDF.
    
    Args:
        pdf_name: Name of current PDF
        
    Returns:
        List of suggested questions
    """
    base_questions = [
        "Summarize this document",
        "What are the main topics?",
        "List the key points",
        "What is this document about?"
    ]
    
    return base_questions

def generate_response(question: str) -> Dict[str, any]:
    """Generate fast response using optimized RAG.
    
    Args:
        question: User question
        
    Returns:
        Response dictionary
    """
    try:
        # Show immediate feedback
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Searching document...")
        progress_bar.progress(25)
        
        # Quick RAG query with timeout
        import time
        start_time = time.time()
        
        response = st.session_state.rag_engine.query(
            st.session_state.current_pdf, question
        )
        
        progress_bar.progress(100)
        elapsed_time = time.time() - start_time
        status_text.text(f"✅ Response generated in {elapsed_time:.1f}s")
        
        # Clear progress indicators after 1 second
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        return response
        
    except Exception as e:
        # Clear progress indicators on error
        try:
            progress_bar.empty()
            status_text.empty()
        except:
            pass
            
        error_msg = str(e)
        
        # Fast offline fallback
        if "rate_limit_exceeded" in error_msg or "429" in error_msg or "timeout" in error_msg.lower():
            try:
                from src.services.offline_chatbot import OfflineChatbot
                
                if 'offline_bot' not in st.session_state:
                    st.session_state.offline_bot = OfflineChatbot()
                    
                    if st.session_state.current_pdf:
                        try:
                            from pathlib import Path
                            doc_dir = Path("data/pdfs")
                            doc_files = list(doc_dir.glob(f"{st.session_state.current_pdf}.*"))
                            if doc_files:
                                st.session_state.offline_bot.load_document_content(str(doc_files[0]))
                        except Exception:
                            pass
                
                # Fast offline response
                response = st.session_state.offline_bot.generate_offline_response(question)
                return response
                
            except Exception:
                return {
                    "answer": "⚡ **Fast Mode Active**\n\nAPI timeout detected. Using quick analysis.\n\n💰 For full AI features, check your connection.",
                    "sources": [],
                    "confidence": "low"
                }
        
        return {
            "answer": f"❌ **Error**: {error_msg}\n\nTry a shorter question or check your connection.",
            "sources": [],
            "confidence": "low"
        }

def export_chat(format_type: str) -> str:
    """Export chat history in specified format.
    
    Args:
        format_type: 'json' or 'txt'
        
    Returns:
        Formatted chat data
    """
    try:
        if not st.session_state.current_pdf:
            return "No PDF selected"
        
        return st.session_state.rag_engine.chat_manager.export_chat(
            st.session_state.current_pdf, format_type
        )
    except Exception as e:
        return f"Export error: {str(e)}"

def display_welcome_screen():
    """Display welcome screen when no document is selected."""
    st.markdown("""
    <div class="welcome-section">
        <h1>🚀 Welcome to Smart Document Chatbot</h1>
        <h3>Chat with your documents using AI</h3>
        <p>Upload PDF, Word, Text, or Markdown documents and start asking questions!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎆 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📄 Multi-Format Support**
        - PDF documents
        - Word files (.docx)
        - Text files (.txt)
        - Markdown files (.md)
        """)
    
    with col2:
        st.markdown("""
        **🤖 AI-Powered Chat**
        - Natural language questions
        - Context-aware responses
        - Source page references
        """)
    
    with col3:
        st.markdown("""
        **📊 Advanced Features**
        - Chat history management
        - Export conversations
        - Multiple document support
        """)
    
    st.info("👈 **Get Started:** Upload any document (PDF, DOCX, TXT, MD) using the sidebar to begin chatting!")

def display_chat_interface():
    """Display the main chat interface."""
    # Load chat history
    chat_messages = st.session_state.rag_engine.chat_manager.get_chat_history(
        st.session_state.current_pdf, limit=50
    )
    
    # Chat container
    st.markdown("### ⚡ Fast AI Chat")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not chat_messages:
            st.info("⚡ Fast AI responses! Optimized for speed and accuracy.")
        else:
            for msg in chat_messages:
                display_chat_message(
                    msg['role'], 
                    msg['content'], 
                    {'timestamp': msg['timestamp'], 'sources': msg.get('metadata', {}).get('sources', [])}
                )
    
    # Quick actions - suggested questions
    st.markdown("### 💡 Suggested Questions")
    suggested_questions = get_suggested_questions(st.session_state.current_pdf)
    
    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(question, key=f"suggest_{i}"):
                # Generate response for suggested question
                response = generate_response(question)
                st.rerun()
    
    # Input section
    st.markdown("### ✏️ Ask a Question")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "Ask anything about the PDF...",
            key="user_input",
            placeholder="What is this document about?"
        )
    
    with col2:
        send_button = st.button("🚀 Send", type="primary")
        clear_button = st.button("🗑️ Clear Chat", type="secondary")
    
    # Handle send button
    if send_button and user_question.strip():
        response = generate_response(user_question.strip())
        st.rerun()
    
    # Handle clear chat
    if clear_button:
        if st.checkbox("⚠️ Confirm clear chat history"):
            st.session_state.rag_engine.chat_manager.clear_history(
                st.session_state.current_pdf
            )
            st.success("✅ Chat history cleared!")
            st.rerun()
    
    # Footer section
    st.markdown("---")
    st.markdown("### 📊 Chat Statistics & Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stats = st.session_state.rag_engine.chat_manager.get_statistics(
            st.session_state.current_pdf
        )
        st.metric("💬 Total Messages", stats['total_messages'])
    
    with col2:
        session_duration = datetime.now() - st.session_state.session_start
        hours = session_duration.seconds // 3600
        minutes = (session_duration.seconds % 3600) // 60
        st.metric("⏱️ Session Time", f"{hours}h {minutes}m")
    
    with col3:
        # Export options
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("💾 Export JSON"):
                json_data = export_chat("json")
                st.download_button(
                    "Download JSON",
                    json_data,
                    f"chat_{st.session_state.current_pdf}.json",
                    "application/json"
                )
        
        with export_col2:
            if st.button("📄 Export TXT"):
                txt_data = export_chat("csv")
                st.download_button(
                    "Download TXT",
                    txt_data,
                    f"chat_{st.session_state.current_pdf}.txt",
                    "text/plain"
                )

# [Previous helper functions remain the same - handle_pdf_upload, display_pdf_list, etc.]

def handle_document_upload(uploaded_file) -> bool:
    """Handle document file upload and processing.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate document
        is_valid, error_msg = validate_document(uploaded_file)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return False
        
        # Process document
        with st.spinner(f"📄 Processing {uploaded_file.type} document..."):
            result = st.session_state.rag_engine.process_document(
                uploaded_file, uploaded_file.name
            )
        
        if result["status"] == "success":
            st.success(f"✅ Document processed successfully!")
            st.session_state.current_pdf = result["pdf_name"]
            st.session_state.processing_status = result
            return True
        else:
            st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        st.error(f"❌ Upload error: {str(e)}")
        return False

def validate_document(file) -> tuple:
    """Validate uploaded document file.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file type
        allowed_types = ['.pdf', '.txt', '.md', '.docx']
        file_ext = '.' + file.name.split('.')[-1].lower()
        
        if file_ext not in allowed_types:
            return False, f"File type {file_ext} not supported. Use: PDF, TXT, MD, DOCX"
        
        # Check file size (50MB limit)
        if file.size > 50 * 1024 * 1024:
            return False, "File size must be less than 50MB"
        
        # Check if file is empty
        if file.size == 0:
            return False, "File is empty"
        
        return True, "Valid document file"
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def display_pdf_list():
    """Display list of available documents."""
    try:
        docs = st.session_state.rag_engine.list_available_documents()
        
        if not docs:
            st.info("📭 No documents uploaded yet")
            return
        
        with st.expander(f"📚 Available Documents ({len(docs)})", expanded=True):
            for doc in docs:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Show file type icon
                    file_type = doc.get('file_type', 'DOC')
                    icon = {
                        'PDF': '📄',
                        'TXT': '📝', 
                        'MD': '📝',
                        'DOCX': '📄'
                    }.get(file_type, '📄')
                    
                    if st.button(
                        f"{icon} {doc['filename']}",
                        key=f"select_{doc['pdf_name']}",
                        help=f"Type: {file_type} | Size: {doc['file_size']} | Pages: {doc['page_count']}"
                    ):
                        st.session_state.current_pdf = doc['pdf_name']
                        st.rerun()
                
                with col2:
                    if st.button(
                        "🗑️",
                        key=f"delete_{doc['pdf_name']}",
                        help="Delete Document"
                    ):
                        if st.session_state.rag_engine.delete_pdf(doc['pdf_name']):
                            st.success("✅ Document deleted")
                            if st.session_state.current_pdf == doc['pdf_name']:
                                st.session_state.current_pdf = None
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete document")
                
                # Show document details
                st.caption(f"📅 {doc['upload_date'][:10]} | 📊 {doc['file_size']} | 📄 {doc['page_count']} pages | {file_type}")
                
    except Exception as e:
        st.error(f"❌ Error loading documents: {str(e)}")

def display_current_pdf_info():
    """Display information about currently selected document."""
    if not st.session_state.current_pdf:
        st.info("👆 Select a document from the list above")
        return
    
    try:
        docs = st.session_state.rag_engine.list_available_documents()
        current_doc_info = next(
            (doc for doc in docs if doc['pdf_name'] == st.session_state.current_pdf),
            None
        )
        
        if current_doc_info:
            st.markdown("### 📄 Current Document")
            file_type = current_doc_info.get('file_type', 'DOC')
            st.info(f"**{current_doc_info['filename']}** ({file_type})")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📄 Pages", current_doc_info['page_count'])
            with col2:
                st.metric("📊 Size", current_doc_info['file_size'])
            
            # Summary
            with st.expander("📝 Summary", expanded=False):
                summary = st.session_state.rag_engine.get_document_summary(
                    st.session_state.current_pdf
                )
                st.write(summary)
                
    except Exception as e:
        st.error(f"❌ Error loading document info: {str(e)}")

def update_settings():
    """Update application settings."""
    st.markdown("### ⚙️ Settings")
    
    # Temperature
    st.session_state.temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Controls randomness in responses"
    )
    
    # Max tokens
    st.session_state.max_tokens = st.slider(
        "📝 Max Tokens",
        min_value=100,
        max_value=1000,
        value=st.session_state.max_tokens,
        step=50,
        help="Maximum response length"
    )
    
    # Top K results
    st.session_state.top_k = st.slider(
        "🔍 Chunks to Retrieve",
        min_value=1,
        max_value=10,
        value=st.session_state.top_k,
        help="Number of relevant chunks to use"
    )

def clear_all_data():
    """Clear all application data with confirmation."""
    st.markdown("### 🗑️ Clear All Data")
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        if st.checkbox("⚠️ I understand this will delete all documents and chat history"):
            try:
                # Get all documents and delete them
                docs = st.session_state.rag_engine.list_available_documents()
                for doc in docs:
                    st.session_state.rag_engine.delete_pdf(doc['pdf_name'])
                
                # Reset session state
                st.session_state.current_pdf = None
                st.session_state.chat_history = []
                st.session_state.processing_status = None
                
                st.success("✅ All data cleared successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error clearing data: {str(e)}")

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    initialize_components()
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 📁 Document Management")
        
        # Section 1: File Upload
        st.markdown("### 📤 Upload Document")
        # File uploader with multiple formats
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=["pdf", "txt", "md", "docx"],
            help="Supported: PDF, TXT, MD, DOCX (max 50MB)"
        )
        
        if uploaded_file and st.button("🚀 Process Document"):
            handle_document_upload(uploaded_file)
        
        st.divider()
        
        # Section 2: Available Documents
        st.markdown("### 📚 Available Documents")
        display_pdf_list()
        
        st.divider()
        
        # Section 3: Current Document Info
        display_current_pdf_info()
        
        st.divider()
        
        # Section 4: Settings
        update_settings()
        
        st.divider()
        
        # Clear all data
        clear_all_data()
    
    # Main content area
    st.markdown('<h1 class="main-header">📄 Smart Document Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Chat with your documents using AI</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if PDF is selected
    if not st.session_state.current_pdf:
        display_welcome_screen()
    else:
        display_chat_interface()

if __name__ == "__main__":
    main()
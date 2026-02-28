# 🤖 Lumina-PDF-Bot

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-121011?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

> **Transform your PDF documents into interactive AI conversations.** Lumina-PDF-Bot uses state-of-the-art **RAG (Retrieval-Augmented Generation)** to provide accurate, context-aware answers from your files in milliseconds.

---

## 🌟 Key Features

- ⚡ **Lightning Fast Responses**: Powered by **Groq API** for sub-second inference.
- 📂 **Multi-Format Support**: Chat with PDF, DOCX, TXT, and Markdown files.
- 🧠 **Smart Context Retrieval**: Uses advanced vector embeddings to find the exact information you need.
- 💬 **Persistent History**: Built-in chat management to keep track of your conversations.
- 📁 **Modular Architecture**: Professional folder structure designed for scalability and maintainability.
- 🔌 **Cloud LLM Support**: Easily switch between **Groq**, **OpenAI**, and **OpenRouter**.
- 🔋 **Lightweight Embeddings**: Optimized TF-IDF fallback for low-resource environments.

---

## 🏗️ Project Architecture

```text
pdf_chatbot/
├── data/                       # 🏠 Storage for PDFs and Vector DB
├── src/                        # 🚀 Main Source Code
│   ├── api/                    # 🎨 Streamlit UI & Application Logic
│   ├── core/                   # ⚙️ Global Configuration & Constants
│   ├── engine/                 # 🧠 RAG Pipeline & Vector Store
│   ├── handlers/               # 🔌 External API Connectors (LLMs)
│   ├── services/               # 🛠️ Business Logic & History Management
│   └── utils/                  # 🔧 Shared Utility Functions
└── scripts/                    # 📜 Maintenance & Setup Scripts
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Iamzain804/Lumina-PDF-Bot.git
cd Lumina-PDF-Bot
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openrouter  # choice: groq, openai, openrouter
```

### 3. Run the App
```bash
streamlit run src/api/app.py
```

---

## 🛠️ How It Works (RAG Pipeline)

1.  **Ingestion**: Documents are split into optimized chunks using **LangChain**.
2.  **Indexing**: Chunks are converted into mathematical vectors (Embeddings) and stored in a local **Vector Store**.
3.  **Retrieval**: When you ask a question, the system searches the index for the most relevant context.
4.  **Generation**: The context + question are sent to the LLM to generate a precise, cited answer.

---

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request to improve Lumina-PDF-Bot.

## 📄 License
This project is licensed under the MIT License.

---
<p align="center">
  Made with ❤️ for the AI Community
</p>
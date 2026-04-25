# 📄 PDF FAQ RAG Chatbot

An AI-powered PDF Question Answering application built using **Retrieval-Augmented Generation (RAG)**.  
This app reads PDF documents, creates embeddings, and answers user queries with accurate, context-based responses.

---

## 🚀 Features

- 📄 Upload & process PDF documents
- 🔍 Semantic search using FAISS
- 🤖 AI-powered answers using OpenAI
- ⚡ Fast retrieval with vector database
- 📚 Source-based answers
- 🎯 Context-aware responses
- 💬 Interactive UI with Streamlit

---

## 🧠 Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **FAISS (Vector Database)**
- **OpenAI (LLM + Embeddings)**

---

## 📂 Project Structure
pdf_faq_bot/
│
├── app.py # Streamlit UI
├── rag.py # RAG pipeline logic
├── data/ # PDF files
├── .gitignore
└── requirements.txt


---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/kowsalya/pdf-faq-rag-app.git
cd pdf-faq-rag-app

pip install -r requirements.txt
OPENAI_API_KEY=your_api_key_here
streamlit run app.py

import streamlit as st
import os

from rag import (
    load_pdf,
    split_docs,
    create_vectorstore,
    save_vectorstore,
    load_vectorstore,
    get_llm
)

st.set_page_config(page_title="PDF FAQ Bot", layout="wide")

# Session state for caching answers
if "history" not in st.session_state:
    st.session_state.history = {}

# 🎨 UI styling
st.markdown("""
<style>
.answer-box {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 PDF FAQ Bot (Optimized)")
st.caption("Accurate answers from your PDF ⚡")

# 📂 Sidebar Questions
with st.sidebar:
    st.header("📘 Sample Questions")

    st.subheader("🔧 Tech Stack")
    for q in [
        "What frontend technologies are used?",
        "What backend technologies are used?",
        "What databases are used?",
        "What is Redis used for?",
        "What is ClickHouse used for?"
    ]:
        if st.button(q):
            st.session_state["question"] = q

    st.subheader("🧠 Microservices")
    for q in [
        "List all microservices in the system",
        "What does API Gateway do?",
        "What is the role of Auth Service?",
        "Explain Catalog Service",
        "What does Recommendation Service do?"
    ]:
        if st.button(q):
            st.session_state["question"] = q

    st.subheader("🗂️ Data")
    for q in [
        "What is stored in PostgreSQL?",
        "What is stored in Redis?",
        "What is Elasticsearch used for?"
    ]:
        if st.button(q):
            st.session_state["question"] = q

# 📄 PDF path
pdf_path = "data/sample.pdf"

if not os.path.exists(pdf_path):
    st.error("❌ PDF not found")
    st.stop()

# ⚡ Load or create FAISS
if os.path.exists("faiss_index"):
    vectorstore = load_vectorstore()
    st.success("⚡ Fast mode enabled")
else:
    with st.spinner("Processing PDF..."):
        docs = load_pdf(pdf_path)
        chunks = split_docs(docs)
        vectorstore = create_vectorstore(chunks)
        save_vectorstore(vectorstore)
    st.success("✅ Index created")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = get_llm()

# 💬 Input
query = st.text_input(
    "Ask your question:",
    value=st.session_state.get("question", "")
)

# 🤖 Answer
if query:
    st.info("🔍 Searching document...")

    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # ❌ Safety check
    if not docs or len(context.strip()) < 50:
        st.write("❌ Not in document")
        st.stop()

    # 🔁 Cache check
    if query in st.session_state.history:
        response_text = st.session_state.history[query]
    else:
        prompt = f"""
You are a strict assistant.

Answer ONLY using the provided context.
If the answer is not clearly found in the context, respond EXACTLY with:
"Not in document"

Do NOT guess.
Do NOT add external knowledge.

Context:
{context}

Question:
{query}
"""
        response = llm.invoke(prompt)
        response_text = response.content
        st.session_state.history[query] = response_text

    # ✅ Answer
    st.markdown("### ✅ Answer")
    st.markdown(f"<div class='answer-box'>{response_text}</div>", unsafe_allow_html=True)

    # 📌 Sources
    with st.expander("📌 Show Sources"):
        for i, doc in enumerate(docs):
            st.write(f"**Source {i+1}:**")
            st.write(doc.page_content[:300])
            st.write("---")
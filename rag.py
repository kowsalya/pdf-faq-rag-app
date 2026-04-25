from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

load_dotenv()


def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()


def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)


def save_vectorstore(vectorstore):
    vectorstore.save_local("faiss_index")


def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )


def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
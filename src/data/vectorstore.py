import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

os.makedirs("phone_index", exist_ok=True)

# Global BGE embeddings (used by both functions)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

def create_vectorstore(docs):
    """Persistent FAISS store for smartphones."""
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("phone_index")
    return vectorstore

def load_vectorstore():
    """Load existing index."""
    return FAISS.load_local("phone_index", embeddings, allow_dangerous_deserialization=True)
import sys
import os
# 🔥 FIX: Add src/ to path (solves ALL module errors)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from dotenv import load_dotenv
from data.loader import load_docs
from data.vectorstore import create_vectorstore
from tools.retrieve import retrieve_context
from agents.rag_agent import PhoneRAGAgent

# Load environment
load_dotenv()

# Global agent (singleton - created once)
_agent = None
_vectorstore = None

def initialize_agent():
    """Initialize agent once (called by Streamlit/local)"""
    global _agent, _vectorstore
    
    if _agent is None:
        print("📱 Indexing 5000+ Indian smartphones...")
        docs = load_docs()
        _vectorstore = create_vectorstore(docs)
        _agent = PhoneRAGAgent(_vectorstore)
        print("✅ Agent ready with BGE + FAISS!")
    
    return _agent

def get_agent():
    """Streamlit calls this - returns ready agent"""
    return initialize_agent()

def ask_phone(query: str):
    """Main query endpoint - returns structured result"""
    agent = get_agent()
    result = agent.invoke(query)
    
    return {
        "content": result["content"],
        "memory_turns": result["memory_turns"],
        "success": True
    }

def get_status():
    """Health check endpoint"""
    agent = get_agent()
    return {
        "status": "healthy",
        "memory_turns": len(agent.memory.memory),
        "model": "Groq gpt-oss-120b"
    }

# Local demo (unchanged functionality)
# if __name__ == "__main__":
#     agent = initialize_agent()
#     queries = [
#         "Best camera phone under 30k?",
#         "Compare that with Poco X7 Pro", 
#         "Gaming phone 50k budget"
#     ]
    
#     print("\n🚀 Indian Smartphone Agent Ready!\n")
#     for query in queries:
#         result = ask_phone(query)
#         print(f"\n🔥 Q: {query}")
#         print(f"🤖 A: {result['content'][:300]}...")
#         print(f"💾 Memory: {result['memory_turns']} turns")
#         print("-" * 80)

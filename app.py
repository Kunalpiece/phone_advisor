import streamlit as st
import importlib.util
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import main logic dynamically
spec = importlib.util.spec_from_file_location("main", "src/main.py")
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

# Page config & Custom CSS
st.set_page_config(page_title="📱 Phone Agent Pro", page_icon="📱", layout="wide")

st.markdown("""
<style>
.agent-header {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;}
.price-highlight {font-size: 1.4rem; color: #fff; font-weight: bold;}
.recommendation-card {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 12px;}
.trend-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 12px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="agent-header">
    <h1>🤖 Phone Agent Pro</h1>
    <p>AI-Powered Smartphone Recommendations | March 2026 India Market</p>
</div>
""", unsafe_allow_html=True)

# Initialize agent (cached)
@st.cache_resource
def get_agent():
    return main_module.get_agent()

agent = get_agent()

# Unified query processor
def process_query(query_string):
    with st.spinner("AI is analyzing data..."):
        result = main_module.ask_phone(query_string)
        st.session_state.current_result = result
        st.rerun()

# --- SIDEBAR (Consolidated Metrics & Controls) ---
with st.sidebar:
    st.markdown("### 🤖 Agent Settings")
    st.caption("**Status:** 🟢 Live")
    
    if st.button("🗑️ Clear Memory", use_container_width=True):
        agent.memory.memory =[]
        if "current_result" in st.session_state:
            del st.session_state.current_result
        st.rerun()
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_resource.clear()
        st.success("Data refreshed!")
    
    st.markdown("---")
    st.markdown("**📈 System Stats**")
    st.metric("Memory Depth", f"{len(agent.memory.memory)} turns")
    st.metric("Phones Indexed", "5,247")
    
    st.markdown("---")
    st.markdown("**Powered by:**\n- Groq gpt-oss-120b\n- BGE Embeddings\n- FAISS Vector DB")

# --- TOP SEARCH & UNIFIED RESULT DISPLAY ---
col1, col2 = st.columns([4, 1])
with col1:
    quick_query = st.text_input("🔍 Quick search", placeholder="e.g. Best camera phone under 30k...", label_visibility="collapsed")
with col2:
    if st.button("🚀 Analyze", use_container_width=True) and quick_query:
        process_query(quick_query)

if "current_result" in st.session_state:
    result = st.session_state.current_result
    st.markdown("### 🎯 AI Verdict")
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="price-highlight">{result['content']}</div>
        <br>
        <small><i>Memory Used: {result.get('memory_turns', len(agent.memory.memory))} turns</i></small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- ADVANCED TOOLS (Consolidated Tabs) ---
st.markdown("### 🎛️ Advanced Agent Tools")
tab1, tab2, tab3 = st.tabs(["🎯 Smart Finder", "⚖️ Compare Phones", "💸 Live Price Radar"])

# Merged redundancy: Removed duplicate budget sliders/category dropdowns
with tab1:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        budget = st.slider("💰 Budget", 10000, 100000, 30000, 5000)
    with col2:
        category = st.selectbox("🎯 Priority", ["Camera", "Gaming", "Battery", "Value", "Display"])
    with col3:
        st.write("") # Vertical alignment
        if st.button("Find Best Match", use_container_width=True, type="primary"):
            process_query(f"Best {category.lower()} phone under ₹{budget:,} India 2026")

with tab2:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        phone1 = st.text_input("Phone 1", "iPhone 16")
    with col2:
        phone2 = st.text_input("Phone 2", "Samsung S26")
    with col3:
        st.write("") 
        if st.button("⚖️ Compare", use_container_width=True):
            process_query(f"Compare {phone1} vs {phone2} price specs India")

with tab3:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        phone_name = st.text_input("Phone Name", "Nothing Phone 3a")
    with col2:
        store = st.selectbox("Store", ["Flipkart", "Amazon", "Croma"])
    with col3:
        st.write("")
        if st.button("💰 Check Price", use_container_width=True):
            process_query(f"{phone_name} current price {store} India March 2026")

# --- HOT TRENDS CAROUSEL ---
st.markdown("---")
st.markdown("**🏆 Hot Phones Right Now**")
trends = st.columns(4)
hot_phones =[
    ("📸 Nothing Phone 3a", "₹26,999", "Best Camera <30k"),
    ("⚡ Poco X7 Pro", "₹28,999", "Gaming Beast"),
    ("🔋 Samsung M56", "₹22,999", "Battery King"),
    ("⭐ iQOO 13", "₹49,999", "Flagship Killer")
]

for i, (name, price, tag) in enumerate(hot_phones):
    with trends[i]:
        st.markdown(f"""
        <div class="trend-card">
            <b style='font-size: 1.1rem;'>{name}</b><br>
            <span style='font-size: 1.3rem; color: #10b981;'>{price}</span><br>
            <small>{tag}</small>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    🚀 Professional AI Agent | Built for India Market | March 2026
</div>
""", unsafe_allow_html=True)
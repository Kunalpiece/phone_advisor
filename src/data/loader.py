import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PHONE_SOURCES_2026 = [
    "https://www.gizbot.com/top-10-mobiles/",  # Top 10 list [web:59]
    "https://www.smartprix.com/mobiles",       # Full specs/prices [web:66]
    "https://www.croma.com/unboxed/best-android-phones-in-india-2026-top-10-picks-for-every-budget",  # Reviews [web:58]
    "https://www.cashify.in/compare-mobile-phones",  # Comparisons [web:64]
    "https://www.reuz.in/articles/best-new-smartphones-2026-rankings-ai-scores-resale-value"  # Rankings [web:62]
]

def load_docs():
    """Load Indian smartphone data: specs, prices, reviews."""
    all_docs = []
    for url in PHONE_SOURCES_2026:
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs={"parse_only": bs4.SoupStrainer(class_=("post-content", "table", "spec", "price"))}
        )
        docs = loader.load()
        all_docs.extend(docs)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    return splitter.split_documents(all_docs)

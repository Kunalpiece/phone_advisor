from langchain_core.tools import tool

@tool
def retrieve_context(query: str, vectorstore) -> str:
    """Search smartphones by name, budget, specs. Gets prices, reviews, comparisons."""
    docs = vectorstore.similarity_search(query + " India price specs review discount", k=5)
    results = []
    for i, doc in enumerate(docs, 1):
        results.append(f"{i}. {doc.page_content[:400]}...\nSource: {doc.metadata.get('source', 'N/A')}")
    return "\n\n".join(results)

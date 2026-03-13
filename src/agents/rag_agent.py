import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tools.retrieve import retrieve_context

class SmartMemory:
    """Production-grade memory: fixed size + persistent + efficient"""
    
    def __init__(self, max_turns=6, filename="phone_memory.json"):
        self.max_turns = max_turns
        self.filename = filename
        self.memory = self._load()
    
    def _load(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.memory, f)
    
    def add(self, user_query, ai_response):
        turn = {"user": user_query, "ai": ai_response[:300] + "..."}
        self.memory.append(turn)
        if len(self.memory) > self.max_turns:
            self.memory = self.memory[-self.max_turns:]
        self._save()
    
    def get_summary(self):
        if not self.memory:
            return "No previous conversation."
        recent = self.memory[-3:]
        return f"Past topics: {', '.join([t['user'][:50] for t in recent])}"

class PhoneRAGAgent:
    """Complete RAG agent with memory + retrieval"""
    
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)  # ✅ FIXED
        
        self.prompt = ChatPromptTemplate.from_template("""
Smartphone expert - India March 2026.

CONTEXT: {context}
HISTORY SUMMARY: {history}
QUESTION: {question}

Answer: ₹prices, specs, offers, pros/cons
""")
        
        self.memory = SmartMemory()
        self.chain = self.prompt | self.model
    
    # def invoke(self, query):
    #     # Retrieve
    #     context = retrieve_context.invoke({
    #         "query": query, 
    #         "vectorstore": self.vectorstore
    #     })
        
    #     # Memory
    #     history_summary = self.memory.get_summary()
        
    #     # Generate
    #     response = self.chain.invoke({
    #         "context": context,
    #         "history": history_summary,
    #         "question": query
    #     })
        
    #     # Save to memory
    #     self.memory.add(query, response.content)
        
    #     return {
    #         "content": response.content,
    #         "memory_turns": len(self.memory.memory)
    #     }
    
    def invoke(self, query):
        context = retrieve_context.invoke({"query": query, "vectorstore": self.vectorstore})
        history_summary = self.memory.get_summary()
        
        # JSON schema prompt
        json_prompt = ChatPromptTemplate.from_template("""
        Return ONLY valid JSON (no other text):
        
        CONTEXT: {context}
        HISTORY: {history}
        QUESTION: {question}
        
        Respond in this EXACT format:
        {{
        "recommendations": [{{"name": "...", "price": "₹...", "pros": [], "cons": []}}],
        "summary": "...",
        "best_pick": "...",
        "offers": "..."
        }}
        """)
        
        chain = json_prompt | self.model
        json_response = chain.invoke({"context": context, "history": history_summary, "question": query})
        
        # Parse JSON
        try:
            data = json.loads(json_response.content)
            formatted = self._format_pretty(data, query)  # Pretty print
        except:
            formatted = json_response.content  # Fallback
        
        self.memory.add(query, formatted)
        return {"content": formatted, "memory_turns": len(self.memory.memory)}

    def _format_pretty(self, data, query):
        if "recommendations" in data:
            md = f"**📱 {query.upper()}**\n\n"
            for phone in data["recommendations"][:3]:
                md += f"**{phone['name']}** - {phone['price']}\n"
                md += f"• Camera: {phone.get('camera', 'N/A')}\n"
                md += f"• Pros: {', '.join(phone['pros'])}\n\n"
            md += f"\n**🎯 Best Pick:** {data.get('best_pick', 'N/A')}"
            return md
        return str(data)

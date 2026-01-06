import os
import re # Added regex for cleaning
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import PromptTemplate
from neo4j import GraphDatabase

# --- CONFIGURATION ---
NEO4J_URI = "bolt://graph-db:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "veritas_password"
OLLAMA_URL = "http://llm-server:11434"

CHAT_MODEL = "gemma3"
EMBEDDING_MODEL = "nomic-embed-text"

app = FastAPI(title="Veritas RAG Agent")

class QueryRequest(BaseModel):
    query: str

# --- 1. SETUP GRAPH CONNECTION ---
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def query_graph_context(query_text):
    """
    Retrieves related entities from Neo4j with cleaned keywords.
    """
    # 1. Clean the query (remove punctuation, make lowercase)
    clean_text = re.sub(r'[^\w\s]', '', query_text).lower()
    
    # 2. Extract significant words (skip 'what', 'is', 'the')
    stop_words = {'what', 'is', 'the', 'of', 'in', 'a', 'an', 'to'}
    words = [w for w in clean_text.split() if w not in stop_words]
    
    # 3. Pick the longest remaining word as the anchor
    keyword = max(words, key=len) if words else "transformer"
    
    print(f"🕸️ Graph Searching for keyword: '{keyword}'")

    cypher_query = """
    MATCH (c:Chunk)
    WHERE toLower(c.text) CONTAINS $keyword
    RETURN c.text AS text LIMIT 2
    """
    
    with driver.session() as session:
        result = session.run(cypher_query, keyword=keyword)
        return [record["text"] for record in result]

# --- 2. SETUP VECTOR CONNECTION ---
embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory="/app/chroma_db_local", 
    embedding_function=embeddings,
    collection_name="veritas_knowledge"
)

llm = ChatOllama(base_url=OLLAMA_URL, model=CHAT_MODEL)

@app.post("/ask")
def ask(request: QueryRequest):
    print(f"🧠 Thinking about: {request.query}")
    
    # A. Get Vector Context (Increase k to see more pages)
    docs = vectorstore.similarity_search(request.query, k=3)
    vector_context = "\n---\n".join([d.page_content for d in docs])
    
    # B. Get Graph Context
    graph_data = query_graph_context(request.query)
    graph_context = "\n---\n".join(graph_data)
    
    # C. Synthesize Answer (Better System Prompt)
    prompt = f"""
    You are a Research Assistant analyzing a technical document.
    
    [CONTEXT FROM DATABASE]:
    {vector_context}
    
    [ADDITIONAL CONTEXT]:
    {graph_context}
    
    USER QUESTION: {request.query}
    
    INSTRUCTIONS:
    1. Answer the question based ONLY on the provided context.
    2. If the context contains multiple topics, summarize the main one.
    3. Do not mention "American governments" unless the user asks about voting.
    
    YOUR ANSWER:
    """
    
    response = llm.invoke(prompt)
    
    return {
        "answer": response.content,
        "sources": {
            "vector_chunks": len(docs),
            "graph_nodes": len(graph_data),
            "keyword_used": "See logs"
        }
    }
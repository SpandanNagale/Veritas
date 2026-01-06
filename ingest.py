import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from neo4j import GraphDatabase

# 1. Configuration (Matching your Docker Setup)
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "veritas_password"
CHROMA_PATH = "./chroma_db_local" # Local path for script access

# 2. Connect to Databases
print("🔌 Connecting to Neo4j...")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

print("🔌 Connecting to Ollama (Embedding Model)...")
# We use Llama3 itself or nomic-embed-text for embeddings. 
# For simplicity, we use Llama3, though a specialized embed model is better.
embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")

# 3. The "Graph" Extraction Logic
def extract_entities_to_graph(text_chunk, chunk_id):
    """
    This is the Secret Sauce. Instead of just saving text, we ask LLM to 
    identify concepts and insert them into Neo4j.
    """
    # Simple Cypher query to create a node for the Chunk
    with driver.session() as session:
        session.run(
            """
            MERGE (c:Chunk {id: $chunk_id})
            SET c.text = $text
            """,
            chunk_id=chunk_id, text=text_chunk
        )
    print(f"   └── 🕸️  Indexed Chunk {chunk_id} in Graph")

# 4. Main Pipeline
def run_pipeline(pdf_path):
    print(f"📂 Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"✂️  Split into {len(splits)} chunks.")

    # A. Vector Store Ingestion (The Standard Way)
    print("💾 Ingesting into Vector DB (Chroma)...")
    # We use a persistent client directly to avoid Docker path issues from host script
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        collection_name="veritas_knowledge",
        persist_directory=CHROMA_PATH
    )
    print("   └── ✅ Vector Data Saved.")

    # B. Graph Ingestion (The "Veritas" Way)
    print("🧠 Ingesting into Graph DB (Neo4j)...")
    for i, split in enumerate(splits):
        extract_entities_to_graph(split.page_content, f"chunk_{i}")
    
    print("🚀 Ingestion Complete!")
    driver.close()

if __name__ == "__main__":
    import os
    
    file_name = "manual.pdf"
    
    if os.path.exists(file_name):
        print(f"🔥 Found {file_name}! Starting ingestion process...")
        try:
            run_pipeline(file_name)
        except Exception as e:
            print(f"❌ Error during ingestion: {e}")
    else:
        print(f"⚠️ Could not find '{file_name}'. Please check the file name is exact.")
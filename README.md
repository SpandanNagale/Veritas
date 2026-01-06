# 🛡️ Veritas: Local High-Performance GraphRAG Engine

![Status](https://img.shields.io/badge/Status-Operational-brightgreen)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Local-blue)
![Hardware](https://img.shields.io/badge/Hardware-RTX_5070_Optimized-76B900)

**Veritas** is a privacy-first, self-hosted Retrieval-Augmented Generation (RAG) agent that combines **Vector Semantic Search** with **Knowledge Graph Traversal** to deliver highly accurate, context-aware answers from technical documents.

Unlike standard RAG implementations that rely on flat text chunks, Veritas constructs a local knowledge graph to understand the *relationships* between entities, reducing hallucination rates for complex technical queries. The entire pipeline runs locally on consumer hardware via Docker, ensuring zero data leakage.

## ⚡ Key Features

* **Hybrid Retrieval Architecture**: Simultaneously queries **ChromaDB** (Vector) for semantic nuance and **Neo4j** (Graph) for structural relationships.
* **Privacy-First & Offline**: 100% local execution using **Ollama**. No OpenAI keys, no cloud data transfer.
* **Hardware Accelerated**: Optimized Docker GPU passthrough for NVIDIA RTX 5070, achieving sub-second inference latencies with quantized LLMs.
* **Asynchronous API**: Built on **FastAPI** with async architecture to handle ingestion and retrieval concurrently.
* **Interactive UI**: Streamlit-based frontend for real-time document interrogation and system introspection.

## 🏗️ Tech Stack

* **LLM Engine**: [Ollama](https://ollama.com/) (Running Gemma-2-2b / Llama 3)
* **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Semantic Memory)
* **Graph Database**: [Neo4j](https://neo4j.com/) (Structural Memory)
* **Backend**: Python, FastAPI, LangChain
* **Frontend**: Streamlit
* **Infrastructure**: Docker Compose (Container Orchestration)

---

## 🚀 Architecture Overview

```mermaid
graph TD
    User[User Query] --> UI[Streamlit UI]
    UI --> API[FastAPI Backend]
    
    subgraph "The Brain (Docker Network)"
        API -->|Semantic Search| VectorDB[ChromaDB]
        API -->|Entity Search| GraphDB[Neo4j]
        API -->|Synthesis| LLM[Ollama Service]
        
        VectorDB -->|Context| LLM
        GraphDB -->|Relationships| LLM
    end
    
    LLM -->|Final Answer| UI

🛠️ Prerequisites
OS: Windows 10/11 (WSL2), Linux, or MacOS.

Docker Desktop: Installed and running.

GPU (Recommended): NVIDIA GPU with at least 8GB VRAM (Tested on RTX 5070 12GB).

Python: 3.10+

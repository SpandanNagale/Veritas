# 🛡️ Veritas: Local High-Performance GraphRAG Engine

**Veritas** is a privacy-first, self-hosted Retrieval-Augmented Generation (RAG) agent that combines **Vector Semantic Search** with **Knowledge Graph Traversal** to deliver highly accurate, context-aware answers from technical documents.

Unlike standard RAG implementations that rely on flat text chunks, Veritas constructs a local knowledge graph to understand the *relationships* between entities, significantly reducing hallucination rates for complex technical queries. The entire pipeline runs locally on consumer hardware via Docker, ensuring zero data leakage.

## ⚡ Key Features

* **Hybrid Retrieval Architecture**: Simultaneously queries **ChromaDB** (Vector) for semantic nuance and **Neo4j** (Graph) for structural relationships.
* **Privacy-First & Offline**: 100% local execution using **Ollama**. No OpenAI keys, no cloud data transfer.
* **Hardware Accelerated**: Optimized Docker GPU passthrough for NVIDIA **RTX 5070**, achieving sub-second inference latencies with quantized LLMs.
* **Asynchronous API**: Built on **FastAPI** with an async architecture to handle ingestion and retrieval concurrently.
* **Interactive UI**: Streamlit-based frontend for real-time document interrogation and system introspection.

## 🏗️ Tech Stack

* **LLM Engine**: [Ollama](https://ollama.com/) (Running Gemma-2-2b / Llama 3)
* **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Semantic Memory)
* **Graph Database**: [Neo4j](https://neo4j.com/) (Structural Memory)
* **Backend**: Python, FastAPI, LangChain
* **Frontend**: Streamlit
* **Infrastructure**: Docker Compose (Container Orchestration)

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* NVIDIA Container Toolkit (for GPU acceleration)
* Python 3.10+ (for local development)

### Quick Start (Docker)

1. **Clone the repository:**
```bash
git clone https://github.com/SpandanNagale/Veritas.git
cd Veritas

```


2. **Configure Environment:**
Create a `.env` file in the root directory:
```env
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
OLLAMA_BASE_URL=http://ollama:11434

```


3. **Launch the stack:**
```bash
docker-compose up -d

```


4. **Access the Application:**
* **Frontend UI**: `http://localhost:8501`
* **API Docs (Swagger)**: `http://localhost:8000/docs`



---

## 📂 Project Structure

```text
├── main.py            # FastAPI Application Entrypoint
├── ingest.py          # Document processing & Graph/Vector ingestion logic
├── frontend.py        # Streamlit UI implementation
├── test_agent.py      # Unit testing for RAG chains
├── Dockerfile         # Multi-stage build for the API
├── docker-compose.yml # Full-stack orchestration (Neo4j, Chroma, Ollama, API)
└── README.md          # Documentation

```

## 🛠️ Performance Optimization

This project is specifically tuned for the **Black Anvil** workstation (Ryzen 7 9800X3D + RTX 5070).

* **GPU Passthrough**: The `docker-compose.yml` is configured to utilize `nvidia-container-runtime`.
* **Quantization**: Defaults to 4-bit/8-bit quantized weights via Ollama to maximize VRAM efficiency while maintaining logical reasoning capabilities.

---

## 🤝 Contributing

As an IT student focused on AI/ML, I welcome contributions that improve the entity extraction logic or graph traversal algorithms.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git checkout origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed by [Spandan Nagale**](https://www.google.com/search?q=https://github.com/SpandanNagale) *Building Local Intelligence, One Node at a Time.*

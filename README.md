# 🚀 Financial AI Agent: Real-time RAG & Analysis System

FastAPI와 Kafka를 활용한 실시간 금융 데이터 분석 및 RAG 기반 질의응답 시스템입니다.

## 🛠 Tech Stack
- **Backend:** Python, FastAPI
- **AI/LLM:** LangChain, OpenAI GPT-4o, Ollama (Local LLM)
- **Vector DB:** ChromaDB or pgvector
- **Event Streaming:** Apache Kafka (Redpanda)
- **Infrastructure:** Docker, Docker-compose

## 🏗 System Architecture
- [사용자] -> [Main Backend] -> [FastAPI AI Server] -> [Vector DB / LLM]
- [External API] -> [Kafka Producer] -> [Kafka] -> [AI Server Consumer]
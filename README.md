# Financial AI Agent: Real-time RAG & Analysis System & KAFA

이 프로젝트는 **실시간 암호화폐 시세 데이터**를 Kafka로 수집하고, 급격한 변동이 감지되면 **RAG(검색 증강 생성)** 기술을 활용해 **AI가 원인을 분석**하여 리포트를 제공하는 **지능형 금융 에이전트**입니다.

## Key Features

* **Real-time Data Pipeline**: Upbit WebSocket 데이터를 `Redpanda(Kafka)`를 통해 실시간으로 스트리밍 처리 (무손실 아키텍처).
* **Event-Driven Architecture**: FastAPI Consumer가 시세 변동을 감지(Anomaly Detection)하여 비동기적으로 AI 분석을 트리거.
* **RAG (Retrieval-Augmented Generation)**: `PostgreSQL` + `pgvector`에 저장된 금융 리포트를 기반으로 Gemini 1.5 Flash가 근거 있는 답변 생성.
* **Vector Database**: 3072차원 임베딩(`embedding-001`)을 활용한 유사도 검색.

##  Tech Stack
- **Backend:** Python, FastAPI
- **AI/LLM:** LangChain, GEMINI, GEMINI-embedding
- **Vector DB:** ChromaDB or pgvector
- **Infrastructure:** Docker, Docker-compose
- **Message Broker**: Redpanda (Kafka Compatible)
  
##  System Architecture
- [사용자] -> [Main Backend] -> [FastAPI AI Server] -> [Vector DB / LLM]
- [External API] -> [Kafka Producer] -> [Kafka] -> [AI Server Consumer]

##  Database Schema Design

본 프로젝트는 **PostgreSQL**과 **pgvector**를 사용하여 관계형 데이터와 벡터 데이터를 통합 관리합니다.

##  Architecture

1.  **Ingestion**: `market_producer.py`가 Upbit Websocket 데이터를 수집 → Kafka Topic(`market-prices`)으로 전송.
2.  **Detection**: FastAPI Server(`market_consumer.py`)가 Kafka 데이터를 구독 중 급변동 감지.
3.  **Retrieval**: `document_chunks` 테이블에서 관련 금융 지식/리포트 벡터 검색.
4.  **Generation**: 검색된 컨텍스트(Context)를 바탕으로 Gemini가 변동 원인 분석 리포트 생성.
---

### 1. `documents` (원본 문서 관리)
PDF 리포트나 뉴스 기사의 원본 메타데이터를 저장합니다.

| 필드명 | 타입 | 제약 조건 | 설명 |
|:---:|:---:|:---:|:---|
| **id** | `UUID` | **PK** | 문서 고유 식별자 |
| **title** | `VARCHAR` | NOT NULL | 문서 제목 (예: "2026 비트코인 전망 리포트") |
| **source_url** | `TEXT` | - | 원본 출처 및 참조 링크 |
| **doc_type** | `VARCHAR` | - | 유형 (PDF, NEWS, REPORT 등) |
| **created_at** | `TIMESTAMP` | DEFAULT | 데이터 수집 일시 |

---

### 2. `document_chunks` (벡터 데이터 저장)
RAG 구현을 위해 원본 문서를 조각낸 텍스트와 임베딩 벡터를 저장합니다.

| 필드명 | 타입 | 제약 조건 | 설명 |
|:---:|:---:|:---:|:---|
| **id** | `UUID` | **PK** | 청크 고유 식별자 |
| **document_id** | `UUID` | **FK** | `documents.id` 참조 |
| **content** | `TEXT` | NOT NULL | 쪼개진 텍스트 본문 |
| **embedding** | `VECTOR(3072)` | - | Gemini 임베딩 모델 기반 벡터 값 |
| **page_number** | `INTEGER` | - | (PDF의 경우) 해당 페이지 번호 |

---

### 3. `market_data` (실시간 시세 데이터)
Kafka를 통해 유입되는 실시간 금융 시세 정보를 저장합니다.

| 필드명 | 타입 | 제약 조건 | 설명 |
|:---:|:---:|:---:|:---|
| **symbol** | `VARCHAR` | **PK** | 자산 심볼 (예: BTC, ETH) |
| **price** | `NUMERIC` | NOT NULL | 현재 가격 |
| **change_rate** | `FLOAT` | - | 전일 대비 변동률 |
| **timestamp** | `TIMESTAMP` | - | 데이터 수신 및 기록 시간 |

---

### 4. `chat_history` (대화 이력 관리)
LLM의 Context 유지를 위해 사용자와의 대화 내역을 보관합니다.

| 필드명 | 타입 | 제약 조건 | 설명 |
|:---:|:---:|:---:|:---|
| **id** | `BIGSERIAL` | **PK** | 로그 고유 ID |
| **session_id** | `VARCHAR` | INDEX | 사용자 세션 구분값 |
| **role** | `VARCHAR` | - | 발화 주체 (user / assistant) |
| **message** | `TEXT` | NOT NULL | 대화 본문 내용 |
| **created_at** | `TIMESTAMP` | DEFAULT | 메시지 생성 일시 |

---
데이터 수집
<img width="907" height="293" alt="image" src="https://github.com/user-attachments/assets/8b435711-40cc-42b9-9e54-b6ca71a76617" />
---
AI 답변
<img width="1016" height="594" alt="image" src="https://github.com/user-attachments/assets/1a15a7c7-739f-4a8b-af38-bfa24b33b319" />


> **Design Decision:**
> - **Hybrid Search**: `pgvector`를 사용함으로써 SQL 기반의 메타데이터 필터링(예: 특정 날짜 이후의 리포트만 검색)과 벡터 유사도 검색을 동시에 수행할 수 있도록 설계했습니다.

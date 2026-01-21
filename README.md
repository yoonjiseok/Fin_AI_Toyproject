# Financial AI Agent: Real-time RAG & Analysis System

FastAPI와 Kafka를 활용한 실시간 금융 데이터 분석 및 RAG 기반 질의응답 시스템입니다.

## 🛠 Tech Stack
- **Backend:** Python, FastAPI
- **AI/LLM:** LangChain, OpenAI GPT-4o, Ollama (Local LLM)
- **Vector DB:** ChromaDB or pgvector
- **Event Streaming:** Apache Kafka (Redpanda)
- **Infrastructure:** Docker, Docker-compose

##  System Architecture
- [사용자] -> [Main Backend] -> [FastAPI AI Server] -> [Vector DB / LLM]
- [External API] -> [Kafka Producer] -> [Kafka] -> [AI Server Consumer]

## 🗄️ Database Schema Design

본 프로젝트는 **PostgreSQL**과 **pgvector**를 사용하여 관계형 데이터와 벡터 데이터를 통합 관리합니다.

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
| **embedding** | `VECTOR(768)` | - | Gemini 임베딩 모델 기반 벡터 값 |
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

> **Design Decision:**
> - **Hybrid Search**: `pgvector`를 사용함으로써 SQL 기반의 메타데이터 필터링(예: 특정 날짜 이후의 리포트만 검색)과 벡터 유사도 검색을 동시에 수행할 수 있도록 설계했습니다.

import uuid
from app.db.session import SessionLocal
from app.db.vector_db import embeddings
from app.models.db_models import Document, DocumentChunk


def ingest_text(text: str, title: str):
    db = SessionLocal()
    try:

        new_doc = Document(id=uuid.uuid4(), title=title, doc_type="TEXT")
        db.add(new_doc)
        db.flush()

        content_chunks = text.split("\n")

        for content in content_chunks:
            if not content.strip(): continue

            vector = embeddings.embed_query(content)

            new_chunk = DocumentChunk(
                document_id=new_doc.id,
                content=content,
                embedding=vector
            )
            db.add(new_chunk)

        db.commit()
        print(f"'{title}' 데이터 주입 성공")

    except Exception as e:
        db.rollback()
        print(f"데이터 주입 실패: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    with open("data/test_report.txt", "r", encoding="utf-8") as f:
        sample_text = f.read()
    ingest_text(sample_text, "2026 비트코인 전망")
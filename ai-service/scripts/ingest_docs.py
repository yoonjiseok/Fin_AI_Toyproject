import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db.session import SessionLocal
from app.db.vector_db import embeddings
from app.models.db_models import Document, DocumentChunk


def ingest_pdf(file_path: str, title: str):
    db = SessionLocal()
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(pages)

        new_doc = Document(id=uuid.uuid4(), title=title, doc_type="PDF")
        db.add(new_doc)
        db.flush()  # ID를 확정하기 위해 실행

        for chunk in chunks:
            vector = embeddings.embed_query(chunk.page_content)

            new_chunk = DocumentChunk(
                document_id=new_doc.id,
                content=chunk.page_content,
                embedding=vector
            )
            db.add(new_chunk)

        db.commit()
        print(f"Successfully ingested {len(chunks)} chunks from {title}")

    except Exception as e:
        db.rollback()
        print(f"Error during ingestion: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # 테스트용 샘플 실행 (data 폴더에 PDF가 있다고 가정)
    # ingest_pdf("data/sample_report.pdf", "Sample Finance Report")
    pass
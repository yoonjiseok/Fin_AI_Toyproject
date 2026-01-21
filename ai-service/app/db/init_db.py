from app.db.session import engine
from app.models.db_models import Base
from sqlalchemy import text

def init_db():
    with engine.connect() as conn:
        # 1. pgvector 확장 기능 활성화 (반드시 필요)
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
        print("pgvector extension enabled.")

    # 2. SQLAlchemy 모델을 기반으로 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    init_db()
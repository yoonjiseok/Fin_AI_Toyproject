from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
import os

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=settings.GOOGLE_API_KEY
)

CHROMA_DB_DIR = os.path.join(os.getcwd(), "data", "chroma_db")

def get_vector_db():
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name="fin_reports"
    )
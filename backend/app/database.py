import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "career_guidance.db")
raw_url = os.getenv("DATABASE_URL")
if not raw_url or raw_url in ("sqlite:///./career_guidance.db", "sqlite:///career_guidance.db"):
    DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"
else:
    DATABASE_URL = raw_url

# SQLAlchemy's default PostgreSQL driver is psycopg2. This project installs
# psycopg 3, so normalize provider URLs to the matching SQLAlchemy dialect.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# SQLite requires check_same_thread=False for multi-threaded FastAPI requests
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

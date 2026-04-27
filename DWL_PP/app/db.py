from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from config import DB_CONFIG # On importe ta configuration

# 1. On construit l'URL de connexion MySQL
# Note : il te faudra peut-être installer un driver comme pymysql (pip install pymysql)
DATABASE_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session():
    return SessionLocal()

def init_db():
    """Crée les tables dans la base de données si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)
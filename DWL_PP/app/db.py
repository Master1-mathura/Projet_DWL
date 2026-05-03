import os
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from config import DB_CONFIG # On importe ta configuration

# 1. On construit l'URL de connexion MySQL
# Note : il te faudra peut-être installer un driver comme pymysql (pip install pymysql)
if os.getenv("TESTING") == "1":
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, echo=False, connect_args={'check_same_thread': False})
else:
    # On intègre pymysql, le port, et on sécurise la connexion pour TiDB
    DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?ssl_verify_cert=true&ssl_verify_identity=true"
    engine = create_engine(DATABASE_URL, echo=True)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session():
    return SessionLocal()

def init_db():
    """Crée les tables dans la base de données si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)
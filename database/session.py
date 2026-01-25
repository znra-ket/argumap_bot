from config import DATABASE
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from .models import Base

engine = create_engine(
    DATABASE,
    echo=False,
    pool_pre_ping=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

def close_db():
    engine.dispose()
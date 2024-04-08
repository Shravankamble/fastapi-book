from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings as st

# postgresql://postgres:shravankamble@localhost/fastapi

SQLALCHEMY_DATABASE_URL = f'postgresql://{st.database_username}:{st.database_password}@{st.database_hostname}:{st.database_port}/{st.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
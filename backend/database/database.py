from sqlmodel import create_engine


sqlite_url = "sqlite:///./database/local.db"
engine = create_engine(sqlite_url, echo=False)

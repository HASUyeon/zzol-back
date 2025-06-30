import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

user = os.getenv("DB_USER")
passwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8'

engine = create_engine(DB_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session

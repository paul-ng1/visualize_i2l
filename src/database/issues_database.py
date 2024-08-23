from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from src.config import configs


def get_alchemy_url():
    return "postgresql://{username}:{password}@{host}:{port}/{db}".format(
        username=configs['db_issue']['username'],
        password=configs['db_issue']['password'],
        host=configs['db_issue']['host'],
        port=configs['db_issue']['port'],
        db=configs['db_issue']['db'])

engine = create_engine(
    get_alchemy_url(),
    pool_pre_ping=True
)

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)

Base = declarative_base()

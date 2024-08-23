from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import configs


tunnel = SSHTunnelForwarder(
    (configs['ssh']['host'], configs['ssh']['port']),
    ssh_username=configs['ssh']['user'],
    ssh_private_key=configs['ssh']['private_key'],
    remote_bind_address=(configs['db']['host'], configs['db']['port'])
)
tunnel.start()

def get_alchemy_url():
    return "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}".format(username=configs['db']['user'],
                                                                    password=configs['db']['password'],
                                                                    host='localhost',
                                                                    port=tunnel.local_bind_port,
                                                                    db=configs['db']['name'])

engine = create_engine(get_alchemy_url())

Session = sessionmaker(bind=engine)

Base = declarative_base()

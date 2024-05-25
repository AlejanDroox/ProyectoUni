"""Modulo que contiene el conector a la bd y mas nada"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnector:
    """Conector bd"""
    def __init__(self, config):
        self.engine = create_engine(config)
        session = sessionmaker(bind=self.engine)
        self.session = session()
# End-of-file

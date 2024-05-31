"""Modulo que contiene el conector a la bd y mas nada"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnector:
    """clase que crea y cierra la Conexion"""

    def __init__(self, config):
        self.engine = create_engine(config)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def close_session(self):
        """cierra la Conexion """
        if self.session:
            self.session.close()

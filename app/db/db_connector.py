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
    def reopen_session(self):
        """reabre la Conexion """
        if not self.session:
            session = sessionmaker(bind=self.engine)
            self.session = session()
class DbConnectorRV:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = None
        
    def get_session(self):
        if not self.session:
            self.session = self.SessionLocal()
        return self.session

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None

    def reopen_session(self):
        self.close_session()
        self.get_session()
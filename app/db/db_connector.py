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

    def get_session(self):
        return self.SessionLocal()
    
    def close_session(self):
        """cierra la Conexion """
        if self.SessionLocal:
            self.SessionLocal.close()
    def reopen_session(self):
        """reabre la Conexion """
        if not self.SessionLocal:
            SessionLocal = sessionmaker(bind=self.engine)
            self.SessionLocal = session()
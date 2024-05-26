from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnector:
    """clase que crea y cierra la contraseña"""

    def __init__(self, config):
        self.engine = create_engine(config)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def close_session(self):
        """cierra la contraseña"""
        if self.session:
            self.session.close()

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuariosMysqlalchemy'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    Rol= Column(String(45),nullable=False)

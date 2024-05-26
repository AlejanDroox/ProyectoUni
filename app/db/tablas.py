"""Modulo que contiene la estructura de todas las tablas"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Usuario(Base):
    """Tabla Usuarios.
    Nombre: usuariosMysqlalchemy
    Estructura de la tabla:
    *   id:int
    *   nombres:str(255)
    *   contrasena:str(255)
    *   rol: str(45)"""
    __tablename__ = 'usuariosMysqlalchemy'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    Rol= Column(String(45),nullable=False)
if __name__ == '__main__':
    h = Usuario()
    
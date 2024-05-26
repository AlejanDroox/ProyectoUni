"""Modulo que contiene la estructura de todas las tablas"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Usuario(Base):
    """creora/manipuladora de tabla users. Estructura de la tabla:
    idUsers:int
    Username:str(255)
    Password:str(255)
    Status: int"""
    __tablename__ = 'users'
    __tablename__ = 'usuariosMysqlalchemy'

    id = Column(Integer, primary_key=True)
    nombres = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    Rol= Column(String(45),nullable=False)

"""Modulo que encripta la contraseña"""
from math import perm
import bcrypt
from db.db_connector import DbConnector
from sqlalchemy import Null, create_engine, false
from sqlalchemy.ext.automap import automap_base
from utils.globals import CONFIG


# Crea el motor de SQLAlchemy
engine = create_engine(CONFIG)

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine)

# Accede a la clase de modelo correspondiente a la tabla 'Usuarios'
Usuario = Base.classes.users
usuario_creador=Usuario
username=""
PERMISOS = {
    'administrador': ['crear', 'leer', 'actualizar', 'eliminar'],
    'gerente': ['leer', 'actualizar'],
    'empleado': ['leer']
}

def __init__(self, db_connector):
        self.db_connector = db_connector

def verificar_permiso(rol_nombre, accion):
    return accion in PERMISOS.get(rol_nombre, [])

def encontrar_usuario(self, username):
    """busca usuario por nombre"""
    return self.db_connector.session.query(Usuario).filter_by(username=username).first()

#crear_admin
def crear_admin(usuario_creador):
    if usuario_creador=="administrador":
        print("ud es  administrador tiene permisos de todo")
        verificar_permiso('administrador','crear')
    elif usuario_creador == None :
        pass
    else: print("pobre pendejo sin jerarquia")
    return usuario_creador
        
    
# leer_admin
def leer_admin(usuario_creador):
    if usuario_creador=="administrador":
        print("ud es  administrador tiene permisos de todo")
        verificar_permiso('administrador','leer')
    elif usuario_creador == None :
        pass
    else: print("pobre pendejo sin jerarquia")
    return usuario_creador
# actualizar_admin
def actualizar_admin(usuario_creador):

    if usuario_creador=="administrador":
        print("ud es  administrador tiene permisos de todo")
        verificar_permiso('administrador','actualizar')
        
    elif usuario_creador == None :
       pass
    else: print("pobre pendejo sin jerarquia")
    return usuario_creador

def eliminar_admin(usuario_creador):
    if usuario_creador=="administrador"  :
        print("ud es  administrador tiene permisos de todo")
        verificar_permiso('administrador','eliminar')
    elif usuario_creador == None :
        pass
    else: 
        print("pobre pendejo sin jerarquia")

        
    return usuario_creador

# fin admin

def leer_gerente(usuario_creador):
    if usuario_creador=="gerente":
        print("ud es  gerente solo puede leer y actualizar a los que estan su mismo nivel o abajo")
        verificar_permiso('administrador','leer')
    elif usuario_creador == None :
        pass        
    elif usuario_creador == False :
        print("casi daniao")
    else: 
        print("pobre pendejo sin jerarquia")
    
# actualizar_gerente
def actualizar_gerente(usuario_creador):
    if usuario_creador=="gerente":
        print("ud es  gerente solo puede leer y actualizar a los que estan su mismo nivel o abajo")
        verificar_permiso('administrador','actualizar')
    elif usuario_creador == None :
       pass
    else: 
        print("pobre pendejo sin jerarquia")
    

def leer_empleado(usuario_creador):
    verificar_permiso('empleado','leer')
# fin empleado

# 
# # usuario_creador = control_usuarios.encontrar_usuario(username)


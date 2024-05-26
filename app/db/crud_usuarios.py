"""Modulo que encripta la contraseña"""
from math import perm
import bcrypt
from db_connector import DBConnector
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import permisos



# Crea el motor de SQLAlchemy
engine = create_engine(
    'mysql://root:1234@127.0.0.1:3306/dbferreteria')

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine, reflect=True)

# Accede a la clase de modelo correspondiente a la tabla 'Usuarios'
Usuario = Base.classes.users


class ControlUsuarios:
    """clase que maneja las operaciones de los usuarios"""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def encontrar_usuario(self, username):
        """busca usuario por nombre"""
        return self.db_connector.session.query(Usuario).filter_by(username=username).first()
    

# Inicio Create User
    def create_user(self, usuario_creador, username, password, rol_nombre):
        # Verificar si el usuario_creador puede crear un usuario
        if not permisos.crear_admin(usuario_creador.Rol):
            print("No tienes permisos para crear usuarios.")
            return False
        
        """crea un usuario"""
        usuario = self.encontrar_usuario(username)
        if not usuario:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())#yosnel que hace esta mierda desencripta o encripta
            nuevo_usuario = Usuario(username=username,
                              contrasena=hashed.decode('utf-8'),
                              Rol=rol_nombre)
            
            self.db_connector.session.add(nuevo_usuario)
            self.db_connector.session.commit()
            print("Usuario creado exitosamente.")
            return True
            
        else:
            print(f"El usuario '{username}' ya existe.")
            return False
# FIN CREATE USER

#incio imagino que esto es puro para el inicio de sesion
    def authenticate_user(self, username, password,):
        """confirma la contraseña"""
        usuario = self.encontrar_usuario(username)
        if usuario:
            if bcrypt.checkpw(password.encode('utf-8'), usuario.contrasena.encode('utf-8')):
                print("Usuario autenticado correctamente.")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print(f"El usuario '{username}' no fue encontrado")
            return False
#FIN AUTENTICACION
# Inicio reset password
    def reset_password(self,usuario_creador, username, new_password):
        if not permisos.actualizar_admin(usuario_creador) :
            
            """resetea la contraseña"""
            usuario = self.encontrar_usuario(username)
            if usuario:
                hashed = bcrypt.hashpw(
                    new_password.encode('utf-8'), bcrypt.gensalt())
                usuario.contraseña = hashed.decode('utf-8')
                self.db_connector.session.commit()
                print("Contraseña cambiada exitosamente.")
            else:
                
                print(f"El usuario '{username}' no fue encontrado")
            
        elif not  permisos.actualizar_gerente(usuario_creador):
            """resetea la contraseña"""
            usuario = self.encontrar_usuario(username)
            if usuario:
                hashed = bcrypt.hashpw(
                    new_password.encode('utf-8'), bcrypt.gensalt())
                usuario.contraseña = hashed.decode('utf-8')
                self.db_connector.session.commit()
                print("Contraseña cambiada exitosamente.")
            else:
                print(f"El usuario '{username}' no fue encontrado")
        else:
            print(usuario_creador)
            print("ud no tiene permiso cacocorro")
# FIN RESET PASSWORD

    def delete_user(self,usuario_creador, username):
        if not permisos.eliminar_admin(usuario_creador):
            """borra un usuario"""
            usuario = self.encontrar_usuario(username)
            if usuario:
                self.db_connector.session.delete(usuario)
                self.db_connector.session.commit()
                print(f"Usuario '{username}' fue borrado correctamente.")
            else:
                print(f"El usuario '{username}' no existe en la BD")
#termina crud usuarios 



# Configuración de la base de datos
CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
conexion = DBConnector(CONFIG)

Base.metadata.create_all(conexion.engine)

control_usuarios = ControlUsuarios(conexion)

print("prueba de  crear usuarios :")
username="azael"
password="1234"

usuario_creador = control_usuarios.encontrar_usuario(username)

control_usuarios.delete_user(usuario_creador,'nuevo_usuario4')

# control_usuarios.reset_password(usuario_creador,'nuevo_usuario', '1234')

# control_usuarios.create_user(usuario_creador, 'nuevo_usuario4', 'contraseña1234', 'empleado')

# Observacion   hay que hacer una autenticacion tambien para contrasenia ya que se pueden crear dos usuarios con contrasenias iguales

#observacion 2 no se que es esa vaina de deprecated yosnel chambee
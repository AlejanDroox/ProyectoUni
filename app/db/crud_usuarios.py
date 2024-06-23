"""Modulo que encripta la contraseña"""
from math import perm
from re import U
import bcrypt
from db.db_connector import DbConnector
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from db import permisos
from utils.globals import CONFIG


# Crea el motor de SQLAlchemy
engine = create_engine(CONFIG)

# Crea una instancia de automap_base
Base = automap_base()

# Refleja las tablas de la base de datos en los modelos de SQLAlchemy
Base.prepare(engine)

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
        if permisos.crear_admin(usuario_creador):
            print("No tienes permisos para crear usuarios.")
            #raise NotPermisos
            return False
        """crea un usuario"""
        usuario = self.encontrar_usuario(username)
        if not usuario:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #yosnel que hace esta mierda desencripta o encripta
            nuevo_usuario = Usuario(username=username,
                            contrasena=hashed.decode('utf-8'),
                            rol=rol_nombre)
            
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
        if  permisos.actualizar_admin(usuario_creador) :
            
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
            
        elif  permisos.actualizar_gerente(usuario_creador):
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

    # FIN RESET PASSWORD
    # inicio delete_user
    def delete_user(self,usuario_creador, username):
        if  permisos.eliminar_admin(usuario_creador):
            """borra un usuario"""
            usuario = self.encontrar_usuario(username)
            if usuario:
                self.db_connector.session.delete(usuario)
                self.db_connector.session.commit()
                print(f"Usuario '{username}' fue borrado correctamente.")
            else:
                print(f"El usuario '{username}' no existe en la BD")
    # fin del delete_user



        # editar status de usuario
       
    def edit_status_user(self,usuario_creador,username,status_nuevo):
        if   permisos.actualizar_admin(usuario_creador.status) :
                print("uwu")
                usuario = self.encontrar_usuario(username)
        
                if usuario.status !="administrador" or usuario.status !="gerente" or usuario.status !='empleado':
                    
                    
                    if  status_nuevo== 'administrador' or status_nuevo=='gerente' or status_nuevo=='empleado':
                        usuario.status= status_nuevo
                        self.db_connector.session.commit()
                        print(f"el status fue cambiado a {status_nuevo}")
                
                
                elif status_nuevo!= 'administrador' or status_nuevo!='gerente' or status_nuevo!='empleado':
                    
                    print("como vas a escribir mal imbecil")
                
                    
               
  # actualizar gerente

            
              
        if  permisos.actualizar_gerente(usuario_creador.status) :
            
                print(permisos.actualizar_gerente(usuario_creador))
                print(usuario_creador.status)
                usuario = self.encontrar_usuario(username)
                if usuario.status =="administrador":
                    print("ud no puede editar a un administrador")
                    
                elif usuario.status !="administrador" or usuario.status !="gerente" or usuario.status !='empleado':
                    
                    if status_nuevo=='administrador':
                        print( "no puedes volver a alguien administrador eres gerente")
                        
                    elif  status_nuevo== 'administrador' or status_nuevo=='gerente' or status_nuevo=='empleado':
                            usuario.status= status_nuevo
                            self.db_connector.session.commit()
                            print(f"el status fue cambiado a {status_nuevo}")
                
                
                    elif status_nuevo!= 'administrador' or status_nuevo!='gerente' or status_nuevo!='empleado':
                    
                            print("como vas a escribir mal imbecil")
                
                  
        else:("usuario no encontrado")
    
    # fin editar status usuarios
    
    
    
    
    # inicio editar rol
    def edit_rol_user(self,usuario_creador,username,rol_nuevo):
            
        if   permisos.actualizar_admin(usuario_creador)=="administrador" :
                print("uwu")
                usuario = self.encontrar_usuario(username)
        
                if usuario.rol !="administrador" or usuario.rol !="gerente" or usuario.rol !='empleado':
                    
                    
                    if  rol_nuevo== 'administrador' or rol_nuevo=='gerente' or rol_nuevo=='empleado':
                        usuario.rol= rol_nuevo
                        self.db_connector.session.commit()
                        print(f"el rol fue cambiado a {rol_nuevo}")
                
                
                elif rol_nuevo!= 'administrador' or rol_nuevo!='gerente' or rol_nuevo!='empleado':
                    
                    print("como vas a escribir mal imbecil")
                    
                else: print("ni modo  cuando lo sabes lo sabes")
                
         
                    
               
        # actualizar gerente

            
              
        if  permisos.actualizar_gerente(usuario_creador)=="gerente" :
                print(permisos.actualizar_gerente(usuario_creador))
                print(usuario_creador.rol)
                usuario = self.encontrar_usuario(username)
                if usuario.rol =="administrador":
                    print("ud no puede editar a un administrador")
                    
                elif usuario.rol !="administrador" or usuario.rol !="gerente" or usuario.rol !='empleado':
                    
                    if rol_nuevo=='administrador':
                        print( "no puedes volver a alguien administrador eres gerente")
                        
                    elif  rol_nuevo== 'administrador' or rol_nuevo=='gerente' or rol_nuevo=='empleado':
                            usuario.rol= rol_nuevo
                            self.db_connector.session.commit()
                            print(f"el rol fue cambiado a {rol_nuevo}")
                
                
                    elif rol_nuevo!= 'administrador' or rol_nuevo!='gerente' or rol_nuevo!='empleado':
                    
                            print("como vas a escribir mal imbecil")
                else:print("ni modo  cuando lo sabes lo sabes")
                  
        else:print("usuario no encontrado")
    
    
    
    # fin editar rol 


    def devolver_users(self,):
        lista_users=list(self.db_connector.session.query(Usuario).all())
        """for usuario in lista_users:
            print(f"Nombre: {usuario.username}")
            print(f"Status: {usuario.Status}")
            print(f"Rol: {usuario.Rol}")
            print("-" * 20)"""
        return lista_users
    


#termina crud usuarios 



# Configuración de la base de datos
if __name__ == '__main__':
    conexion = DbConnector(CONFIG)

    Base.metadata.create_all(conexion.engine)

    control_usuarios = ControlUsuarios(conexion)

    # print("prueba de  crear usuarios :")
    username="azael"
    password="1234"
    user_creador= "yosnell"
    usuario_creador = control_usuarios.encontrar_usuario(user_creador)
    status_nuevo="administrador"
    
    #control_usuarios.edit_rol_user(usuario_creador,username,status_nuevo)

    control_usuarios.devolver_users()
    #control_usuarios.delete_user(usuario_creador,'nuevo_usuario4')

    #control_usuarios.reset_password(usuario_creador,'yosnel', '1234')

    #control_usuarios.create_user(usuario_creador, 'nuevo_usuario4', 'contraseña1234', 'empleado')

# Observacion   hay que hacer una autenticacion tambien para contrasenia ya que se pueden crear dos usuarios con contrasenias iguales

#observacion 2 no se que es esa vaina de deprecated yosnel chambee


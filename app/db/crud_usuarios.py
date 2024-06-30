"""Modulo que encripta la contraseña"""
from math import perm
from re import U
import bcrypt
from urllib3 import Retry
from crud_productos import Proveedor
from db.db_connector import DbConnector
from sqlalchemy import create_engine, false
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
Proveedor=Base.classes.proveedor

class ControlUsuarios:
    """clase que maneja las operaciones de los usuarios"""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def encontrar_usuario(self, username):
        """busca usuario por nombre"""
        return self.db_connector.session.query(Usuario).filter_by(username=username).first()
    

    # Inicio Create User
    #revisado
    def create_user(self, usuario_creador, username, password, rol_nombre):
        # Verificar si el usuario_creador puede crear un usuario
        """crea un usuario"""
        rol_usuario= permisos.crear_admin(usuario_creador)
        usuario = self.encontrar_usuario(username)
        
        if rol_usuario !="administrador":
            print("No tienes permisos para crear usuarios.")
            #raise NotPermisos
            return False
        

        elif rol_usuario  =="administrador":
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
            nuevo_usuario = Usuario(username=username,
                            contrasena=hashed.decode('utf-8'),
                            Rol=rol_nombre)
            
            self.db_connector.session.add(nuevo_usuario)
            self.db_connector.session.commit()
            print("Usuario creado exitosamente.")
            return True
            
        else:
            print(usuario)
            print(f"El usuario '{username}' ya existe.")
            return False
    # FIN CREATE USER

    #incio imagino que esto es puro para el inicio de sesion
    #revisado
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
    #revisado
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

            
        elif  permisos.actualizar_gerente(usuario_creador):
            """resetea la contraseña"""
            usuario = self.encontrar_usuario(username)
            if usuario.Rol=="administrador":
                print("ud no puede modificar a un administrador")
                return false
            elif usuario == usuario_creador:
                print("no puedes modificarte a ti mismo")
                return false
                
            elif usuario:
                hashed = bcrypt.hashpw(
                    new_password.encode('utf-8'), bcrypt.gensalt())
                usuario.contraseña = hashed.decode('utf-8')
                self.db_connector.session.commit()
                print("Contraseña cambiada exitosamente.")
                return True
        
        else:
            print(f"El usuario '{username}' no fue encontrado")
            return false

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
        if   permisos.actualizar_admin(usuario_creador)=="administrador" :
                usuario = self.encontrar_usuario(username)
                        
                if  usuario.status ==1 or usuario.status== 0:
                        usuario.status= status_nuevo
                        self.db_connector.session.commit()
                        print(f"el status fue cambiado a {status_nuevo}")
                
                
                elif usuario.status !=1 or usuario.status!= 0:
                    
                    print("como vas a escribir mal imbecil")
                
                    
               
     # actualizar gerente

            
              
        elif  permisos.actualizar_gerente(usuario_creador)=="gerente" :
            
                usuario = self.encontrar_usuario(username)
                    
                if  usuario.status ==1 or usuario.status== 0:
                        usuario.status= status_nuevo
                        self.db_connector.session.commit()
                        print(f"el status fue cambiado a {status_nuevo}")
                
                
                elif usuario.status !=1 or usuario.status!= 0:
                    
                    print("como vas a escribir mal imbecil")
                
                  
        else:("usuario no encontrado")
    
    # fin editar status usuarios
    
    
    
    
    # inicio editar rol
    def edit_rol_user(self,usuario_creador,username,rol_nuevo):
            
        if  permisos.actualizar_admin(usuario_creador)=="administrador" :
                usuario = self.encontrar_usuario(username)   
                if  rol_nuevo== 'administrador' or rol_nuevo=='gerente' or rol_nuevo=='empleado':
                        usuario.rol= rol_nuevo
                        self.db_connector.session.commit()
                        print(f"el rol fue cambiado a {rol_nuevo}")
                
                    
                else: print("escribiste mal")
                
         
                    
               
         # actualizar gerente

            
              
        elif  permisos.actualizar_gerente(usuario_creador)=="gerente" :
                usuario = self.encontrar_usuario(username)
                if usuario.Rol =="administrador":
                    print("ud no puede editar a un administrador")
                    
                elif usuario.Rol !="administrador" or usuario.Rol !="gerente" or usuario.Rol !='empleado':
                    
                    if rol_nuevo=='administrador':
                        print( "no puedes volver a alguien administrador eres gerente")
                        
                    elif  rol_nuevo== 'administrador' or rol_nuevo=='gerente' or rol_nuevo=='empleado':
                            usuario.Rol= rol_nuevo
                            self.db_connector.session.commit()
                            print(f"el Rol fue cambiado a {rol_nuevo}")
                
            
                    
                           
                else: print("como vas a escribir mal imbecil")
                  
        else:print("usuario no encontrado")
    
    
    
    # fin editar Rol 


    def devolver_users(self,):
        lista_users=list(self.db_connector.session.query(Usuario).all())
        """for usuario in lista_users:
            print(f"Nombre: {usuario.username}")
            print(f"Status: {usuario.Status}")
            print(f"Rol: {usuario.Rol}")
            print("-" * 20)"""
        return lista_users
    


#termina crud usuarios 

class ControlProveedor:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def encontrar_nombre_proveedor(self, Nom_proveedor):
        """busca proveedor por nombre"""
        print( self.db_connector.session.query(Proveedor.Nom_proveedor).filter_by(Nom_proveedor=Nom_proveedor).first()  )
        
        return self.db_connector.session.query(Proveedor).filter_by(Nom_proveedor=Nom_proveedor).first()   
    
    def create_proveedor(self, usuario_creador, id_provedor, Nom_proveedor,telf_proveedor):

        """crea un proveedor"""
        rol_usuario= permisos.crear_admin(usuario_creador)
        
        if rol_usuario !="administrador":
            print("No tienes permisos para crear usuarios.")
            #raise NotPermisos
            return False
        

        elif rol_usuario  =="administrador":
            nuevo_proveedor = Proveedor(Id_provedor=id_provedor,
                            Nom_proveedor=Nom_proveedor,
                            Telf_proveedor=telf_proveedor)
            
            self.db_connector.session.add(nuevo_proveedor)
            self.db_connector.session.commit()
            print("proveedor creado exitosamente.")
            return True
            
        else:
            print(f"El proveedor '{Nom_proveedor}' ya existe.")
            return False
    
    


# Configuración de la base de datos
if __name__ == '__main__':
    conexion = DbConnector(CONFIG)

    Base.metadata.create_all(conexion.engine)

    control_usuarios = ControlUsuarios(conexion)
    control_proveedor = ControlProveedor(conexion)

    # print("prueba de  crear usuarios :")
    username="azael"
    password="1234"
    user_creador= "yosnel"
    usuario_creador = control_usuarios.encontrar_usuario(user_creador)
    status_nuevo="administrador"
        
    # control_usuarios.edit_rol_user(usuario_creador,username,status_nuevo) #furula

    #control_usuarios.authenticate_user("azael","1234") furula
    
    #control_usuarios.delete_user(usuario_creador,'nuevo_usuario4') #furula

    #control_usuarios.reset_password(usuario_creador,'azael', '1234') #furula

    # control_usuarios.create_user(usuario_creador, 'nuevo_usuario99', '1234', 'empleado') #furla

    #control_proveedor.encontrar_nombre_proveedor("jonathan")
    control_proveedor.create_proveedor(usuario_creador,33,"fernandez",231341231) #furula


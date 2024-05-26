"""Modulo que contiene la clase para la manipulacion de usuarios."""
#si desea hacer pruebas en este script directamente tienen que quitar los
#'Modulos.db.' de los from import 👍
import bcrypt
from db.db_connector import DbConnector
from db.tablas import Base, Usuario

class ControlUsuarios:
    """Clase con metodos para manipulacion de usuarios. Metodos que contiene:
    1. create_user
    2. auth_user
    3. reset_pass
    4. dell_user"""
    def __init__(self, conector:DbConnector):
        self.db_connector = conector

    def create_user(self, username, password) -> bool:
        """Crea el usuario si el usarname pasado no esta en uso de lo contrario devolvera false"""
        usuario = self.db_connector.session.query(
            Usuario).filter_by(Username=username).first()
        if not usuario:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            usuario = Usuario(Username=username,
                            Password=hashed.decode('utf-8'),
                            Status=1)
                            #hice que el valor de status por defecto manualmente sea 1, me imagino que eso lo pueden hacer uds de otra manera
            self.db_connector.session.add(usuario)
            self.db_connector.session.commit()
            print("Usuario creado exitosamente.")
            return True
        else:
            print(f"El usuario {username} ya existe.")
            return False

    def auth_user(self, username, password) -> bool:
        """Autentificacion de usuario.
        devuelve true si el usuario existe y su contraseña coincide"""
        usuario = self.db_connector.session.query(
            Usuario).filter_by(Username=username).first()
        if usuario:
            if bcrypt.checkpw(password.encode('utf-8'), usuario.Password.encode('utf-8')):
                print("Usuario autenticado correctamente.")
                return True
            print("Contraseña incorrecta.")
            return False
        print(f"El usuario {username} no fue encontrado")
        return False

    def reset_pass(self, username, new_password):
        """No he probado este metodo att: daniel"""
        usuario = self.db_connector.session.query(
            Usuario).filter_by(nombres=username).first()
        if usuario:
            hashed = bcrypt.hashpw(
                new_password.encode('utf-8'), bcrypt.gensalt())
            usuario.contraseña = hashed.decode('utf-8')
            self.db_connector.session.commit()
            print("Contraseña cambiada exitosamente.")
        else:
            print(f"El usuario {username} no fue encontrado")

    def dell_user(self, username):
        """tampoco he probado este metodo"""
        usuario = self.db_connector.session.query(
            Usuario).filter_by(nombres=username).first()
        if usuario:
            self.db_connector.session.delete(usuario)
            self.db_connector.session.commit()
            print(f"Usuario {username} borrado correctamente.")
        else:
            print(f"El usuario {username} no existe en la BD")

if __name__ == '__main__':
    # Configuración de la base de datos
    CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
    db_connector = DbConnector(CONFIG)

    Base.metadata.create_all(db_connector.engine)

    control_usuarios = ControlUsuarios(db_connector)
    control_usuarios.create_user('juan', '1234')
#EOF

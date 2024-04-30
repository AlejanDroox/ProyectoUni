"""Hashea la contraseña"""
import bcrypt
import mysql.connector

# apartado con el CRUD relacionado a los usuarios, tiene para crear, autenticar,
# cambiar contraseña y borrar usuarios (digan si creen que deberia haber algo mas)
# lo relacionado a los niveles de acceso va para despues xdxdxdxd

class ControlUsuarios:
    """Metodos Relacionados a la Gestopn de Usuarios"""
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_user(self, username, password):
        """Metodo de Creacion de Usuarios"""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor = self.db_connector.connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombres, contraseña) VALUES (%s, %s)", (username, hashed))
            self.db_connector.connection.commit()
            print("Usuario creado exitosamente.")
        except mysql.connector.Error as e:
            print("No se pudo crear el usuario", e)

    def authenticate_user(self, username, password):
        """Comprobocaion de autentificacion"""
        try:
            cursor = self.db_connector.connection.cursor()
            cursor.execute(
                "SELECT contraseña FROM usuarios WHERE nombres = %s", (username,))
            user = cursor.fetchone()

            if user:
                hashed_password = user[0]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    print("Usuario autenticado correctamente.")
                    return True
                print("contraseña incorrecta.")
                return False
            print(f"El usuario '{username}' no fue encontrado")
            return False
        except mysql.connector.Error as e:
            print("error autenticando usuario", e)
            return False

    def reset_password(self, username, new_password):
        """Metodo de restablecimiento de contraseña de usuario en especifico"""
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor = self.db_connector.connection.cursor()
            cursor.execute(
                "UPDATE usuarios SET contraseña = %s WHERE nombres = %s", (hashed, username))
            self.db_connector.connection.commit()
            print("contraseña cambiada exitosamente.")
        except mysql.connector.Error as e:
            print("Error con el cambio de contraseña", e)

    def delete_user(self, username):
        """Metodo para borrar usuarios"""
        try:
            cursor = self.db_connector.connection.cursor()
            cursor.execute(
                "SELECT nombres FROM usuarios WHERE nombres = %s", (username,))
            user = cursor.fetchone()

            if user:

                cursor.execute(
                    "DELETE FROM usuarios WHERE nombres = %s", (username,))
                self.db_connector.connection.commit()

                print(f"Usuario borrado {username} correctamente.")

            else:
                print(f"El usuario {username} no existe en la BD")

        except mysql.connector.Error as e:
            print("Error a la hora de borrar el usuario", e)

# End-of-file (EOF)

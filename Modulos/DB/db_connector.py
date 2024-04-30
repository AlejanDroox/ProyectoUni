"""libreria de la conexion al a BD"""
import mysql.connector

# no pregunten como funciona este codigo, lo copié y pegué


class DBConnector:
    """ Clase que """

    def __init__(self, config: dir):
        self.config = config
        self.connection = None

    def connect(self):
        """Metodo que establece la conexion"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL Server")
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)

    def disconnect(self):
        """Metodo que desconecta la BD"""
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL Server")
# End-of-file (EOF)

"""Clase de conexion BD"""
from db_connector import DBConnector

# pip install mysql-connector-python bcrypt

config = {
    'user': 'root',
    'password': '1234',
    'host': '127.0.0.1',
    'database': 'dbferreteria',  # nombre de la BD
    "port": "3306"
}


conx = DBConnector(config=config)
conx.connect()
# End-of-file (EOF)

"""Conector BD"""
from db_connector import DBConnector
from Modulos.DB.ctrlusuarios import ControlUsuarios


config = {
    'user': 'root',
    'password': 'root123',
    'host': '127.0.0.1',
    'database': 'otravez',  # nombre de la BD
    "port": "3306"
}

db_connector = DBConnector(config)
db_connector.connect()
user_manager = ControlUsuarios(db_connector)
user_manager.delete_user("yosnel")

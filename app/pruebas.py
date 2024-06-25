from db.crud_productos import ControlProductos, Producto
from db.db_connector import DbConnector
from utils.globals import CONFIG
conx = DbConnector(CONFIG)
crtl = ControlProductos(conx)
crtl.devolver_productor(Producto)
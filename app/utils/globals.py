"""Modulo donde se podran variables y constantes para acceder desde cualquier
lado evitando la importacion circular"""

DIRECCIONES= {
    'inicio': '/',
    'inventario': '/app/procesos',
    'reporte': '/app/reportes',
    'ayuda': '/app/ayuda',
    'archivos': '/app/archivos'
}
"""Direcciones de enrutamiento para flet"""

CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
""" Configuracion de conexion de Base de datos"""
class User():
    """Solo contiene el rol y el nombre es para pruebas"""
    def __init__(self, user, rol):
        self.user = user
        self.__rol = rol
    def get_rol(self):
        """retorna el rol por ahora yo mismo lo defino """
        return self.__rol

class ControlSesion():
    def agg_sesion(self):
        



def show_drawer(e):
    """mostrar menu lateral"""
    e.page.views[-1].drawer.open = True
    e.page.views[-1].update()

# End-of-file (EOF)

"""Modulo donde se podran variables y constantes para acceder desde cualquier
lado evitando la importacion circular"""

DIRECCIONES= {
    'inicio': '/',
    'inventario': '/app/procesos',
    'reporte': '/app/reportes',
    'ayuda': '/app/ayuda',
    'archivos': '/app/archivos',
    'panel': '/app/panel_control',
}
"""Direcciones de enrutamiento para flet"""

CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
""" Configuracion de conexion de Base de datos"""
class User():
    """Solo contiene el rol y el nombre es para pruebas"""
    def __init__(self, user, rol):
        self.user = user
        self.rol = rol
    def get_rol(self):
        """retorna el rol por ahora yo mismo lo defino """
        return self.rol

class ControlSesion():
    """Agrega y elimina la instancia de la sesion actual"""
    def agg_sesion(self, sesion:User):
        self.sesion = sesion
    def dell_sesion(self):
        del self.sesion
def show_drawer(e):
    """mostrar menu lateral"""
    e.page.views[-1].drawer.open = True
    e.page.views[-1].update()

user = User('azael', 'administrador')
ctrl_sesion = ControlSesion()
# End-of-file (EOF)

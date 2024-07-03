"""Modulo donde se podran variables y constantes para acceder desde cualquier
lado evitando la importacion circular"""

DIRECCIONES= {
    'inicio': '/',
    'inventario': '/app/procesos',
    'reporte': '/app/reportes',
    'ayuda': '/app/ayuda',
    'archivos': '/app/archivos',
    'panel': '/app/panel_control',
    'pruebas': 'pruebas',
    'registro': '/app/registro'
}
"""Direcciones de enrutamiento para flet"""

CONFIG = 'mysql://root:1234@127.0.0.1:3306/dbferreteria'
LOGO = r'assets/logo.png'
""" Configuracion de conexion de Base de datos"""
class User():
    """Guarda los datos de la sesion actual""" 
    def __init__(self):
        self.username: str = ''
        self.rol: str = ''
        self.status: str = ''
    def setter(self, user):
        self.username = user.username
        self.rol = user.Rol
        self.status = user.Status
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
user = User()

ctrl_sesion = ControlSesion()
# End-of-file (EOF)

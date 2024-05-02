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


def show_drawer(e):
    """mostrar menu lateral"""
    e.page.views[-1].drawer.open = True
    e.page.views[-1].update()

# End-of-file (EOF)

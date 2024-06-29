"""Script principal"""
import flet as ft
from views.procesos import Inventario, menu_lateral
from views.iniciosesion import InicioSesion
from views.panel_control import Panel_Control
from views.tabla_registro import TablaRegistro
from utils.globals import DIRECCIONES, show_drawer
from views.pruebas import BODY_PRUEBAS
from views.colors import GRIS_FONDOS
def main(page: ft.Page):
    """funcion principal"""

    menu = menu_lateral(page=page)
    inventario = Inventario(page=page)
    body_inicio = InicioSesion(page,inventario)
    STYLE_APP_BAR = {
        'bgcolor':'#FFF510',
        'actions':[ft.Image(src=r'app\assets\logo.png')],
        'toolbar_height':80, 
        'center_title':True
    }
    def cambio(e):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [body_inicio.body]
            )
        )
        if page.route == DIRECCIONES['inventario']:
            page.views.append(
                ft.View(
                    DIRECCIONES['inventario'],
                    controls= [
                        ft.AppBar(
                            title=ft.Text("VENTAS", size=36),
                            **STYLE_APP_BAR),
                        inventario
                        ],
                    drawer=menu,
                    bgcolor=GRIS_FONDOS
                )
            )
        elif page.route == "/app/ayuda":
            page.views.append(
                ft.View(
                    "/app/ayuda",
                    [
                        ft.AppBar(title=ft.Text("app/ayuda", size=36), **STYLE_APP_BAR),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu
                )
            )
        elif page.route == "/app/p":
            page.views.append(
                ft.View(
                    "/app/p",
                    [
                        ft.AppBar(title=ft.Text("app/procesos", size=36), **STYLE_APP_BAR),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu
                )
            )
        elif page.route == DIRECCIONES['registro']:
            page.views.append(
                ft.View(
                    DIRECCIONES['registro'],
                    [
                        ft.AppBar(title=ft.Text("Registro", size=36), **STYLE_APP_BAR),
                        TablaRegistro(page)
                    ],
                    drawer=menu,
                    bgcolor=GRIS_FONDOS
                )
            )
        elif page.route == "/app/archivos":
            page.views.append(
                ft.View(
                    "/app/archivos",
                    [
                        ft.AppBar(title=ft.Text("app/archivos"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu
                )
            )
        elif page.route == DIRECCIONES['panel']:
            page.views.append(
                ft.View(
                    DIRECCIONES['panel'],
                    [
                        ft.AppBar(title=ft.Text("Panel De Control", size=36), **STYLE_APP_BAR),
                        Panel_Control(page=page)
                    ],
                    drawer=menu,
                    bgcolor=GRIS_FONDOS
                )
            )
        elif page.route == DIRECCIONES['pruebas']:
            page.views.append(
                ft.View(
                    DIRECCIONES['pruebas'],
                    [
                        ft.AppBar(title=ft.Text("Zona de pruebas visuales"), bgcolor=ft.colors.SURFACE_VARIANT),
                        BODY_PRUEBAS
                    ],
                    drawer=menu
                )
            )
        page.update()
    # pylint: disable=unused-argument
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    def key_event(e:ft.KeyboardEvent):
        #print(e.key)
        pass
    page.on_keyboard_event = key_event
    page.window_width = 1280
    page.window_height = 720
    page.window_resizable = False
    page.window_maximizable = False
    page.vertical_alignment = 'CENTER'
    page.horizontal_alignment = 'CENTER'
    page.on_route_change = cambio
    page.on_view_pop = view_pop
    #page.go(DIRECCIONES['panel'])
    page.go(page.route)
    page.add()
    page.title = 'Ferretería Sam Benito'
    page.theme_mode ='light'


if __name__ == '__main__':
    ft.app(target=main)

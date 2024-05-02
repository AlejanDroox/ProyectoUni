"""Script principal"""
import flet as ft
from Modulos.gui.general import inventario, menu_lateral
from Modulos.gui.iniciosesion import inicio_sesion
from Modulos.globals import DIRECCIONES, show_drawer

def main(page: ft.Page):
    """funcion principal"""
    page.theme = ft.Theme(color_scheme_seed="blue")# cambiar los colores oir lo
    body_inicio = inicio_sesion(page=page)
    inventario1 = inventario(page=page)
    # pylint: disable=unused-argument
    def cambio(e):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [body_inicio]
            )
        )
    # aqui iria los meas route y toda la vaina pero se alarga mucho la imagen
        if page.route == DIRECCIONES['inventario']:
            page.views.append(
                ft.View(
                    DIRECCIONES['inventario'],
                    [ft.AppBar(title=ft.Text("Procesos"),
                    bgcolor=ft.colors.SURFACE_VARIANT),
                    inventario1],
                    drawer=menu_lateral(page=page)
                )
            )
        elif page.route == "/app/ayuda":
            page.views.append(
                ft.View(
                    "/app/ayuda",
                    [
                        ft.AppBar(title=ft.Text("app/ayuda"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu_lateral(page=page)
                )
            )
        elif page.route == "/app/p":
            page.views.append(
                ft.View(
                    "/app/p",
                    [
                        ft.AppBar(title=ft.Text("app/procesos"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu_lateral(page=page)
                )
            )
        elif page.route == "/app/reportes":
            page.views.append(
                ft.View(
                    "/app/reportes",
                    [
                        ft.AppBar(title=ft.Text("app/reportes"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store",
                        on_click=lambda _: page.go(DIRECCIONES['inventario'])),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=menu_lateral(page=page)
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
                    drawer=menu_lateral(page=page)
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
    page.window_height = 960
    page.window_resizable = False
    page.window_maximizable = False
    page.vertical_alignment = 'CENTER'
    page.horizontal_alignment = 'CENTER'
    page.on_route_change = cambio
    page.on_view_pop = view_pop
    page.go(page.route)
    page.add()
    page.title = 'hola'



if __name__ == '__main__':
    ft.app(target=main)

# End-of-file (EOF)
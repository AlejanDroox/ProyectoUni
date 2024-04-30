import flet as ft
from Modulos.GUI.iniciosesion import InicioSesion, inventario, MenuLateral
from Modulos.globals import DIRECCIONES, show_drawer
class User():
    def __init__(self, identificador, clave):
        self.id = identificador
        self._pass = clave
    def Valid(self):
        #aqui hariamos la comprobacion
        if True:
            return True
        else:
            raise NotFoundValueUser("Valores no encontrados en el sistema")
def main(page: ft.Page):
    
    

    
    page.theme = ft.Theme(color_scheme_seed="blue")# cambiar los colores oir lo
    InicioSesion1 = InicioSesion(page=page)
    inventario1 = inventario(page=page)
    
    def cambio(a):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [InicioSesion1]
            )
        )
        if page.route == '/app/procesos':
            page.views.append(
                ft.View(
                    '/app/procesos',
                    [ft.AppBar(title=ft.Text("Procesos"), bgcolor=ft.colors.SURFACE_VARIANT), inventario1],
                    drawer=MenuLateral(page=page)
                )
            )
        elif page.route == "/app/ayuda":
            page.views.append(
                ft.View(
                    "/app/ayuda",
                    [
                        ft.AppBar(title=ft.Text("app/ayuda"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store", on_click=lambda _: page.go("/app/procesos")),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=MenuLateral(page=page)
                )
            )
        elif page.route == "/app/p":
            page.views.append(
                ft.View(
                    "/app/p",
                    [
                        ft.AppBar(title=ft.Text("app/procesos"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store", on_click=lambda _: page.go("/app/procesos")),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=MenuLateral(page=page)
                )
            )
        elif page.route == "/app/reportes":
            page.views.append(
                ft.View(
                    "/app/reportes",
                    [
                        ft.AppBar(title=ft.Text("app/reportes"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store", on_click=lambda _: page.go("/app/procesos")),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=MenuLateral(page=page)
                )
            )
        elif page.route == "/app/archivos":
            page.views.append(
                ft.View(
                    "/app/archivos",
                    [
                        ft.AppBar(title=ft.Text("app/archivos"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go store", on_click=lambda _: page.go("/app/procesos")),
                        ft.ElevatedButton("Menu", on_click=show_drawer),
                    ],
                    drawer=MenuLateral(page=page)
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    def key_event(e:ft.KeyboardEvent):
        print(e.key)
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
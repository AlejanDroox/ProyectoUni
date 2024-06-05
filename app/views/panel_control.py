import flet as ft
from utils.globals import User
from db.permisos import PERMISOS
user = User('juan', 'administrador')
CONTAINER_STYLE_1 = {
    'bgcolor': '#949494',
    'border_radius': 5
}
CONTAINER_STYLE_2 = {
    'bgcolor': '#D9D9D9',
    'border_radius': 10
}

class Panel_Control(ft.Container):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.user = user
        self.alert_dialog = Panel_alerts(page= page)
        self.contenido()
        self.padding = ft.padding.only(top=50)
        self.alignment = ft.alignment.top_center
        self.border= ft.border.all()
        self.page.update()
    def contenido(self):
        icon = ft.CircleAvatar(
                content=ft.Icon(ft.icons.PERSON_OUTLINED, size=70),
                color=ft.colors.BLACK,
                bgcolor='#D9D9D9',
                radius=60
            )

        #contenedor izquierdo, tiene lo de la info de user 
        content_info = ft.Container(
            **CONTAINER_STYLE_2,
            content=ft.Column(
                [
                    ft.Text(
                        value=f'Usuario: {self.user.user}',
                        color='black'
                    ),
                    ft.Text(
                        value=f'Rol: {self.user.get_rol()}',
                        color='black'
                    ),
                ]
            ),
            height=330,
            width=330,
        )
        contenedor_i = ft.Container(
            **CONTAINER_STYLE_1,
            content= ft.Column(
                [
                    icon,
                    content_info
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=10),
            height=500,
            width=370
        )
        contenedor_d = ft.Container(
            **CONTAINER_STYLE_1,
            content=ft.Column(
                [
                    ft.FilledTonalButton("Agregar Usuario", icon="person_add", on_click= lambda _: self.open_dialog()),
                    ft.FilledTonalButton("Elminar Usuario", icon='person_remove'),
                    ft.FilledTonalButton("Editar Rol de Usuario", icon="edit"), # No me cuadra ese icono pero no se que otro poner xd
                    ft.FilledTonalButton("Editar Status de Usuario", icon='supervised_user_circle'),
                    ft.Divider(thickness=2, color='white'),
                    ft.Container(
                        **CONTAINER_STYLE_2,
                        width=650,
                        height=215
                    )
                ]
            ),
            padding=ft.padding.only(left=35, top=10),
            width=735,
            height=725
        )
        self.content= ft.Row(
            [
                contenedor_i,
                contenedor_d
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    def open_dialog(self):
        self.page.dialog = self.alert_dialog
        self.alert_dialog.open = True
        self.page.update()
class Panel_alerts(ft.AlertDialog):
    STYLE_ALERT = {
        'bgcolor': 'white',
        
    }
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.alert_agg()
    def alert_agg(self):
        def mostrar_pass(btn:ft.IconButton, entry: ft.TextField):
            btn.selected = not btn.selected
            entry.password = not entry.password
            btn.page.update()
        
        title = ft.Text("Agregar Usuario", size=48, weight=ft.FontWeight.W_900, selectable=True)
        entry_user = ft.TextField(label='Nombre', width=240)
        entry_pass = ft.TextField(label='Contraseña', password=True, width=240)
        btn_pass = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED, on_click= lambda _: mostrar_pass(btn_pass, entry_pass))
        btn_aceptar = ft.TextButton(text='Aceptar')
        btn_cancelar = ft.TextButton(text='Cancelar')
        multi_select = ft.Dropdown(
            label= 'Rol',
            width=160,
            options= [
                ft.dropdown.Option("Administrador"),
                ft.dropdown.Option("Gerente"),
                ft.dropdown.Option("Empleado")
            ], padding=ft.padding.only(left=27)
        )
        self.widgt_agg = [entry_user,entry_pass, btn_aceptar, btn_cancelar]
        body = ft.Column(
                    [
                        title, 
                        ft.Container(
                            ft.Row(
                                [
                                    entry_user, multi_select
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=ft.padding.only(left=45, top=23, right=27)
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    entry_pass, btn_pass
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=ft.padding.only(left=45, top=35, bottom=55)
                        ),
                        ft.Row(
                            [
                                btn_cancelar, btn_aceptar
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        
                    ],
                    width=512,
                    height=408,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

        self.content = body
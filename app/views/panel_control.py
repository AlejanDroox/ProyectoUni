import flet as ft
from utils.globals import User
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
    def __init__(self):
        super().__init__()
        self.user = user
        self.contenido()
        self.padding = ft.padding.only(top=50)
        self.alignment = ft.alignment.top_center
        self.border= ft.border.all()
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
                    ft.FilledTonalButton("Agregar Usuario", icon="person_add"),
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

class Panel_alerts(ft.AlertDialog):
    STYLE_ALERT = {
        'bgcolor': 'white',
        
    }
    STYLE_TITLE 
    def __init__(self):
        super().__init__()

    def alert_agg(self):
        title = ft.Text("Agregar Usuario", size=48, weight=ft.FontWeight.W_900, selectable=True)
        entry_user = ft.TextField(label='Nombre')
        multi_select = ft.Dropdown(
            width=160,
            options=[
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue"),
            ],
        )
        body = ft.Container(
            [
                ft.Column(
                    [
                        title, 
                        ft.Row(
                            [
                                entry_user, 
                            ]
                        )
                    ]
                )
            ]
        )
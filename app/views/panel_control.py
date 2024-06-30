import flet as ft
from utils.globals import user, CONFIG
from views.panel_alerts import PanelAlerts
from db.db_connector import DbConnector
from db.crud_usuarios import ControlUsuarios
CONTAINER_STYLE_1 = {
    'bgcolor': '#949494',
    'border_radius': 5
}
CONTAINER_STYLE_2 = {
    'bgcolor': '#D9D9D9',
    'border_radius': 10
}
class Panel_Control(ft.Container):
    """Usando un continer creo un widget visual unico para el panel de control
    el cual posea tanto frotend y el backed del mismo, """
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.conx = DbConnector(CONFIG)
        self.crtl_user = ControlUsuarios(self.conx)
        self.alert_dialog = PanelAlerts(page= page, crtl_user=self.crtl_user, load_table=self.load_table)
        self.page.dialog = self.alert_dialog
        self.contenido()
        self.padding = ft.padding.only(top=50)
        self.alignment = ft.alignment.top_center
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
                        value=f'Usuario: {user.username}',
                        color='black',
                        size=24 if len(user.username) < 10 else 20,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        value=f'Estatus: {user.rol}',
                        color='black',
                        size=24,
                        text_align=ft.TextAlign.CENTER
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            height=130,
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
            height=300,
            width=370
        )
        
        self.tabla_user = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Estatus")),
                    ft.DataColumn(ft.Text("Estado")),
                ],
            )
        contenedor_d = ft.Container(
            **CONTAINER_STYLE_1,
            content=ft.Column(
                [
                    ft.FilledTonalButton("Agregar Usuario", icon="person_add", on_click= lambda _: self.open_dialog('agg'), width=450),
                    ft.FilledTonalButton("Elminar Usuario", icon='person_remove', on_click= lambda _: self.open_dialog('dell'), width=450),
                    ft.FilledTonalButton("Editar Estatus de Usuario", icon="edit", on_click= lambda _: self.open_dialog('edit_rol'), width=450),
                    ft.FilledTonalButton("Editar Estado de Usuario", icon='supervised_user_circle',  on_click= lambda _: self.open_dialog('edit_status'), width=450),
                    ft.Container(ft.Divider(thickness=2, color='white'), padding=ft.padding.only(left=10, top=30,right=10, bottom=2),),
                    ft.Container(ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED, on_click=lambda _: self.load_table(), icon_color='white', icon_size=20), alignment=ft.Alignment(0.85,0.15)),
                    ft.Container(
                        content=ft.Column(
                            [self.tabla_user],
                            scroll=ft.ScrollMode.ALWAYS
                        ),
                        **CONTAINER_STYLE_2,
                        width=650,
                        height=215,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            ),
            padding=ft.padding.only(left=35, top=10, bottom=20),
            width=735,
            height=525
        )
        self.content= ft.Row(
            [
                contenedor_i,
                contenedor_d
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    def open_dialog(self, alert_name):
        """alerts_names = {
            'agg': self.alert_agg,
            'dell': self.alert_dell,
            'edit_rol': self.alert_edit_rol,
            'edit_status': self.draw_alert_edit_status,
        }"""
        self.alert_dialog.change_alert(alert_name)
        self.alert_dialog.open = True
        self.page.update()
    def load_table(self):
        self.tabla_user.rows.clear()
        for user in self.crtl_user.devolver_users():
            status = 'activo' if user.Status != '0' else 'inactivo'
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(user.username)),
                    ft.DataCell(ft.Text(user.Rol)),
                    ft.DataCell(ft.Text(status)),
                ]
            )
            self.tabla_user.rows.append(row)
        self.page.update()
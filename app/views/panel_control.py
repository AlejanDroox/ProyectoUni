import flet as ft
from utils.globals import user, CONFIG
from db.permisos import PERMISOS
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
        self.user = user
        self.conx = DbConnector(CONFIG)
        self.alert_dialog = Panel_alerts(page= page, conx=self.conx)
        self.page.dialog = self.alert_dialog
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
                    ft.FilledTonalButton("Agregar Usuario", icon="person_add", on_click= lambda _: self.open_dialog('agg')),
                    ft.FilledTonalButton("Elminar Usuario", icon='person_remove', on_click= lambda _: self.open_dialog('dell')),
                    ft.FilledTonalButton("Editar Rol de Usuario", icon="edit", on_click= lambda _: self.open_dialog('edit_rol')), # No me cuadra ese icono pero no se que otro poner xd
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
    def open_dialog(self, alert_name):
        self.alert_dialog.change_alert(alert_name)

        self.alert_dialog.open = True
        self.page.update()
class Panel_alerts(ft.AlertDialog):
    """Un controlador de los distintos alertdialog que necesarios, crea todos los 
    alert dialog los guarda en una variable y segun se necesite el contenido del alert
    dialog sera uno u otro. tambien posee el backend de los mismos"""
    STYLE_ALERT = {
        'bgcolor': 'white',  
    }
    def __init__(self, page:ft.Page, conx):
        super().__init__()
        self.crtl_user = ControlUsuarios(conx)
        self.page = page
        self.draw_alerts()
        self.alerts = {
            'agg': self.alert_agg,
            'dell': self.alert_dell,
            'edit_rol': self.alert_edit_rol,
        }
    
    def draw_alerts(self):
        self.draw_alert_agg()
        self.draw_alert_dell()
        self.draw_alert_edit_rol()
    
    def change_alert(self, alert_name):
        self.content = self.alerts[alert_name]
    
    def draw_alert_agg(self):
        """Crea el alert Dialog de agregar usuario"""
        def mostrar_pass(btn:ft.IconButton, entry: ft.TextField):
            btn.selected = not btn.selected
            entry.password = not entry.password
            btn.page.update()
        def aceptar():
            new_user = entry_user.value
            passw = entry_pass.value
            rol = multi_select.value
            self.crtl_user.create_user(usuario_creador=user, username=new_user, password=passw, rol_nombre=rol)
        title = ft.Text("Agregar Usuario", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre', width=240)
        entry_pass = ft.TextField(label='Contraseña', password=True, width=240)
        btn_pass = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED, on_click= lambda _: mostrar_pass(btn_pass, entry_pass))
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar())
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        multi_select = ft.Dropdown(
            label= 'Rol',
            width=160,
            options= [
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("gerente"),
                ft.dropdown.Option("empleado")
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
        self.alert_agg = body
    
    def draw_alert_dell(self):
        def aceptar():
            user_dell = entry_user.value
            if user_dell != entry_user_r.value:
                print('los nombres no coinciden')
                return False
            self.crtl_user.delete_user(usuario_creador=user, username=user_dell)
        title = ft.Text("Eliminar Usuario", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre de Usuario a eliminar', width=240)
        entry_user_r = ft.TextField(label='Repetir Nombre', width=240)
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar())
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        body = ft.Column(
                    [
                        title, 
                        entry_user,
                        entry_user_r,
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
        self.alert_dell = body
    
    def draw_alert_edit_rol(self):
        def aceptar():
            new_user = entry_user.value
            passw = entry_pass.value
            rol = multi_select.value
            self.crtl_user.create_user(usuario_creador=user, username=new_user, password=passw, rol_nombre=rol)
        def check():
            btn_aceptar.disabled = not btn_aceptar.disabled
            self.page.update()
        title = ft.Text("Editar Rol", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre de usuario',tooltip='Nombre  del usuario a cambiar rol', width=240)
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar(), disabled=True)
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        btn_check = ft.CupertinoCheckbox(
            label="Usted confirma el cambio de rol de este usuario",
            on_change= lambda _: check()
        )
        multi_select = ft.Dropdown(
            label= 'Rol',
            width=160,
            options= [
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("gerente"),
                ft.dropdown.Option("empleado")
            ], padding=ft.padding.only(left=27)
        )
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
                        btn_check,
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
        self.alert_edit_rol = body
    def close(self):
        for i in self.widgt_agg:
            i.value = ''
        self.open = False
        self.page.update()
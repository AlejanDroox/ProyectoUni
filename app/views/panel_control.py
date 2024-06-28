import flet as ft
from utils.globals import user, CONFIG
from db.permisos import PERMISOS
from db.db_connector import DbConnector
from db.crud_usuarios import ControlUsuarios
from utils.errores import ValuesExist
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
        self.alert_dialog = Panel_alerts(page= page, crtl_user=self.crtl_user, load_table=self.load_table)
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
#region PanelAlerts
class Panel_alerts(ft.AlertDialog):
    """Un controlador de los distintos alertdialog que necesarios, crea todos los 
    alert dialog los guarda en una variable y segun se necesite el contenido del alert
    dialog sera uno u otro. tambien posee el backend de los mismos"""
    STYLE_ALERT = {
        'bgcolor': 'white',  
    }
    def __init__(self, page:ft.Page, crtl_user, load_table):
        super().__init__()
        self.load_table = load_table
        self.crtl_user = crtl_user
        self.page = page
        self.draw_alerts()
        self.alerts = {
            'agg': self.alert_agg,
            'dell': self.alert_dell,
            'edit_rol': self.alert_edit_rol,
            'edit_status': self.alert_edit_status,
        }
        self.STYLE_BANNER_ERROR = {
            'bgcolor':ft.colors.AMBER_100,
            'leading':ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            'actions':[ft.TextButton("aceptar", on_click=self.close_banner)]
        }
        self.STYLE_BANNER_FINE = {
            'bgcolor':ft.colors.BLUE_100,
            'leading':ft.Icon(ft.icons.CHECK, color=ft.colors.AMBER, size=40),
            'actions':[
                ft.TextButton("aceptar", on_click=self.close_banner),
            ],
        }
        self.msg_error_unexp = 'Ha ocurrido un error inesperado intentelo nuevamente \n si el error persiste llama a servicio tecnico'
    def draw_alerts(self):
        self.draw_alert_agg()
        self.draw_alert_dell()
        self.draw_alert_edit_rol()
        self.draw_alert_edit_status()
    
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
            try:
                self.crtl_user.create_user(usuario_creador=user.rol, username=new_user, password=passw, rol_nombre=rol)
                self.page.banner = ft.Banner(
                    content=ft.Text(
                        f"Se ha agregado al usuario {new_user} de manera exitosa"
                    ),
                    **self.STYLE_BANNER_FINE
                )
                show_banner_click()
            except ValuesExist as e:
                self.page.banner = ft.Banner(
                    content=ft.Text(e.msg),
                    **self.STYLE_BANNER_ERROR
                )
                show_banner_click()
                
            self.close(entry_pass, entry_user, multi_select)
            self.load_table()
        def show_banner_click():
            self.page.banner.open = True
            self.page.update()
            self.page.banner.actions[0].focus()
        title = ft.Text("Agregar Usuario", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre', width=240)
        entry_pass = ft.TextField(label='Contraseña', password=True, width=240)
        btn_pass = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED, on_click= lambda _: mostrar_pass(btn_pass, entry_pass))
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar())
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        multi_select = ft.Dropdown(
            label= 'Estatus',
            width=160,
            options= [
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("gerente"),
                ft.dropdown.Option("empleado")
            ], padding=ft.padding.only(left=27),
            on_change= lambda _: print(multi_select.value)
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
        def show_banner_click():
            self.page.banner.open = True
            self.page.update()
        def aceptar():
            user_dell = entry_user.value
            if user_dell != entry_user_r.value:
                self.page.banner = ft.Banner(
                    content=ft.Text(f"los nombres no coinciden, intente nuevamente"),
                    **self.STYLE_BANNER_ERROR
                )
                show_banner_click()
            try: 
                self.crtl_user.delete_user(usuario_creador=user, username=user_dell)
                self.page.banner = ft.Banner(
                    content=ft.Text(
                        f"Se ha eliminado al usuario {user_dell} de manera exitosa"
                    ),
                    **self.STYLE_BANNER_FINE
                )
                show_banner_click()
            except ValuesExist as e:
                self.page.banner = ft.Banner(
                    content=ft.Text(e.msg),
                    **self.STYLE_BANNER_ERROR
                )
                show_banner_click()
            except:
                self.page.banner = ft.Banner(
                    content=ft.Text(value=self.msg_error_unexp),
                    **self.STYLE_BANNER_ERROR
                )
                show_banner_click()
            finally:
                self.close(entry_user, entry_user_r)
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
        title = ft.Text("Editar Estatus", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre de usuario',tooltip='Nombre  del usuario a cambiar Estatus', width=240)
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar(), disabled=True)
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        btn_check = ft.CupertinoCheckbox(
            label="Usted confirma el cambio de Estatus de este usuario",
            on_change= lambda _: check()
        )
        multi_select = ft.Dropdown(
            label= 'Estatus',
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
    def draw_alert_edit_status(self):
        def aceptar():
            user2 = self.crtl_user.encontrar_usuario(entry_user.value)
            self.crtl_user.edit_status_user(
                usuario_creador=user,
                username=entry_user.value,
                status_nuevo= 'inactivo' if user2.Status != 0 else 'activo'
            )
            self.load_table()
            self.close([entry_user, en])
            
        def check():
            btn_aceptar.disabled = not btn_aceptar.disabled
            self.page.update()
        def search_user(e):
            user = self.crtl_user.encontrar_usuario(entry_user.value)
            if user:
                btn_check.label = f'Seguro que quiere cambiar el Estado de {user.username} a {'inactivo' if user.Status != 0 else 'activo'}'
                entry_user.color = None
                entry_user.tooltip = ''
                entry_user.update()
                btn_check.update()
            else:
                entry_user.color = 'red'
                entry_user.tooltip = 'No se encontro al usuario'
                entry_user.update()
        title = ft.Text("Editar Estatus", size=48, weight=ft.FontWeight.W_900)
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar(), disabled=True)
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        entry_user = ft.TextField(
            label='Nombre de usuario',tooltip='Nombre  del usuario a cambiar Estado',
            on_submit=search_user,
            width=240
            )
        btn_check = ft.CupertinoCheckbox(
            label="Esperando datos del usuario",
            on_change= lambda _: check()
        )
        btn_search = ft.IconButton(
            icon=ft.icons.SEARCH,
            on_click=search_user
        )
        body = ft.Column(
                    [
                        title, 
                        ft.Container(
                            ft.Row(
                                [
                                    entry_user, btn_search
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
        self.alert_edit_status = body
    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()
    def close(self, *entrys):
        for e in entrys:
            e.value = ''
        self.open = False
        self.page.update()

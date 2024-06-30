import flet as ft
from db.permisos import PERMISOS
from db.db_connector import DbConnector
from db.crud_usuarios import ControlUsuarios
from utils.errores import ValuesExist
from utils.globals import user, CONFIG

class PanelAlerts(ft.AlertDialog):
    """Un controlador de los distintos alertdialog que necesarios, crea todos los 
    alert dialog los guarda en una variable y segun se necesite el contenido del alert
    dialog sera uno u otro. tambien posee el backend de los mismos"""
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
            'not_acces': self.alert_not_acces
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
        self.draw_not_acces()
    
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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

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
        def comprobacion(e):
            enabled = bool(entry_user.value and entry_user_r.value and entry_user.value == entry_user_r.value)
            btn_aceptar.disabled = enabled
            btn_aceptar.update()
        title = ft.Text("Eliminar Usuario", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre de Usuario a eliminar', width=240, on_change=comprobacion)
        entry_user_r = ft.TextField(label='Repetir Nombre', width=240, on_change= comprobacion)
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar(), disabled=True)
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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
            disble = btn_check.value and entry_user.value and r
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
                btn_check.label = f'Debe Introducir Primero el nombre de usuario'
                entry_user.color = 'red'
                entry_user.tooltip = 'No se encontro al usuario'
                entry_user.update()
        title = ft.Text("Editar Estado", size=48, weight=ft.FontWeight.W_900)
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
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

            )
        self.alert_edit_status = body
    def draw_not_acces(self):
        body = ft.Container(
            alignment=ft.alignment.center,
            width=300,
            height=200,
            padding=ft.padding.all(16),
            border_radius=ft.border_radius.all(12),
            bgcolor=ft.colors.AMBER_100,
            content=ft.Text(
                "No posees los permisos para acceder a esta función.\nRequiere un rol de gerente o superior.",
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.AMBER_900,
            ),
        )
        self.alert_not_acces = body
    def show_banner(self, is_error: bool, text:str):
        if not is_error:
            self.page.banner = ft.Banner(
                content=ft.Text(text),
                **self.STYLE_BANNER_FINE
            )
        else:
            self.page.banner = ft.Banner(
                content=ft.Text(text),
                **self.STYLE_BANNER_ERROR
            )
        self.page.banner.open = True
        self.page.update()
        self.page.banner.actions[0].focus()
    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()
    def close(self, *entrys):
        for e in entrys:
            e.value = ''
        self.open = False
        self.page.update()

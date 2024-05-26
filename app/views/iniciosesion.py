"""Contiene todo la estructura visual del inicio de sesion y
los procesos de la ventana misma"""
import flet as ft
from utils.globals import DIRECCIONES, CONFIG
from db.db_connector import DbConnector
from db.ctrlusers import ControlUsuarios
class EntrySesion(ft.TextField):
    def __init__(self, label = 'EntrySesion', is_pass = False, icon = None):
        super().__init__()
        #self.input_filter = filter
        self.width=280,
        self.height=40,
        self.border_radius= ft.border_radius.horizontal(left=10,right=30),
        self.label = label,
        #hint_text='Contraseña', es otra forma de poner el texto pero el de arriba me gusto mas
        self.color= ft.colors.WHITE,
        self.prefix_icon= icon, #el icono tambien podria ser lock
        #self.text_vertical_align= -1,
        self.password= is_pass,
    
class InicioSesion():
    def __init__(self, page):
        super().__init__()
        self.entry_user =  ft.TextField(
            width=280,
            height=40,
            border_radius= ft.border_radius.horizontal(left=10,right=30),
            label = 'Username',
            #hint_text='Cedula', es otra forma de poner el texto pero el de arriba me gusto mas
            color= ft.colors.WHITE,
            prefix_icon=ft.icons.PEOPLE,
            #input_filter= ft.NumbersOnlyInputFilter(),
            text_vertical_align= -1.0
        )
        self.entry_pass = ft.TextField(
                width=280,
                height=40,
                border_radius= ft.border_radius.horizontal(left=10,right=30),
                label = 'Contraseña',
                #hint_text='Contraseña', es otra forma de poner el texto pero el de arriba me gusto mas
                color= ft.colors.WHITE,
                prefix_icon=ft.icons.PASSWORD, #el icono tambien podria ser lock
                text_vertical_align= -1.0,
                password= True,
            )
        self.body = ft.Container(
            ft.Row([
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.Text(
                                # Titulo Principal
                                'Inicio de Sesion',
                                width=360,
                                size=30,
                                weight='w900',
                                text_align='center',
                            ),
                            # contenedor del enty de la cedula
                            ft.Container(
                                self.entry_user,
                                padding=ft.padding.only(10)
                            ),
                            ft.Container(
                                self.entry_pass,
                                padding=ft.padding.only(10)
                            ),
                            ft.Container(
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        'ENTRAR',
                                        color='white',
                                        weight='w500',
                                    ),
                                    width=280,
                                    bgcolor='black',
                                    on_click=lambda _: self.auth(page, self.entry_user.value, self.entry_pass.value)
                                ),
                                padding=ft.padding.only(40, 10),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        width=380,
                        height=460
                    ),
                    #border= ft.border.all()
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_EVENLY,
            #vertical_alignment= ft.CrossAxisAlignment.CENTER
            ),
            #border= ft.border.all()
            #alignment= ft.CrossAxisAlignment.CENTER
        )

    def auth(self,page:ft.Page, user, passw):
        """autentificacion para el enrutamiento del inicio de sesion"""

        conx = DbConnector(config=CONFIG)
        ctrl = ControlUsuarios(conx)
        if ctrl.auth_user(user,passw):
            page.go(DIRECCIONES['inventario'])
            print(user)

    
    def auth2(self):
        """autentificacion para el enrutamiento del inicio de sesion"""
        user = self.entry_user.value
        passw = self.entry_pass.value
        conx = DbConnector(config=CONFIG)
        ctrl = ControlUsuarios(conx)
        if ctrl.auth_user(user,passw):
            page.go(DIRECCIONES['inventario'])
            print(user)
    

def auth(page:ft.Page, user, passw):
    """autentificacion para el enrutamiento del inicio de sesion"""

    conx = DbConnector(config=CONFIG)
    ctrl = ControlUsuarios(conx)
    if ctrl.auth_user(user,passw):
        page.go(DIRECCIONES['inventario'])
        print(user)



#proceso para crear usuario
#config = {
#        'user': 'root',
#        'password': '1234',
#        'host': '127.0.0.1',
#        'database': 'dbferreteria',  # nombre de la BD
#        "port": "3306"
#    }
#    conx = DBConnector(config=config)
#    conx.connect()
#    ctrl = ControlUsuarios(conx)
#    ctrl.create_user(username='hola', password= '1234')

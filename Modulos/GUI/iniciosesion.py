"""Contiene todo la estructura visual del inicio de sesion y
los procesos de la ventana misma"""
import flet as ft
from Modulos.globals import DIRECCIONES, CONFIG
from Modulos.db.db_connector import DbConnector
from Modulos.db.ctrlusers import ControlUsuarios

def inicio_sesion(page: ft.Page) -> ft.Container("body del inicio de sesion"):
    """devuelve toda la estructura del inicio de sesion"""
    entry_user =  ft.TextField(
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
    entry_pass = ft.TextField(
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
    body = ft.Container(
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
                            entry_user,
                            padding=ft.padding.only(10)
                        ),
                        ft.Container(
                            entry_pass,
                            padding=ft.padding.only(10)
                        ),
                        ft.Container(
                            ft.ElevatedButton(
                                content=ft.Text(
                                    'INICIAR',
                                    color='white',
                                    weight='w500',
                                ),
                                width=280,
                                bgcolor='black',
                                on_click=lambda _: auth(page, entry_user.value, entry_pass.value)
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
    return body

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

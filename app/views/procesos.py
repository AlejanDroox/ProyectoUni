"""Contiene todo lo relacionado a la estructura y
procesos de la ventana 'procesos', valga la redundancia"""
from time import sleep
import flet as ft
from utils.globals import user_actual, DIRECCIONES, CONFIG
from db.db_connector import DbConnector
from db.crud_productos import ControlProductos
# region clases
class Producto():
    """Crea la estructura visual de cada producto"""
    def __init__(self, n_producto:str,marca:str, des:str, existencia:int,
                page:ft.Page, id_producto:int, tab:ft.Tabs):
        self.page = page
        self.tab = tab
        self.n_producto = n_producto
        self.marca = marca
        self.des = des
        self.id_producto = id_producto
        self.existencia = existencia
        self.nombre_compuesto = ft.Text(value=f'{self.n_producto} {self.marca}\n{self.des}',
                                        overflow=ft.TextOverflow.CLIP,
                                        width=200, max_lines=3)
        self.cont_nombre = ft.Container(ft.Column([
                                        ft.Text(value=f'ID: {id_producto}'),
                                        self.nombre_compuesto,
                                        ]),padding=ft.padding.only(bottom=100),
                                        )
        self.boton_editar = ft.Container(ft.IconButton(ft.icons.EDIT,
                                        on_click=lambda _:self.tab_go()),
                                    padding=ft.padding.only(bottom=125))
        self.text_existencia =  ft.Text(value=self.existencia)
        self.imagen = ft.Image(
                            src="https://picsum.photos/300/200",
                            width=250,
                            height= 150,
                            fit=ft.ImageFit.COVER,
                            border_radius=8
                        )
        self.contenido = ft.Row([
                        self.imagen,
                        self.cont_nombre,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND)
        self.btn_editar()
        self.card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content= self.contenido,
                        padding=ft.padding.only(15,10),
                        #border=ft.border.all()
                        ),
                ],
                ),
                width=525,
                height=225,
                #on_hover=lambda _: self.hover()
            ),
        )

    def update_edit(self):
        """actualiza la parte visual de la card del producto"""
        self.nombre_compuesto.value = f'{self.n_producto} {self.marca}\n{self.des}'
        self.page.update()

    def btn_editar(self):
        """es prueba, se supone que comprobara el nivel de usuario y
        habilitara o deshabilitara el boton de editar"""
        if user_actual.rol > 0:
            self.contenido.controls.append(self.boton_editar)

    def tab_go(self):
        """Vuelve visible el tab de la ediccion, hace una pause
        para luego hacer animacon de traslasion"""
        self.tab.tabs[0].visible = True
        self.tab.selected_index = 1
        self.page.update()
        self.tab.tabs[0].content = tab_edit(self)
        self.tab.selected_index = 0
        sleep(0.2)
        self.page.update()

    def actualizar_bd(self):
        """aqui se puede hacer la actualizacion o no se"""
        return self


class LineaProductos():
    """Contiene las card generadas en la clase producto
    de manera ordenada y en scroll"""
    def __init__(self):
        self.lineas = []  # Initialize the lineas attribute as an empty list
        self.contenido = ft.Column(controls=self.lineas,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                scroll=ft.ScrollMode.ALWAYS,
                                spacing=50,
                                height=750,
                                width=1200,)
    def agg_card(self, producto:Producto):
        """agregar una nueva card de un producto"""
        linea = ft.Row()
        try:
            cantidad = len(self.lineas[-1].controls)
            if cantidad < 2:
                self.lineas[-1].controls.append(producto.card)
            else:
                linea.controls.append(producto.card)
                linea.key = str(cantidad)
                self.lineas.append(linea)
            #self.lineas[-1].controls.append(producto.card)
        except IndexError:
            linea.controls.append(producto.card)
            linea.key = '0'
            self.lineas.append(linea)

#region funciones de dibujo
class Inventario(ft.Tabs):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.contenido()
        self.selected_index = 0
        self.animation_duration = 400
    def contenido(self):
        contenedor_productos = LineaProductos()
        tab_inventario = ft.Container(
            ft.Row([
                ft.Column([
                    ft.Container(
                        content=contenedor_productos.contenido,
                        border=ft.border.all(),
                        padding=ft.padding.only(left=70)
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            border=ft.border.all(),
        )
        self.tabs=[
            ft.Tab(
                text="EDIT",
                content=ft.Text('edit'),
                icon=ft.icons.EDIT_SQUARE,
                visible= False
            ),
            ft.Tab(
                text="inventario",
                content=tab_inventario,
                icon=ft.icons.INVENTORY
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
            
        ]
        self.expand=1
        self.cargar_productos(contenedor_productos)

    def cargar_productos(self,cont):
        for i in range(7):
            algo = Producto(n_producto=ferreteria_nombres[i],marca='Generica',
            des=ferreteria_descripciones[i],existencia=i+2, page=self.page, id_producto=i+1, tab=self.tabs)
            cont.agg_card(producto=algo)
        print('s')

def inventario(page: ft.Page) -> ft.Tabs():
    """crea y devuelve la estructura de la ventana procesos"""
    contenedor_productos = LineaProductos()  # Create an instance of the LineaProductos class
    tab1 = ft.Container(
        ft.Row([
            ft.Column([
                ft.Container(
                    content=contenedor_productos.contenido,
                    border=ft.border.all(),
                    padding=ft.padding.only(left=50)
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    ),
    border=ft.border.all(),
    )
    body = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="EDIT",
                content=ft.Text('edit'),
                icon=ft.icons.EDIT_SQUARE,
                visible= False
            ),
            ft.Tab(
                text="inventario",
                content=tab1,
                icon=ft.icons.INVENTORY
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
    )
    ctrl_bd = DbConnector(CONFIG)
    ctrl_p = ControlProductos(ctrl_bd)

    for i in range(20):
        algo = Producto(n_producto=ferreteria_nombres[i],marca='Generica',
        des=ferreteria_descripciones[i],existencia=i+2, page=page, id_producto=i+1, tab=body)
        contenedor_productos.agg_card(producto=algo)
    return body

def tab_edit(producto:Producto) -> ft.Container:
    """tab de edicion de productos"""
    def edit(e):
        if e.control.label == 'Marca':
            producto.marca = e.control.value
            print(producto.marca)
        elif e.control.label == 'Nombre':
            producto.n_producto = e.control.value
        elif e.control.label == 'des':
            producto.des = e.control.value
        producto.update_edit()
    style = ft.ButtonStyle(
        color={
            ft.MaterialState.HOVERED: ft.colors.WHITE,
            ft.MaterialState.FOCUSED: ft.colors.BLUE,
            ft.MaterialState.DEFAULT: ft.colors.BLACK,
        }, bgcolor='red',
        shape=ft.CircleBorder()
    )
    existencia_field = ft.TextField(value=producto.existencia, height=40, width=40,text_size=16)
    btn_marco_edicion = ft.Row([
        ft.FilledButton(text='-5', style=style),
        ft.FilledButton(text='-1', style=style),
        existencia_field,
        ft.FilledButton(text='+1', style=style),
        ft.FilledButton(text='+5', style=style),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    marco_edicion_body = ft.Column([
        ft.TextField(label='Marca',value= producto.marca, width=400, on_change=edit),
        ft.TextField(label='Nombre',value= producto.n_producto, width=400, on_change=edit),
        ft.TextField(label='des',value= producto.des, max_lines=3, width=400, on_change=edit),
        btn_marco_edicion
    ])

    col_izq = ft.Column([
        ft.Container(
            producto.imagen,
            padding=ft.padding.only(bottom=100)
            ),
        producto.card],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    marco_edicion = ft.Container(
        content= marco_edicion_body,
        height=730,
        width=430,
        border_radius=11,
        bgcolor='#000080',
        padding=ft.padding.only(left=15, top=20 )
    )
    body = ft.Container(
        ft.Row([
            col_izq,
            ft.Container(marco_edicion, padding=ft.padding.only(100))
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND),
        padding=ft.padding.only(top=30, bottom=30)
    )
    return body
# pylint: disable=unused-argument
def menu_lateral(page:ft.Page) -> ft.NavigationDrawer('Menu lateral principal'):
    """devuelve la estructura del menu lateral (drawer)"""
    btn_close = ft.TextButton(
        text='Salir',
        icon=ft.icons.EXIT_TO_APP,
        on_click= lambda _: page.go(DIRECCIONES['inicio'])
    )
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="PROCESOS",
                icon=ft.icons.ENGINEERING_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.ENGINEERING),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.INSERT_DRIVE_FILE_OUTLINED),
                label="ARCHIVOS",
                selected_icon=ft.icons.INSERT_DRIVE_FILE,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.REPORT_OUTLINED),
                label="REPORTES",
                selected_icon=ft.icons.REPORT,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.HELP_OUTLINE_SHARP),
                label="AYUDA",
                selected_icon=ft.icons.HELP,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.BACKUP_OUTLINED),
                label="BACKUP",
                selected_icon=ft.icons.BACKUP          
            ),
            ft.Divider(thickness=2),
            ft.Container(
                padding=ft.padding.only(top=550),
                content= btn_close,
                alignment=ft.alignment.bottom_center
            ),
        ],
        on_change=hola
    )
    return drawer
iconosBarra = {
    '0': '/app/procesos',
    '1': '/app/archivos',
    '2': '/app/reportes',
    '3': '/app/ayuda'
}
def hola(e:ft.ContainerTapEvent):
    """funcion de prueba solo se llama en cualquier cambio del menu lateral"""
    e.page.go(iconosBarra[e.data])
# region pruebas y vainas x
# Lista de nombres de herramientas o productos de ferretería (20 elementos)
ferreteria_nombres = [
    "Martillo",
    "Destornillador",
    "Llave inglesa",
    "Alicate",
    "Cinta métrica",
    "Nivel de agua",
    "Sierra",
    "Taladro",
    "Lijadora",
    "Escalera",
    "Pala",
    "Pico",
    "Rastrillo",
    "Manguera",
    "Pistola de agua",
    "Cepillo",
    "Rodillo",
    "Brocha",
    "Lija",
    "Clavos",
]

# Lista de descripciones breves de las herramientas o productos (20 elementos)
ferreteria_descripciones = [
    "Para golpear y clavar",
    "Para apretar y aflojar tornillos",
    "Para ajustar tuercas y tornillos",
    "Para cortar y pelar cables",
    "Para medir longitudes y distancias",
    "Para verificar la horizontalidad o verticalidad",
    "Para cortar madera, plástico y otros materiales",
    "Para hacer agujeros en paredes, madera y metal",
    "Para alisar y pulir superficies",
    "Para subir y bajar de lugares altos",
    "Para excavar tierra o mover materiales",
    "Para romper piedras o demoler estructuras",
    "Para juntar hojas o ramas",
    "Para transportar agua",
    "Para regar plantas o limpiar superficies",
    "Para limpiar superficies",
    "Para pintar superficies planas",
    "Para pintar superficies con detalles",
    "Para desgastar y pulir superficies",
    "Para unir piezas de madera u otros materiales",
]

# End-of-file

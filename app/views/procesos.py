"""Contiene todo lo relacionado a la estructura y
procesos de la ventana 'procesos', valga la redundancia"""
from time import sleep
import flet as ft
from utils.globals import DIRECCIONES, CONFIG
from db.db_connector import DbConnector
from db.crud_productos import ControlProductos
from jaro import jaro_winkler_metric

ID_PRODUCTO = {}

# region Inventario
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

class ProductCard(ft.ExpansionPanel):
    def __init__(self, image, name, description, characteristics, price, id):
        super().__init__()
        self.name = name
        hed_content = ft.Container(
            ft.Column(
            [
                ft.Image(src=image, width=230, height=200),
                ft.Text(name),
                ft.Text(description),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.only(bottom=10)
        )
        self.header = hed_content
        self.content = ft.Column(
            controls=[
                ft.Text(f"ID: {id}"),
                ft.Text("Características:"),
                ft.Text("  - " + ", ".join(characteristics)),
                ft.Text(f"Precio Venta: {price}"),
                ft.Text(f"Precio Compra: {price}"),
                ft.Text(f"EXistencias: 50"),
                ft.Text(f"Ultimo Proveedor: Mr. Lorum"),
                ft.Text(f"Ultimo Proveedor: Mr. Lorum"),
            ],
        )
class LineaProductos():
    """Contiene las card generadas en la clase producto
    de manera ordenada y en scroll"""
    def __init__(self):
        self.lineas = []  # Initialize the lineas attribute as an empty list
        self.contenido = ft.Column(controls=self.lineas,
                                scroll=ft.ScrollMode.ALWAYS,
                                spacing=25,
                                height=700,
                                width=1150,)
    def agg_card(self, producto):
        """agregar una nueva card de un producto"""
        linea = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        try:
            cantidad = len(self.lineas[-1].controls)
            if cantidad < 3:
                self.lineas[-1].controls.append(producto)
            else:
                linea.controls.append(producto)
                linea.key = str(cantidad)
                self.lineas.append(linea)
            #self.lineas[-1].controls.append(producto.card)
        except IndexError:
            linea.controls.append(producto)
            linea.key = '0'
            self.lineas.append(linea)
    def search(self, serch):
        if len(serch) >= 1:
            for i in self.lineas:
                for p in i.controls:
                    name = p.controls[0].name
                    for n in name.split():
                        similitud = jaro_winkler_metric(serch.lower(), n.lower())
                        if similitud > 0.70:
                            print(similitud)
                            print(n)
                            p.visible = True
                            print(p.visible)
                        else:
                            p.visible = False
                        p.update()
        elif serch == '':
            for i in self.lineas:
                for p in i.controls:
                    p.visible = True
                    p.update()
class Inventario(ft.Tabs):

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.contenido()
        self.selected_index = 0
        self.animation_duration = 400
    def contenido(self):
        self.entry_search = ft.TextField(
            label='Nombre el Producto',
            icon=ft.icons.SEARCH,
            on_change= lambda _: self.contenedor_productos.search(self.entry_search.value),
        )
        btn_create = ft.TextButton(
            text='agregar producto',
            icon=ft.icons.CREATE,
        )
        self.contenedor_productos = LineaProductos()
        tab_inventario = ft.Container(
            ft.Row([
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.entry_search, btn_create
                            ]
                        ),
                        ft.Container(
                            content=self.contenedor_productos.contenido,
                            border=ft.border.all(color='#BABABA', width=2.5),
                            bgcolor='#D9D9D9',
                            border_radius=18
                        ),
                    ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
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
        self.cargar_productos(self.contenedor_productos)

    def cargar_productos(self,cont):
        for i in range(18):
            product_card = ProductCard(
                image="app/assets/XDt.jpeg",
                name=ferreteria_nombres[i],
                description= ferreteria_descripciones[i], 
                characteristics=['bueno', 'bonito', 'barato'], 
                price=i,
                id=i)
            ID_PRODUCTO[ferreteria_nombres[i]] = str(i)
            panel = ft.ExpansionPanelList(
                expand_icon_color=ft.colors.AMBER,
                elevation=8,
                divider_color=ft.colors.AMBER,
                width=300,
                controls= [product_card],
                
            )
            cont.agg_card(panel)
            self.page.update()

    def search(self):
        try:
            key = '8'
            print(type(key))
            self.contenedor_productos.contenido.scroll_to(key='1', duration=100, offset=1)
            self.page.update()
        except  KeyError:
            pass


#region RegistroVentas

#region otros
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
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED),
                label="Panel Control",
                selected_icon=ft.icons.ADMIN_PANEL_SETTINGS
            ),
            ft.Divider(thickness=2),
            ft.Container(
                padding=ft.padding.only(top=450),
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
    '3': '/app/ayuda',
    '4': '/app/ayuda',
    '5': '/app/panel_control',
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

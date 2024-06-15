"""Contiene todo lo relacionado a la estructura y
procesos de la ventana 'procesos', valga la redundancia"""
from time import sleep
import flet as ft
from utils.globals import DIRECCIONES, CONFIG
from db.db_connector import DbConnector
from db.crud_productos import ControlProductos
from jaro import jaro_winkler_metric

name_product = {}
"""Contendra todos los productos en formato
Nombre: ProductCard"""
mini_cards = []
# region Inventario
class ProductCard(ft.ExpansionPanel):
    def __init__(self, image, name, description, characteristics, price, id):
        super().__init__()
        self.name = name
        self.image = image
        self.id = id
        self.mini_card = ft.Container(
            content=ft.Column(
                [
                    ft.Image(src=image, width=230, height=200),
                    ft.Text(name),
                    ft.Text(description)
                ]
            )
        )
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
class MiniCard(ft.Container):
    def __init__(self, name, image, id, price, cantidad):
        super().__init__()
        self.name = name
        self.image = image
        self.id = id
        self.price = price
        self.existencia = cantidad
        self.content=ft.Column(
                [
                    ft.Image(src=image, width=230, height=200),
                    ft.Text(value=f'{name}  precio:{price}'),
                    ft.Text(value=f'Disponibles {cantidad}', text_align='center'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        self.visible = False
        self.bgcolor = '#D3D3D3'
        self.border_radius = 18
        self.height = 275
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
                            p.visible = True
                            print(p.visible)
                            p.update()
                            break
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
        self.registro_ventas = RegistroVenta()
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
                content=self.registro_ventas,

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
            panel = ft.ExpansionPanelList(
                expand_icon_color=ft.colors.AMBER,
                elevation=8,
                divider_color=ft.colors.AMBER,
                width=300,
                controls= [product_card],
                
            )
            minicard = MiniCard(image='app/assets/XDt.jpeg', name= ferreteria_nombres[i], id=id, price = i, cantidad=50)
            self.registro_ventas.products.append(minicard)
            minicard.on_click = self.registro_ventas.select
            name_product[product_card.name] = product_card
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
            'edit': self.alert_edit,
        }
    
    def draw_alerts(self):
        self.draw_alert_agg()
        self.draw_alert_dell()
        self.draw_alert_edit()
    
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
        title = ft.Text("Editar ", size=48, weight=ft.FontWeight.W_900)
        entry_user = ft.TextField(label='Nombre', width=240)
        entry_marca = ft.TextField(label='Marca', width=240)
        entry_descripcion = ft.TextField(label='descripcion', width=240)
        btn_pass = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED, on_click= lambda _: mostrar_pass(btn_pass, entry_pass))
        btn_aceptar = ft.TextButton(text='Aceptar', on_click=lambda _: aceptar())
        btn_cancelar = ft.TextButton(text='Cancelar', on_click= lambda _: self.close())
        multi_select = ft.Dropdown(
            label= 'Proevedor',
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
#region RegistroVentas
class RegistroVenta(ft.Container):
    def __init__(self):
        super().__init__()
        #self.border=ft.border.all(color='#BABABA', width=2.5)
        self.products = []
        self.products_mini = []
        self.monto_total = 0
        self.draw_contenido()
    def draw_contenido(self):
        def comprobar_cant(e):
            control: ft.TextField = e.control
            for i in self.products:
                if i.name == self.entry_producto.value:
                    product_cant = i.existencia
                    break
            if control.value == '':
                pass
            elif int(control.value) > product_cant:
                control.color = 'red'
                control.tooltip = 'la cantidad ingresada es mayor a la cantidad disponible'
                self.btn_add.disabled = True
            elif int(control.value) <= 0:
                control.color = 'red'
                control.tooltip = 'la cantidad no puede ser menor a 1'
                self.btn_add.disabled = True
            elif int(control.value) >= 1 and int(control.value) <= product_cant:
                self.btn_add.disabled = False
                control.color = None
            self.update()
        
        def add_product():
            if self.entry_cant.color != 'red':
                registro_product = f'- {self.entry_producto.value} : {self.entry_cant.value} \n'
                self.actualizar_celda(0,2, registro_product)
                for i in self.products:
                    i:MiniCard
                    if i.name == self.entry_producto.value:
                        self.monto_total += i.price * int(self.entry_cant.value)
                        monto_total_text.value = f'Monto Total: {self.monto_total} bs'
                        self.actualizar_celda(0,3, self.monto_total)
                        break
                self.entry_producto.value = ''
                self.entry_producto.disabled = False
                self.entry_cant.disabled = True
                self.btn_add.disabled = True
                self.update()
        title = ft.Text(
            value='Registro De Ventas',
            size=48,
            weight=ft.FontWeight.W_900
        )
        self.entry_producto = ft.TextField(
            label='Nombre Producto',
            on_change = lambda _: self.search(self.entry_producto.value)
        )
        self.entry_cant = ft.TextField(
            label='Cantidad',
            width=60,
            label_style={'size': 8},
            input_filter=ft.NumbersOnlyInputFilter(),
            disabled=True,
            on_change=comprobar_cant
        )
        entry_ci_cliente = ft.TextField(
            label='Cedula Cliente',
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change= lambda _: self.actualizar_celda(0, 1, entry_ci_cliente.value)
        )
        metodo_pago = ft.Dropdown(
            label= 'Metodo de pago',
            width=160,
            options= [
                ft.dropdown.Option("BS"),
                ft.dropdown.Option("COP"),
                ft.dropdown.Option("USD")
            ],
            on_change= lambda _: self.actualizar_celda(0,4, metodo_pago.value)
        )
        headers = ["Fecha", "Cliente", "Descripción de Venta", "Monto Total", "Método de Pago"]

        # Crear las filas de la tabla (una fila vacía para empezar)
        rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(value="\n\n") ) for _ in headers
            ])
        ]
        
        # Crear la tabla
        self.table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(header)) for header in headers],
            rows=rows,
            data_row_min_height=150,
        )
        self.descripcion_venta = ft.Text(value='', max_lines=None, size=12)
        self.table.rows[0].cells[2].content = ft.Container(
                    content=ft.Column(
                        [self.descripcion_venta],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                )
        self.btn_add = ft.IconButton(
            icon=ft.icons.ADD,
            disabled=True,
            tooltip='Agregar Producto al Registro',
            on_click= lambda _: add_product()
        )
        self.btn_cancelar = ft.IconButton(
            icon=ft.icons.CANCEL_OUTLINED,
            disabled=True,
            tooltip='Cancelar seleccion de producto',
            on_click=lambda _: self.cancel_product()
        )
        btns = ft.Container(
                ft.Row(
                    [
                        self.btn_add, self.btn_cancelar
                    ]
                ),
            width=125,
            padding=ft.padding.only(bottom=275),
            border=ft.border.all()
        )
        self.list_product = ft.Container(
            content=ft.Column(controls=self.products,
                                scroll=ft.ScrollMode.ALWAYS,
                                spacing=25,
            ),
            height=350,
            width=250,
            #bgcolor='#D9D9D9'
            )
        monto_total_text = ft.Text(
            value=f'Monto total: 0 bs',
            size=18,
            weight=ft.FontWeight.W_900,
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
        body = ft.Column(
            [
                title,
                ft.Row(
                    [
                        self.entry_producto, self.entry_cant, entry_ci_cliente
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                ft.Row(
                    [
                        self.list_product, btns ,metodo_pago, monto_total_text 
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                ft.Container(
                    content= self.table,
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(bottom=40))
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
        self.content = body
    def search(self, search):
        if len(search) >= 1:
            for p in self.products:
                name = p.name
                for n in name.split():
                    similitud = jaro_winkler_metric(search.lower(), n.lower())
                    if similitud > 0.7:
                        p.visible = True
                        self.update()
                        break
                    p.visible = False
                    self.update()
        elif search == '':
            for i in self.products:
                i.visible = False
                self.update()
    def select(*self):
        product:MiniCard = self[1].control
        self: RegistroVenta = self[0]
        self.entry_producto.value = product.name
        self.entry_producto.disabled = True
        self.btn_cancelar.disabled = False
        self.btn_add.disabled = False
        self.entry_cant.disabled = False
        self.update()

    def cancel_product(self):
        self.entry_producto.value = ''
        self.entry_producto.disabled = False
        self.entry_cant.disabled = True
        self.btn_add.disabled = True
        self.update()
    def actualizar_celda(self,fila, columna, valor):
        if fila < len(self.table.rows) and columna < len(self.table.columns):
            if columna == 2:
                self.descripcion_venta.value += valor
            else:
                self.table.rows[fila].cells[columna].content.value = valor
            self.table.update()

#region otros
def tab_edit(producto) -> ft.Container:
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

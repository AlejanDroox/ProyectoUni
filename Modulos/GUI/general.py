"""Libreria de la interfaz"""
import flet as ft
from Modulos.globals import show_drawer
# region clases
class Producto():
    def __init__(self, Nproduct:str, des:str, Existencias:float, page:ft.Page, ID:int):
        self.page = page
        self.ID = ID
        self.TiDes = ft.ListTile(
                        leading=ft.Icon(ft.icons.LOCK),
                        title=ft.Text(Nproduct),
                        subtitle=ft.Text(value=des,
                                        max_lines=3),
                        #selected=True
                    )
        self.Existencias =  ft.Text(value=1)
        self.card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    self.TiDes,
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.ADD,
                            on_click=self.operacion 
                        ),
                        self.Existencias,
                        ft.IconButton(
                            icon=ft.icons.REMOVE,
                            on_click=self.operacion
                        ),
                    ])
                ],
                
                ),
                width=350,
                height=175,
                on_hover=lambda _: self.Hover(),
                
            ),
        )
    def Hover(self):
        if self.TiDes.selected:
            self.TiDes.selected = False
        else:
            self.TiDes.selected = True
        self.page.update()
    
    def operacion(*e):
        self:Producto = e[0] # el argumento 0 es si mismo
        widget: ft.ControlEvent = e[1] # es el objeto que manda flet
        if widget.control.icon == 'add':
            self.Existencias.value += 1
        else:
            self.Existencias.value -= 1
        widget.page.update()
    
    def ActualizarBD(self): # esta puede ser la funcion para guardar cambios a la base de datos una vez confirmados, no se si aqui directamente o llmando a otra
        return self


class LineaProductos():
    def __init__(self):
        self.lineas = []  # Initialize the lineas attribute as an empty list
        self.Contenido = ft.Column(controls=self.lineas,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                scroll=ft.ScrollMode.ALWAYS,
                                spacing=30,
                                height=750,
                                width=1200,)
    def agg(self, producto:Producto):
        linea = ft.Row()
        #print(len(self.lineas[-1].controls))
        try:
            cantidad = len(self.lineas[-1].controls) 
            if cantidad < 3:
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

def inventario(page: ft.Page):
    ContenedorProductos = LineaProductos()  # Create an instance of the LineaProductos class
    for i in range(20):
        algo = Producto(ferreteria_nombres[i], ferreteria_descripciones[i],0.1, page=page, ID=i)
        ContenedorProductos.agg(producto=algo)
    tab1 = ft.Container(
        ft.Row([
            ft.Column([
                
                ft.Container(
                    ft.Text(
                        value= 'Inventario',
                        size=32, color=ft.colors.YELLOW_ACCENT_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=ft.padding.only(top=50),
                    border=ft.border.all(),   
                    on_click=show_drawer
            ),
                ft.Container(
                    content=ContenedorProductos.Contenido,
                    border=ft.border.all()
                    #padding=ft.padding.only(top=50,left=15)
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
                text="Tab 1",
                content=tab1
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
        expand=1,
    )   
    return body
# pylint: disable=unused-argument
def menu_lateral(page:ft.Page) -> ft.NavigationDrawer('Menu lateral principal'):
    """devuelve la estructura del menu lateral (drawer)"""
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
                selected_icon=ft.icons.BACKUP,             
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
    print('cambio')
    print(e.data)
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

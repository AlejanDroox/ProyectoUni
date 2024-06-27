import flet as ft
from db.db_connector import DbConnectorRV
from db.crud_registro import CRUDVentas
from utils.globals import CONFIG
class TablaDatos(ft.DataTable):
    def __init__(self):
        super().__init__()
        headers = ["Fecha", "Cliente", "Descripción de Venta", "Monto Total", "Método de Pago"]
        self.columns=[ft.DataColumn(ft.Text(header,size=12,)) for header in headers]
        #self.scale = 1.5
        self.pack_rows = []   
    def agregar_datos(self, datos):
        self.pack_rows.clear()
        row = []
        for dato in datos:
            fila = ft.DataRow(cells=[
                ft.DataCell(ft.Text(size=18, value=dato['fecha'])),
                ft.DataCell(ft.Text(size=18, value=dato['cliente'])),
                ft.DataCell(ft.Column(
                        [ft.Text(size=12, value=self.format_descripcion_venta(dato['Descripcion_Venta']))],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )),
                ft.DataCell(ft.Text(size=18, value=str(dato['monto_total']))),
                ft.DataCell(ft.Text(size=18, value=dato['metodo'])),
            ])
            row.append(fila)
            if len(row) >= 10:
                self.pack_rows.append(row)
                row = []
        self.pack_rows.append(row)
        self.rows = self.pack_rows[0]
        self.update()
    def change_page(self, n):
        print(self.rows)
        self.rows = self.pack_rows[n]
        print(self.rows)
        self.update()
    def format_descripcion_venta(self, descripcion_venta):
        texto = ""
        for producto, cantidad in descripcion_venta.items():
            texto += f"- {producto}: {cantidad}\n"
        return texto

class TablaRegistro(ft.Container):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page = page
        self.conx = DbConnectorRV(CONFIG)
        self.alignment = ft.alignment.top_center
    def contenido(self):
        def change2():
            if self.pagina_n.value:
                n = int(self.pagina_n.value)
                if n > len(self.tabla.pack_rows)-1:
                    self.pagina_n.color = 'red'
                    self.pagina_n.tooltip = f'el valor no puede ser mayor a {len(self.tabla.pack_rows)-1}'
                else:
                    self.pagina_n.color = None
                    self.pagina_n.tooltip = ''
                    self.tabla.change_page(n)
        self.tabla = TablaDatos()
        style_number = {
            'width':75,
            'label_style':{"size":10},
            'border_radius':0,
            'border':ft.InputBorder.UNDERLINE,
            'filled':True,
            'input_filter': ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
        }
        self.pagina_n = ft.TextField(
            value='0',
            on_change= lambda _: change2(),
            **style_number,
            visible=False
        )
        top = ft.Row(
            [
                ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED, on_click=lambda _: self.load_datos() ),

            ]
        )
        self.content = ft.Column(
            [
                ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED, on_click=lambda _: self.load_datos()),
                self.tabla,
                self.pagina_n
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    def load_datos(self):
        self.conx.reopen_session()
        self.ctrl_registro = CRUDVentas(self.conx.get_session())
        self.datos = self.ctrl_registro.obtener_ventas()
        self.tabla.agregar_datos(datos=self.datos)
        self.pagina_n.hint_text = f'0-{(len(self.tabla.pack_rows)-1)}'
        self.pagina_n.visible = True
        self.pagina_n.update()
        self.conx.close_session()
    def build(self):
        self.contenido()
import flet as ft
from db.db_connector import DbConnectorRV
from db.crud_registro import CRUDVentas
headers = ["Fecha", "Cliente", "Descripción de Venta", "Monto Total", "Método de Pago"]
from utils.globals import CONFIG, user
import datetime

class TablaDatos(ft.DataTable):
    def __init__(self):
        super().__init__()
        self.columns=[ft.DataColumn(ft.Text(header,size=12,)) for header in headers]
        self.pack_rows = []
        self.header_style = ft.TextStyle(color=ft.colors.WHITE, bgcolor='#402C07')
        self.row_style = ft.TextStyle(color=ft.colors.BLACK, bgcolor='#FFF510')
        self.row_hover_style = ft.TextStyle(color=ft.colors.BLACK, bgcolor='#C0902E')
        self.column_spacing = 10
        self.border = ft.border.all(1, '#734F0E')
        self.horizontal_scrollbar = True
        self.vertical_scrollbar = True
        self.scroll = ft.ScrollMode.ALWAYS
        self.height = 480
        self.width = 1150
        #self.data_row_color={"hovered": "0x30FF0000"},
        self.vertical_lines=ft.BorderSide(3, "#CFCFCF")
        self.horizontal_lines=ft.BorderSide(1, "green")
        self.bgcolor = '#D9D9D9'
        self.pack_rows = []
    def agregar_datos(self, datos):
        self.pack_rows.clear()
        self.datos = []
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
                ft.DataCell(ft.Text(size=18, value=str(dato['monto_total']) + 'bs')),
                ft.DataCell(ft.Text(size=18, value=dato['metodo'])),
            ])
            row.append(fila)
            self.datos.append(
                [
                    dato['fecha'],
                    dato['cliente'],
                    self.format_descripcion_venta(dato['Descripcion_Venta']),
                    dato['monto_total'],
                    dato['metodo'],
                ]
            )
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
    def generar_pdf(self):
        pdf = MultiColumnPDF(headers=headers)
        for i in self.datos:
            pdf.row(i)
        pdf.output("app/assets/pdfdd.pdf")
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
                ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED, on_click=lambda _: self.load_datos(), icon_color='white', )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
        ),
        if user.rol == 'administrador':
            top = ft.Row(
                [
                    ft.IconButton(icon=ft.icons.CHANGE_CIRCLE_OUTLINED, on_click=lambda _: self.load_datos(), icon_color='white', ),
                        ft.IconButton(icon=ft.icons.FILE_DOWNLOAD_OUTLINED, on_click=lambda _: self.create_pdf(), icon_color='white',
                        tooltip='Descargar Registro'),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
            ),
        self.content = ft.Column(
            [
                top,
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
        #elf.tabla.generar_pdf()
        self.pagina_n.update()
        self.conx.close_session()
    def create_pdf(self):
        self.conx.reopen_session()
        self.ctrl_registro = CRUDVentas(self.conx.get_session())
        now = datetime.datetime.now()
        filename = f'{now.strftime('D%-M-%Y H%:M%')}'
        print(filename)
        self.conx.close_session()
    def build(self):
        self.contenido()
import flet as ft

class ProductCard(ft.ExpansionPanel):
    def __init__(self, image, name, description, characteristics, price):
        super().__init__()
        hed_content = ft.Container(
            ft.Column(
            [
                ft.Image(src=image, width=200, height=200),
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
                ft.Text("Características:"),
                ft.Text("  - " + ", ".join(characteristics)),
                ft.Text(f"Precio Venta: {price}"),
                ft.Text(f"Precio Compra: {price}"),
                ft.Text(f"EXistencias: 50"),
                ft.Text(f"Ultimo Proveedor: Mr. Lorum"),
                ft.Text(f"Ultimo Proveedor: Mr. Lorum"),
            ]
        )

BODY_PRUEBAS = ft.Container(
)
def main(page: ft.Page):


    product_card = ProductCard(
        image=r"./app/",
        name="Producto XYZ",
        description="Descripción del producto",
        characteristics=["Peso: 1kg", "Material: Plástico"],
        price="$10.99",
    )
    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.AMBER,
        elevation=8,
        divider_color=ft.colors.AMBER,
        width=300,
        controls= [product_card]
    )

    page.theme_mode = 'light'
    page.add(ft.Row([panel,panel]))
    page.scroll = ft.ScrollMode.ALWAYS
if __name__ == '__main__':
    ft.app(target=main)
import flet as ft

def main(page: ft.Page):
    def show(e):
        if text.visible:
            text.visible = False
        else:
            text.visible = True

        page.update()
    text = ft.TextField(
                "Image title",
                color="white",
                opacity=0.5,
                visible=False
                )
    st = ft.Stack(
        [
            ft.Row([
                ft.Image(
                src=f"https://picsum.photos/300/300",
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            ), 
        ]), 
            ft.Row(
                [
                    text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        width=300,
        height=300,
    )

    page.add(st)
    page.add(ft.TextButton('ver', on_click=show))

ft.app(target=main)
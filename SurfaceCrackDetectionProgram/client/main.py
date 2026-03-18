import flet as ft

from main_page import main as menu_view
from crack_detection import crack_detection_view


def main(page: ft.Page):

    page.title = "Crack Detection System"
    page.window_width = 1280
    page.window_height = 720
    page.padding = 0

    def show_landing():

        page.controls.clear()

        start_button = ft.ElevatedButton(
            content=ft.Text(
                "START",
                color="#FFFFFF"  # font color as hex
            ),
            bgcolor="#000000",   # button background color as hex
            on_click=lambda e: page.go("/menu")
        )

        layout = ft.Container(
            image=ft.DecorationImage(
                src="title.png",
                fit=ft.BoxFit.COVER
            ),
            expand=True,
            content=ft.Row(
                [start_button],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        page.add(layout)
        page.update()


    def route_change(e):

        page.controls.clear()

        if page.route == "/":
            show_landing()

        elif page.route == "/menu":
            menu_view(page)

        elif page.route == "/detect":
            crack_detection_view(page)

        page.update()


    page.on_route_change = route_change

    # start at landing
    show_landing()


ft.run(main, assets_dir=".")
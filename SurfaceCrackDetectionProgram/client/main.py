import flet as ft

from main_page import main as menu_view
from crack_detection import crack_detection_view
from signup_engineer import main as signup_engineer_view
from signup_developer import main as signup_developer_view


def main(page: ft.Page):

    page.title = "Crack Detection System"
    page.window_width = 1280
    page.window_height = 720
    page.padding = 0

    def show_landing():

        page.controls.clear()

        signup_button = ft.ElevatedButton(
            content=ft.Text("SIGN UP"),
            on_click=lambda e: page.go("/signup_engineer")
        )

        login_button = ft.OutlinedButton(
            content=ft.Text("LOGIN"),
            on_click=lambda e: page.go("/menu")
        )

        layout = ft.Container(
            image=ft.DecorationImage(
                src="CRACK DETECTION.png",
                fit=ft.BoxFit.COVER
            ),
            expand=True,
            content=ft.Row(
                [signup_button, login_button],
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

        elif page.route == "/signup_engineer":
            signup_engineer_view(page)

        elif page.route == "/signup_developer":
            signup_developer_view(page)

        page.update()


    page.on_route_change = route_change

    # start at landing
    show_landing()


ft.run(main, assets_dir=".")
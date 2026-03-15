import flet as ft

def main(page: ft.Page):
    page.title = "Crack Detection System - Engineer Signup"
    page.window.width = 1280
    page.window.height = 720
    page.padding = 0
    username_input = ft.TextField(
        width=300, height=60,
        bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
        border_color=ft.Colors.BLACK, border_width=1, border_radius=15,
        text_size=20, content_padding=ft.Padding.only(left=15, right=15)
    )
    password_input = ft.TextField(
        password=True, can_reveal_password=False, 
        width=300, height=60,
        bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK,
        border_color=ft.Colors.BLACK, border_width=1, border_radius=15,
        text_size=20, content_padding=ft.Padding.only(left=15, right=15)
    )

    def create_shadow_input(input_field):
        return ft.Stack(
            controls=[
                ft.Container(width=300, height=60, bgcolor="#E07A5F", border_radius=15, top=6, left=6),
                input_field
            ],
            width=310, height=70
        )
    create_button = ft.Button(
        content=ft.Text("CREATE", style=ft.TextStyle(weight=ft.FontWeight.W_800), color="#FFD500"),
        style=ft.ButtonStyle(
            bgcolor="#222222",
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=ft.Padding.symmetric(horizontal=50, vertical=25),
        ),
        on_click=lambda _: print(f"Creating account for: {username_input.value}")
    )
    
    # UPDATED: Added ft.ButtonStyle to create the #ffd60a oval background
    dev_link = ft.Button(
        content=ft.Text(
            "CLICK ME FOR DEVELOPER", 
            color=ft.Colors.BLACK, 
            style=ft.TextStyle(
                decoration=ft.TextDecoration.UNDERLINE, 
                weight=ft.FontWeight.W_700
            )
        ),
        style=ft.ButtonStyle(
            bgcolor="#ffd60a",
            shape=ft.RoundedRectangleBorder(radius=25), # This creates the oval shape
            padding=ft.Padding.symmetric(horizontal=25, vertical=10),
        ),
        on_click=lambda _: print("Navigating to Dev Account...")
    )
    
    signup_layout = ft.Container(
        image=ft.DecorationImage(
            src="engineerinspec.png", 
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        bgcolor=ft.Colors.BLUE_GREY_900, 
        content=ft.Stack(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, icon_size=35, top=20, left=20, on_click=lambda _: print("Back button clicked!")),
                ft.Container(content=create_shadow_input(username_input), left=250, top=220),
                ft.Container(content=create_shadow_input(password_input), left=250, top=345),
                ft.Container(content=create_button, left=150, top=500),
                ft.Container(content=dev_link, left=140, top=570)
            ]
        )
    )
    
    page.add(signup_layout)

if __name__ == "__main__":
    ft.run(main, assets_dir=".")
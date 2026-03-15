import flet as ft

def main(page: ft.Page):
    # Match the page dimensions to a standard desktop window
    page.title = "Crack Detection System"
    page.window_width = 1280
    page.window_height = 720
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Sign Up Button: Dark background, Yellow text
    signup_button = ft.ElevatedButton(
        content=ft.Text("SIGN UP", weight=ft.FontWeight.W_800, color="#FFD500"),
        style=ft.ButtonStyle(
            bgcolor="#222222",  
            shape=ft.RoundedRectangleBorder(radius=30), 
            padding=ft.Padding.symmetric(horizontal=45, vertical=20), 
        ),
        on_click=lambda e: print("Navigating to Sign Up...")
    )

    # Login Button: Transparent/Yellow background, Black border, Black text
    login_button = ft.OutlinedButton(
        content=ft.Text("LOGIN", weight=ft.FontWeight.W_800, color=ft.Colors.BLACK), 
        style=ft.ButtonStyle(
            side=ft.BorderSide(width=2, color=ft.Colors.BLACK), 
            shape=ft.RoundedRectangleBorder(radius=30), 
            padding=ft.Padding.symmetric(horizontal=55, vertical=20), 
        ),
        on_click=lambda e: print("Navigating to Login...")
    )

    # Group the buttons in a Row
    button_layout = ft.Row(
        controls=[signup_button, login_button],
        spacing=20,
    )

    # Use a Stack to overlay the buttons on top of the background image
    main_layout = ft.Container(
        # ---> THE FIX: Use ft.DecorationImage instead of image_src <---
        image=ft.DecorationImage(
            src="CRACK DETECTION.png",
            fit=ft.BoxFit.COVER, 
        ),
        expand=True,
        content=ft.Stack(
            controls=[
                # Use absolute positioning to place the buttons accurately
                ft.Container(
                    content=button_layout,
                    left=70,   
                    top=480,   
                )
            ]
        )
    )

    page.add(main_layout)

# Run the app
if __name__ == "__main__":
    ft.run(main)
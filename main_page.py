import flet as ft

def main(page: ft.Page):
    page.title = "Crack Detection System - Choose Action"
    page.window.width = 1280
    page.window.height = 720
    page.padding = 0


    def create_image_button(image_path, click_handler):
        return ft.Container(
            content=ft.Image(
                src=image_path,
                fit=ft.BoxFit.CONTAIN, # Ensures the image isn't stretched or cut off
            ),
            width=260,  # Estimated width based on your screenshot
            height=260, # Estimated height
            ink=True,   # Adds the click ripple effect!
            on_click=click_handler
            # Cursor line completely deleted! Flet handles the pointer automatically now.
        )

    # 1. Create the three image buttons and assign a print statement to test their clicks
    crack_btn = create_image_button("crack_button.png", lambda _: print("Navigating to: Identify Crack..."))
    wall_btn = create_image_button("wall_button.png", lambda _: print("Navigating to: Wall Import..."))
    
    # This button will be perfect for hooking up to your Roboflow dataset logic!
    dataset_btn = create_image_button("dataset.png", lambda _: print("Navigating to: Dataset Management..."))

    # 2. Build the main layout
    choose_layout = ft.Container(
        image=ft.DecorationImage(
            src="mainpage.png", # Your yellow background with the text
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        bgcolor=ft.Colors.BLUE_GREY_900, # Fallback color
        content=ft.Stack(
            controls=[
                # 3. Position the buttons using left and top coordinates. 
                # You might need to tweak these slightly to align perfectly with the text on your specific background image!
                ft.Container(content=crack_btn, left=160, top=180),
                ft.Container(content=wall_btn, left=510, top=180),
                ft.Container(content=dataset_btn, left=860, top=180),
            ]
        )
    )

    page.add(choose_layout)

if __name__ == "__main__":
    ft.run(main, assets_dir=".")
import flet as ft
import websockets
import asyncio
import base64
import json
import tempfile

def crack_detection_view(page: ft.Page):
    page.title = "Surface Crack Detection System"
    page.scroll = "adaptive"

    page.window.width = 1280
    page.window.height = 720
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Controls ---
    title_text = ft.Text(
        "Surface Crack Detection",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#000000"
    )

    image_name = ft.Text(color="#000000")
    image_holder = ft.Image(src="", visible=False, fit="contain")
    result_text = ft.Text(
        color="#000000",
        size=16,
        weight=ft.FontWeight.BOLD
    )
    confidence_label = ft.Text("Confidence: 0%", color="#000000")
    confidence_bar = ft.ProgressBar(width=250, value=0)
    processing = ft.ProgressRing(visible=False)
    history_list = ft.ListView(height=120, width=300)

    # --- Functions ---
    async def open_picker(e):
        picker = ft.FilePicker()
        files = await picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["jpg", "jpeg", "png"],
        )
        if not files:
            return
        f = files[0]
        image_name.value = f"Selected Image: {f.name}"

        if getattr(f, "path", None):
            with open(f.path, "rb") as rf:
                data_bytes = rf.read()
        elif getattr(f, "bytes", None) is not None:
            data_bytes = f.bytes
        else:
            result_text.value = "No usable file selected."
            page.update()
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(data_bytes)
            temp_path = tmp.name

        image_holder.src = temp_path
        image_holder.visible = True
        result_text.value = ""
        page.update()

    async def send_prediction_request(image_data: str):
        try:
            async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
                await websocket.send(json.dumps({"type": "predict", "data": image_data}))
                response = await asyncio.wait_for(websocket.recv(), timeout=20)
                data = json.loads(response)

                has_crack = data.get("has_crack")
                crack_count = data.get("crack_count")
                max_conf = data.get("max_confidence")

                confidence_bar.value = max_conf / 100
                confidence_label.value = f"Confidence: {round(max_conf,2)}%"

                if not has_crack:
                    result_text.value = "Surface Condition: NORMAL\nCracks Detected: 0"
                    history_list.controls.append(ft.Text("Normal surface detected", color="#000000"))
                else:
                    result_text.value = (
                        f"Surface Condition: CRACK DETECTED\n"
                        f"Number of Cracks: {crack_count}\n"
                        f"Highest Confidence: {round(max_conf, 2)}%"
                    )
                    history_list.controls.append(ft.Text(f"{crack_count} cracks | {round(max_conf,2)}%", color="#000000"))

        except Exception as ex:
            result_text.value = f"Error: {ex}"
        finally:
            page.update()

    async def predict_image(e):
        if not image_holder.src:
            result_text.value = "No image selected."
            page.update()
            return
        predict_btn.disabled = True
        processing.visible = True
        page.update()
        with open(image_holder.src, "rb") as f:
            image_bytes = f.read()
        image_data = base64.b64encode(image_bytes).decode("utf-8")
        await send_prediction_request(image_data)
        predict_btn.disabled = False
        processing.visible = False
        page.update()

    # --- Buttons ---
    predict_btn = ft.ElevatedButton(
        content=ft.Text("Analyze Surface", color="#FFFFFF"),
        bgcolor="#000000",
        width=180,
        height=50,
        on_click=predict_image
    )

    # --- Selected image + results ---
    selected_image = ft.Row(
        [
            ft.Container(
                content=ft.Column([image_name, image_holder],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=10,
                padding=10,
                border=ft.border.all(5, ft.Colors.BLACK),
                alignment=ft.alignment.Alignment(0, 0),
                bgcolor=ft.Colors.WHITE,
                width=250,
                height=250,
                border_radius=10,
                ink=True,
                on_click=open_picker,
            ),

            ft.Container(
                content=ft.Image(
                    src="arrowtotheright.png",
                    height=160,
                    fit="contain",
                ),
                height=250,
                width=120,
                alignment=ft.alignment.Alignment(0, 0),
            ),

            ft.Container(
                content=ft.Column([result_text, confidence_label, confidence_bar],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=10,
                padding=10,
                border=ft.border.all(5, ft.Colors.BLACK),
                alignment=ft.alignment.Alignment(0, 0),
                bgcolor=ft.Colors.WHITE,
                width=320,
                height=200,
                border_radius=10,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    predict_button = ft.Container(
        ft.Column([predict_btn, processing],
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.Alignment(0, 0),
    )

    history_section = ft.Column(
        [ft.Text("Detection History", weight=ft.FontWeight.BOLD, color="#000000"), history_list],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # --- Stack background + controls ---
    page.add(
        ft.Stack(
            [
                ft.Container(
                    width=1280,        # match page.window.width
                    height=720,        # match page.window.height
                    image=ft.DecorationImage(
                        src="crackdetection.png",
                        fit=ft.BoxFit.COVER
                    )
                ),
                ft.Column(
                    [title_text, selected_image, predict_button, history_section],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            width=1280,    # give the Stack explicit dimensions too
            height=720,
        )
    )
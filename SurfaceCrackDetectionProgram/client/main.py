import flet as ft
import websockets
import asyncio
import base64
import json
import tempfile


def main(page: ft.Page):
    page.title = "Surface Crack Detection System"
    page.scroll = "adaptive"

    page.window.width = 900
    page.window.height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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

    async def open_picker(e: ft.Event[ft.Control]):
        try:
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

        except Exception as ex:
            result_text.value = f"Failed to pick image: {ex}"
            page.update()

    predict_btn = ft.ElevatedButton(
        content=ft.Text("Analyze Surface"),
        width=170,
        height=50
    )

    async def predict_image(e):
        if not image_holder.src:
            result_text.value = "No image selected."
            page.update()
            return

        predict_btn.disabled = True
        processing.visible = True
        page.update()

        try:
            with open(image_holder.src, "rb") as image_file:
                image_bytes = image_file.read()
                image_data = base64.b64encode(image_bytes).decode("utf-8")
        except Exception as ex:
            result_text.value = f"Failed to read selected image: {ex}"
            predict_btn.disabled = False
            processing.visible = False
            page.update()
            return

        await send_prediction_request(image_data)

        predict_btn.disabled = False
        processing.visible = False
        page.update()

    async def send_prediction_request(image_data: str):
        try:
            async with websockets.connect(
                "ws://127.0.0.1:8000/ws",
                open_timeout=10,
                close_timeout=10,
            ) as websocket:

                await websocket.send(json.dumps({
                    "type": "predict",
                    "data": image_data
                }))

                response = await asyncio.wait_for(websocket.recv(), timeout=20)
                data = json.loads(response)

                if data.get("type") == "prediction":

                    has_crack = data.get("has_crack")
                    crack_count = data.get("crack_count")
                    max_conf = data.get("max_confidence")

                    confidence_bar.value = max_conf / 100
                    confidence_label.value = f"Confidence: {round(max_conf,2)}%"

                    if not has_crack:

                        result_text.value = (
                            "Surface Condition: NORMAL\n"
                            "Cracks Detected: 0"
                        )

                        history_list.controls.append(
                            ft.Text("Normal surface detected")
                        )

                    else:


                        result_text.value = (
                            "Surface Condition: CRACK DETECTED\n"
                            f"Number of Cracks: {crack_count}\n"
                            f"Highest Confidence: {round(max_conf, 2)}%"
                        )

                        history_list.controls.append(
                            ft.Text(
                                f"{crack_count} cracks | {round(max_conf,2)}%"
                            )
                        )

                else:
                    result_text.value = "Server error."

        except (asyncio.TimeoutError, websockets.ConnectionClosedError):
            result_text.value = "Connection timed out."
        except ConnectionRefusedError:
            result_text.value = "Cannot connect to server."
        except Exception as ex:
            result_text.value = f"Client error: {ex}"
        finally:
            page.update()

    predict_btn.on_click = predict_image

    selected_image = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        image_name,
                        image_holder
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                margin=10,
                padding=10,
                border=ft.border.all(5, "#000000"),
                alignment=ft.alignment.Alignment(0, 0),
                bgcolor="#ffffff",
                width=300,
                height=320,
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
                content=ft.Column(
                    [
                        result_text,
                        confidence_label,
                        confidence_bar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                margin=10,
                padding=10,
                border=ft.border.all(5, "#000000"),
                alignment=ft.alignment.Alignment(0, 0),
                bgcolor="#ffffff",
                width=320,
                height=200,
                border_radius=10,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    predict_button = ft.Container(
        ft.Column(
            [
                predict_btn,
                processing
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.Alignment(0, 0),
    )

    history_section = ft.Column(
        [
            ft.Text("Detection History", weight=ft.FontWeight.BOLD),
            history_list
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(
        title_text,
        selected_image,
        predict_button,
        history_section
    )


ft.app(target=main, assets_dir=".")
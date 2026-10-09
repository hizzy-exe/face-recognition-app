import gradio as gr
import requests

API_BASE = "http://localhost:5000"


def enroll_face(image):
    if image is None:
        return "Please upload an image."

    try:
        with open(image, "rb") as f:
            files = {"image": ("enroll.jpg", f, "image/jpeg")}
            r = requests.post(f"{API_BASE}/enroll", files=files, timeout=60)

        data = r.json()
        if r.status_code == 200:
            return f"Success: {data.get('message', 'Face enrolled')}"
        return f"Error: {data.get('error', 'Enrollment failed')}"
    except Exception as e:
        return f"API error: {e}"


def verify_face(image):
    if image is None:
        return "Please upload an image."

    try:
        with open(image, "rb") as f:
            files = {"image": ("verify.jpg", f, "image/jpeg")}
            r = requests.post(f"{API_BASE}/verify", files=files, timeout=60)

        data = r.json()
        if r.status_code != 200:
            return f"Error: {data.get('error', 'Verification failed')}"

        if data.get("reason") == "no_face_detected":
            return "No face detected in the image."

        if data.get("verified"):
            return f"MATCH (distance: {data.get('distance', 0):.3f})"
        return f"NO MATCH (distance: {data.get('distance', 0):.3f})"
    except Exception as e:
        return f"API error: {e}"


def check_status():
    try:
        r = requests.get(f"{API_BASE}/status", timeout=10)
        data = r.json()
        return "Enrolled face: YES" if data.get("enrolled") else "Enrolled face: NO"
    except Exception:
        return "API offline"


with gr.Blocks(title="Face Recognition Lab") as demo:
    gr.Markdown("# Face Recognition Lab")
    gr.Markdown("1) Enroll a face  2) Upload another image to verify")

    status_box = gr.Textbox(label="Status", value="Click refresh status")
    gr.Button("Refresh status").click(fn=check_status, outputs=status_box)

    with gr.Tab("Enroll"):
        enroll_img = gr.Image(type="filepath", label="Drop enrollment photo")
        enroll_btn = gr.Button("Enroll Face")
        enroll_out = gr.Textbox(label="Result")
        enroll_btn.click(fn=enroll_face, inputs=enroll_img, outputs=enroll_out)

    with gr.Tab("Verify"):
        verify_img = gr.Image(type="filepath", label="Drop photo to verify")
        verify_btn = gr.Button("Verify Face")
        verify_out = gr.Textbox(label="Result")
        verify_btn.click(fn=verify_face, inputs=verify_img, outputs=verify_out)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
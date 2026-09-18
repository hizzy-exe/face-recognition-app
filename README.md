# Face Recognition App (Because Windows and ML Libraries Hate Each Other)

Look, if you’ve ever tried installing deep learning libraries natively on Windows, you already know it’s an absolute nightmare. Between the C++ compiler errors, `dlib` failing to build, and Python version mismatches, it’s just not worth the headache. So instead of wrestling with system paths and breaking my local machine, I did the sensible thing and shoved the entire DeepFace engine inside a Docker container so it works instantly without touching my actual OS.

Basically, this project uses a decoupled setup. The heavy lifting happens inside an isolated Linux image running a Flask API, while my local machine just runs a lightweight webcam script that pushes video frames over a network loop. It looks sophisticated to recruiters, but honestly, it was just the easiest way to bypass a massive setup headache.

## How the Pieces Fit Together

The architecture is pretty straightforward, mostly because I didn't want to overcomplicate it:

*   **The Backend (`face-recognition-api/`):** A Flask server packed with DeepFace and TensorFlow running on a stable Python 3.10 Linux image. It takes incoming images, runs them against a reference portrait using the VGG-Face model, and spits back a quick verification response.
*   **The Client (`client.py`):** A lightweight script running on the host machine that grabs webcam frames using OpenCV, packs them into HTTP POST requests, and streams them directly to the container. 

This means your host computer doesn’t get bogged down compiling heavy machine learning graphs locally—the container handles the grind.

## Launching the Stack

### 1. Booting the Infrastructure
Instead of typing out long terminal strings with a dozen parameter flags, I threw together a Docker Compose config so you can spin up the entire pipeline with a single command:

```bash
docker compose up --build
```

*(Just a heads up: the first time you run this, the terminal is going to look completely frozen for about a minute. Don't panic or close it, it's just pulling down the massive pre-trained VGG-Face weights file from the cloud. Once it finishes, the server logs will activate.)*

### 2. Starting the Webcam Stream
Once the container logs say the server is active on port 5000, open up a completely separate terminal tab (so we don't mess up the active backend stream) and launch the capture pipeline:

```bash
pip install opencv-python requests
python face-recognition-api/client.py
```

## Making It Actually Work

1. Drop a clear, front-facing photo of yourself right into the `face-recognition-api` directory and make sure it’s named exactly `reference.JPG`.
2. Spin up the stack using the commands above and look directly at your camera lens.
3. The client script will start hammering the API with frame buffers, dynamically painting a green `MATCH!` overlay across your face if the facial distance metrics check out, or a red `NO MATCH` box if the camera is pointing at a wall or a different person.

## This Was My First Time Creating An API

## Enjoy

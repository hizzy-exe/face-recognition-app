Professional rewrite of `face-recognition-app/README.md`

```markdown
# Face Recognition Application

A containerized face verification system that runs facial recognition inference inside a Docker environment and streams webcam frames from the host for real-time matching.

The solution isolates heavy machine learning dependencies (DeepFace + TensorFlow) in a Linux container while keeping the client lightweight. This design avoids common Windows-native installation issues with deep learning libraries and provides a clean separation between inference and capture.

## Architecture

- **Backend** (`face-recognition-api/`): Flask API running DeepFace with the VGG-Face model inside a Docker container. Accepts image frames and returns verification results against a reference image.
- **Client** (`face-recognition-api/client.py`): Lightweight host-side script that captures webcam frames with OpenCV and posts them to the API.
- **Orchestration**: Docker Compose for single-command startup.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ on the host (for the client script only)
- A clear, front-facing reference image named `reference.JPG` placed in the `face-recognition-api/` directory

## Quick Start

1. Build and start the inference service:
   ```bash
   docker compose up --build
   The first run downloads the VGG-Face model weights and may take one to two minutes.

2. In a separate terminal, install client dependencies and start the webcam stream:
   pip install opencv-python requests
   python face-recognition-api/client.py

3. Position yourself in front of the camera. The client displays a green MATCH overlay when      the face matches the reference image, or a red NO MATCH overlay otherwise.


## Project Structure

face-recognition-app/
├── docker-compose.yml
├── face-recognition-api/
│   ├── Dockerfile
│   ├── app.py              # Flask inference server
│   ├── client.py           # Host-side webcam client
│   ├── requirements.txt
│   └── reference.JPG       # Reference image (user-provided)
└── README.md

## Notes

The API is bound to 127.0.0.1:5000 by default for local use.
This project demonstrates a practical approach to packaging computer vision workloads with Docker and exposing them via a simple HTTP API.

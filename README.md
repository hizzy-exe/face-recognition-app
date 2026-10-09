# Face Recognition Application

Containerized face enrollment and verification system using DeepFace, Flask, and Gradio.

Users enroll a face by uploading a photo, then verify later uploads against the enrolled face. Face detection runs first; DeepFace is only called when a face is present.

## Features

- No hardcoded reference image required
- `/enroll` endpoint to register a face
- `/verify` endpoint to compare against the enrolled face
- Face detection gate before verification
- Gradio UI with drag-and-drop upload

## Architecture

- **API** (`app.py`): Flask service for enroll + verify
- **UI** (`gradio_app.py`): Gradio frontend for uploads
- **Model**: DeepFace with VGG-Face
- **Packaging**: Docker Compos

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ on the host (for the client script only)

## Quick Start

### Option A: Docker Compose

docker compose up --build

API: http://localhost:5000
UI: http://localhost:7860

### Option B: Local

cd face-recognition-api
pip install -r requirements.txt
python app.py

In another terminal:
python gradio_app.py

Open http://localhost:7860

## Usage

Open the Enroll tab and upload a clear face photo
Open the Verify tab and upload another photo
View match / no match result

## API

POST /enroll — form-data field image
POST /verify — form-data field image
GET /status — whether a face is enrolled

## Project Structure

face-recognition-app/
├── docker-compose.yml
├── face-recognition-api/
│   ├── Dockerfile
│   ├── app.py
│   ├── gradio_app.py
│   └── requirements.txt
└── README.md

## Notes

- The API is bound to 127.0.0.1:5000 by default for local use
- This project demonstrates packaging computer vision workloads with Docker and exposing them via a simple HTTP API

## License

This project is provided for educational and portfolio purposes.

###  Make sure Gradio file exists and is tracked
If 'face-recognition-api/gradio_app.py' exists locally:

'''bash
git add face-recognition-api/gradio_app.py



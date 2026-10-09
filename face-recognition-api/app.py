import os
import numpy as np
from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2

app = Flask(__name__)

ENROLLED_PATH = "enrolled.jpg"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def read_image_from_request(file_storage):
    data = file_storage.read()
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def has_face(image) -> bool:
    try:
        faces = DeepFace.extract_faces(image, detector_backend="opencv", enforce_detection=True)
        return len(faces) > 0
    except Exception:
        return False


@app.route("/enroll", methods=["POST"])
def enroll():
    if "image" not in request.files:
        return jsonify({"error": "Missing 'image' file"}), 400

    img = read_image_from_request(request.files["image"])
    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    if not has_face(img):
        return jsonify({"error": "No face detected in enrollment image"}), 400

    cv2.imwrite(ENROLLED_PATH, img)
    return jsonify({"status": "enrolled", "message": "Face enrolled successfully"}), 200


@app.route("/verify", methods=["POST"])
def verify():
    if "image" not in request.files:
        return jsonify({"error": "Missing 'image' file"}), 400

    if not os.path.exists(ENROLLED_PATH):
        return jsonify({"error": "No enrolled face. Call /enroll first."}), 400

    img = read_image_from_request(request.files["image"])
    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    if not has_face(img):
        return jsonify({
            "verified": False,
            "reason": "no_face_detected",
            "message": "No face detected in verification image"
        }), 200

    try:
        result = DeepFace.verify(img, ENROLLED_PATH, model_name="VGG-Face", detector_backend="opencv")
        return jsonify({
            "verified": bool(result["verified"]),
            "distance": float(result["distance"]),
            "threshold": float(result["threshold"]),
            "model": result.get("model", "VGG-Face"),
            "reason": "match" if result["verified"] else "no_match"
        }), 200
    except ValueError:
        return jsonify({
            "verified": False,
            "reason": "no_face_detected",
            "message": "Face could not be processed"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "enrolled": os.path.exists(ENROLLED_PATH)
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
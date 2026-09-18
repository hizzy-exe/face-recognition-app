import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from deepface import DeepFace

app = Flask(__name__)
REFERENCE_PATH = "reference.JPG"

@app.route('/verify', methods=['POST'])
def verify_face():
    if 'image' not in request.files:
        return jsonify({"error": "Missing 'image' file in request form-data"}), 400
        
    file = request.files['image']
    
    try:
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({"error": "Invalid or corrupted image format"}), 400

        result = DeepFace.verify(frame, REFERENCE_PATH, model_name="VGG-Face")
        
        return jsonify({
            "verified": bool(result["verified"]),
            "distance": float(result["distance"]),
            "threshold": float(result["threshold"]),
            "model": result["model"]
        }), 200

    except ValueError:
        return jsonify({"error": "Face could not be detected in one of the images"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal processing error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

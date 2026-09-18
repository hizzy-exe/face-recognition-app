import cv2
import requests

# URL of your Dockerized Face Recognition API
URL = "http://localhost:5000/verify"

# open local webcam stream
cap = cv2.VideoCapture(0)

print("Starting live client. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. compress the live frame into JPG format memory buffer
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        continue

    # 2. convert to binary bytes payload
    image_bytes = encoded_image.tobytes()

    try:
        # 3. stream the image payload to the Docker container endpoint
        files = {'image': ('live_frame.jpg', image_bytes, 'image/jpeg')}
        response = requests.post(URL, files=files)
        
        if response.status_code == 200:
            data = response.json()
            is_verified = data.get("verified", False)
            distance = data.get("distance", 1.0)
            
            # 4. display the matching result on screen
            if is_verified:
                label = f"MATCH! (Dist: {distance:.2f})"
                color = (0, 255, 0) # Green
            else:
                label = f"NO MATCH (Dist: {distance:.2f})"
                color = (0, 0, 255) # Red
        else:
            label = f"Error: {response.json().get('error', 'Unknown')}"
            color = (0, 165, 255) # Orange

    except Exception as e:
        label = "API Offline / Connecting..."
        color = (0, 0, 255)

    # render label text overlay onto your live camera window
    cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Webcam Client (Sending frames to Docker API)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

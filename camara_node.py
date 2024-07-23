import cv2
import depthai as dai
import threading
from flask import Flask, Response, request, jsonify
from flask_cors import CORS  # Import CORS
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class OakDStream:
    def __init__(self):
        self.pipeline = dai.Pipeline()

        # Set up the color camera
        self.cam_rgb = self.pipeline.createColorCamera()
        self.cam_rgb.setPreviewSize(640, 480)  # Lower resolution for faster transmission
        self.cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)
        self.cam_rgb.setInterleaved(False)
        self.cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)

        # Create output for the camera
        self.xout_rgb = self.pipeline.createXLinkOut()
        self.xout_rgb.setStreamName("rgb")
        self.cam_rgb.video.link(self.xout_rgb.input)

        self.frame = None
        self.running = True
        self.lock = threading.Lock()

    def start(self):
        self.device = None
        try:
            self.device = dai.Device(self.pipeline)
            self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()
        except Exception as e:
            print(f"Failed to start device: {e}")
            self.running = False
        return self

    def update(self):
        while self.running:
            if self.device is None:
                continue
            try:
                in_rgb = self.q_rgb.get()  # Blocking call, will wait until new data has arrived
                frame = in_rgb.getCvFrame()
                with self.lock:
                    self.frame = frame
            except Exception as e:
                print(f"An error occurred while fetching frame: {e}")

    def get_frame(self):
        with self.lock:
            return self.frame

    def stop(self):
        self.running = False
        if self.device:
            self.device.close()
        if self.thread.is_alive():
            self.thread.join()

# Initialize the OAK-D stream
stream = OakDStream().start()

hsv_values = {
    "h_min": 35,
    "h_max": 85,
    "s_min": 100,
    "s_max": 255,
    "v_min": 100,
    "v_max": 255
}

@app.route('/video_normal')
def video_feed1():
    def generate_frames():
        while True:
            frame = stream.get_frame()
            if frame is not None:
                # Apply HSV filtering
                # hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # lower = (hsv_values['h_min'], hsv_values['s_min'], hsv_values['v_min'])
                # upper = (hsv_values['h_max'], hsv_values['s_max'], hsv_values['v_max'])
                # mask = cv2.inRange(hsv_frame, lower, upper)
                # result = cv2.bitwise_and(frame, frame, mask=mask)
                
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Reduce JPEG quality for faster transmission
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)  # Add a small delay to reduce CPU usage
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_mask')
def video_feed2():
    def generate_frames():
        while True:
            frame = stream.get_frame()
            if frame is not None:
                # Apply HSV filtering
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower = (hsv_values['h_min'], hsv_values['s_min'], hsv_values['v_min'])
                upper = (hsv_values['h_max'], hsv_values['s_max'], hsv_values['v_max'])
                mask = cv2.inRange(hsv_frame, lower, upper)
                
                
                ret, buffer = cv2.imencode('.jpg', mask, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Reduce JPEG quality for faster transmission
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)  # Add a small delay to reduce CPU usage
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_combined')
def video_feed3():
    def generate_frames():
        while True:
            frame = stream.get_frame()
            if frame is not None:
                # Apply HSV filtering
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower = (hsv_values['h_min'], hsv_values['s_min'], hsv_values['v_min'])
                upper = (hsv_values['h_max'], hsv_values['s_max'], hsv_values['v_max'])
                mask = cv2.inRange(hsv_frame, lower, upper)
                result = cv2.bitwise_and(frame, frame, mask=mask)
                
                ret, buffer = cv2.imencode('.jpg', result, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Reduce JPEG quality for faster transmission
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)  # Add a small delay to reduce CPU usage
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/hsv', methods=['GET', 'POST'])
def hsv():
    global hsv_values
    
    if request.method == 'POST':
        data = request.json
        hsv_values.update(data)
        return jsonify(hsv_values)
    else:
        return jsonify(hsv_values)

@app.route('/')
def index():
    return "OAK-D Stream Server"

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5004, threaded=True)
    except KeyboardInterrupt:
        stream.stop()
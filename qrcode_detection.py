import cv2
import numpy as np
from pyzbar.pyzbar import decode
import depthai as dai
import threading


# Global variable for the latest frame
latest_frame = None


def decode_barcodes(frame):
    for barcode in decode(frame):
        myData = barcode.data.decode("utf-8")
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 0, 255), 3)
        pts2 = barcode.rect
        cv2.putText(
            frame,
            myData,
            (pts2[0], pts2[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,  # Font size
            (0, 0, 255),
            2,
        )


def frame_grabber(qVideo):
    global latest_frame
    while True:
        inVideo = qVideo.tryGet()  # Non-blocking call, returns None if no data
        if inVideo is not None:
            latest_frame = inVideo.getCvFrame()


# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.createColorCamera()
xoutVideo = pipeline.createXLinkOut()

xoutVideo.setStreamName("video")

# Properties
camRgb.setPreviewSize(640, 480)
camRgb.setInterleaved(False)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setFps(120)  # Set FPS to 120

# Linking
camRgb.preview.link(xoutVideo.input)

# Connect and start the pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the frames from the output defined above
    qVideo = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Start frame grabber thread
    frame_thread = threading.Thread(target=frame_grabber, args=(qVideo,))
    frame_thread.daemon = True
    frame_thread.start()

    while True:
        if latest_frame is not None:
            img = latest_frame.copy()
            decode_barcodes(img)
            cv2.imshow("Result", img)

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()
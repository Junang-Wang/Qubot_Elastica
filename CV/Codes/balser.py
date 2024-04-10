''' 
pip install pypylon
pip install opencv-python
'''

from pypylon import pylon
import cv2
import numpy as np

# Color range for tracking (adjust as needed)
green_lower = np.array([35, 43, 46])
green_upper = np.array([77, 255, 255])

# Create camera object
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Start grabbing (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
camera.ExposureAuto.SetValue = 'Off'
camera.ExposureTimeRaw.SetValue(30000)
# Set image format converter
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Set camera parameters (adjust as needed)
# camera.Width.SetValue = 1000
# camera.Height.SetValue = 500
# camera.OffsetX.Value = 0
# camera.OffsetY.Value = 0

while camera.IsGrabbing():
    # Grab the latest image
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert image to OpenCV format
        image = converter.Convert(grabResult)
        frame = image.GetArray()

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create color mask
        mask = cv2.inRange(hsv, green_lower, green_upper)

        # Remove noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in color mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Track the largest contour
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            x = x + w // 2
            y = y + h // 2
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
            cv2.putText(frame, f"End: ({x:.2f}, {y:.2f})", (int(x) + 5, int(y) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Display result
        cv2.imshow('Guidewire Tracking', frame)

        # Exit on 'q' press
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    grabResult.Release()

# Release resources
camera.StopGrabbing()
cv2.destroyAllWindows()
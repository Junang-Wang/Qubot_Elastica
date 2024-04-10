from pypylon import pylon
import cv2

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

# # Set camera parameters (adjust as needed)
# camera.Width.SetValue = 1000
# camera.Height.SetValue = 500
# camera.OffsetX.Value = 0
# camera.OffsetY.Value = 0

# Continuously grab and display frames
while camera.IsGrabbing():
    # Grab the latest image
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert image to OpenCV format
        image = converter.Convert(grabResult)
        frame = image.GetArray()

        # Display the frame
        cv2.imshow('Basler Camera Stream', frame)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release grab result
    grabResult.Release()

# Stop grabbing and release resources
camera.StopGrabbing()
cv2.destroyAllWindows()
import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)  # Use default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # Threshold the image to binarize it
    _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours were found
    if contours:
        # Get the largest contour
        max_contour = max(contours, key=cv2.contourArea)

        # Find the centroid of the largest contour
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Draw a circle at the centroid
            cv2.circle(frame, (cx, cy), 10, (0, 255, 255), -1)

            # Check for gestures (e.g., hand open, closed fist)
            # Implement gesture recognition logic here

    # Display the frame
    cv2.imshow("Frame", frame)

    # Exit on ESC
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

# Example gesture recognition logic
if cx < 200:
    pyautogui.hotkey('ctrl', 'left')  # Example action: Ctrl + Left Arrow
elif cx > 440:
    pyautogui.hotkey('ctrl', 'right')  # Example action: Ctrl + Right Arrow
elif cy < 150:
    pyautogui.hotkey('ctrl', 'up')  # Example action: Ctrl + Up Arrow
elif cy > 330:
    pyautogui.hotkey('ctrl', 'down')  # Example action: Ctrl + Down Arrow

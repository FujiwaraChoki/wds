import cv2
import time

class MOD:
    def __init__(self, cam_index: int = 0, on_detect: function = lambda x, y, w, h: print(x, y, w, h), timeout: int = 2):
        # Initialize camera
        self.cap = cv2.VideoCapture(cam_index)

        # Initialize background subtractor
        self.backSub = cv2.createBackgroundSubtractorMOG2()

        # Initialize on_detect callback
        self.on_detect = on_detect

        # Set timeout in seconds
        self.timeout = timeout

    def detect_motion(self):
        passed_time = 0
        while True:
            if passed_time >= self.timeout:
                break

            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # Apply background subtraction
            fgMask = self.backSub.apply(frame)

            # Find contours of moving objects
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw rectangles around moving objects
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if x > 0 and y > 0 and w > 0 and h > 0:
                        self.on_detect(x, y, w, h)

            # Display the resulting frame
            cv2.imshow('Motion Detection', frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
            # Increment passed time by a second
            time.sleep(1)
            passed_time += 1

    def release(self):
        # Release the capture
        self.cap.release()
        cv2.destroyAllWindows()

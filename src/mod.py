'''
Moving Object Detection (MOD)

This module is responsible for detecting moving objects in a video stream.
'''
import cv2
import numpy
import matplotlib.pyplot as plt

class MOD:
    def __init__(self, camera_index=0, on_detect=None):
        '''
        Initialize the MOD class with the camera index.
        '''
        self.cap = cv2.VideoCapture(camera_index)
        self.selected_frames = []

    def _color_convert(self, image):
        '''
        Convert the image to COLOR_BGR2RGB.
        '''
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def _select_30_frames(self):
        '''
        Extract 30 random frames and store the selected frames in an array.
        '''
        frame_count = 0
        
        while frame_count < 30:
            ret, frame = self.cap.read()
            if ret:
                self.selected_frames.append(frame)
                frame_count += 1

    def run(self):
        ''''
        Run the MOD algorithm.
        '''
        self._select_30_frames()
        
        frame_median = numpy.median(self.selected_frames, axis=0).astype(dtype=numpy.uint8)
        frame_sample = self.selected_frames[0]
        
        gray_frame_median = cv2.cvtColor(frame_median, cv2.COLOR_BGR2GRAY)
        gray_frame_sample = cv2.cvtColor(frame_sample, cv2.COLOR_BGR2GRAY)
        
        bg_removed_frame = cv2.absdiff(gray_frame_sample, gray_frame_median)

        frame_blur = cv2.GaussianBlur(bg_removed_frame, (11, 11), 0)

        ret, frame_threshold = cv2.threshold(frame_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        (contours, _) = cv2.findContours(frame_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            cv2.rectangle(frame_sample, (x, y), (x + width, y + height), (123, 0, 255), 2)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Converting frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Calculating Absolute Difference between Current Frame and Median Frame
            dframe = cv2.absdiff(gray_frame, gray_frame_median)
            # Applying Gaussian Blur to reduce noise
            blur_frame = cv2.GaussianBlur(dframe, (11, 11), 0)
            # Binarizing frame - Thresholding
            ret, threshold_frame = cv2.threshold(blur_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # Identifying Contours
            (contours, _) = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Drawing Boundary Boxes for each Contour
            for contour in contours:
                x, y, width, height = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + width, y + height), (123, 0, 255), 2)
                if on_detect:
                    on_detect(width, height, x, y)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Releasing Video Object
        self.cap.release()
        cv2.destroyAllWindows()

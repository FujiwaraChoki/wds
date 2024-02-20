import cv2
from mod import MOD
from termcolor import colored

def show_available_cameras():
    num_cameras = 10  # You can adjust this number if you have more than 10 cameras
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            continue
        print(f"Camera {i}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        cap.release()

def main():
  show_available_cameras()
  camera_index = int(input('Enter the camera index: '))

  print(colored('Starting MOD algorithm...', 'green'))
  mod = MOD(camera_index)
  mod.run()
  print(colored('MOD algorithm completed.', 'green'))

if __name__ == '__main__':
  main()
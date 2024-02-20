import cv2
import asyncio

from mod import MOD
from playsound import playsound

def show_available_cameras():
    num_cameras = 10  # You can adjust this number if you have more than 10 cameras
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            continue
        print(f"Camera {i}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        cap.release()

def on_detect(x, y, w, h):
    print(f'Shooting Object at {x}, {y} with width {w} and height {h}')
    # asynchronously play the sound
    # New event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # run without waiting to finish
    loop.run_in_executor(None, playsound, 'gunshot.mp3')

def main():
  show_available_cameras()
  camera_index = int(input('Enter the camera index: '))

  print('Starting MOD algorithm...')
  mod = MOD(camera_index, on_detect)
  mod.detect_motion()
  print('MOD algorithm completed.')

if __name__ == '__main__':
  main()

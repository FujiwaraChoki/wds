import cv2
import time
import pyttsx3
import pyaudio
import asyncio
import numpy as np
import scipy.signal as signal

from mod import MOD
from termcolor import colored
from playsound import playsound

def show_available_cameras():
    num_cameras = 10  # You can adjust this number if you have more than 10 cameras
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            continue
        print(f'Camera {i}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')
        cap.release()

show_available_cameras()
camera_index = int(input(colored('Enter the camera index: ', 'magenta')))
# Constants
FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=1,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

directions = []

ENGINE = pyttsx3.init()

def on_detect(x, y, w, h):
  print(colored(f'Detected movement at ({x}, {y}) with width={w} and height={h}. Shooting!', 'green'))
  # New event loop
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  # run without waiting to finish
  loop.run_in_executor(None, playsound, 'gunshot.mp3')
  ENGINE.say('Opening fire.')
  ENGINE.runAndWait()

print(colored('Listening...', 'magenta'))

average_freq = 0

try:
    while True:
        # Read chunk of data from stream
        data = stream.read(CHUNK)
        
        # Convert data to numpy array
        data_np = np.frombuffer(data, dtype=np.int16)
        
        # Apply beamforming
        
        # Compute the power spectral density (PSD) of the signal
        f, t, Sxx = signal.spectrogram(data_np, fs=RATE, nperseg=512)  # Increased resolution
        
        # Set beamforming weights based on the frequency components
        # For simplicity, we'll just use a cosine window
        window = np.cos(np.linspace(0, np.pi, len(f)))  # Adjust window shape as needed
        
        # Apply beamforming by multiplying the PSD by the window
        Sxx_beamformed = Sxx * window[:, np.newaxis]
        
        # Integrate beamformed PSD over frequency
        integrated_power = np.sum(Sxx_beamformed, axis=0)
        
        # Find the time segment with maximum integrated power
        max_power_index = np.argmax(integrated_power)
        estimated_direction = t[max_power_index] * 360 * 10 # Convert to degrees

        directions.append(estimated_direction)
        
        # Get frequency of sound
        freq, Pxx = signal.welch(data_np, fs=RATE, nperseg=1024)  # Higher-order spectrogram
        max_freq = freq[np.argmax(Pxx)]

        if average_freq == 0:
            average_freq = max_freq
        else:
            # Calculate new average
            average_freq = (average_freq + max_freq) / 2
        
        if 0 <= max_freq <= average_freq + 2000:
            print(colored(f'=> No usual activity: {max_freq}', 'cyan'))

            time.sleep(1)
        else:
            print(colored(f'Detected sound with abnormal frequency: {max_freq}Hz at {estimated_direction}°.', 'green'))  
            print(colored(f'=> Turning to {estimated_direction}°', 'blue'))
            print(colored('=> Detecting movement...', 'yellow'))

            mod = MOD(0, on_detect=on_detect) # Use default camera index (0)
            mod.detect_motion()
        
except KeyboardInterrupt:
    print('Stopped listening.')

# Close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Calculate average
average_direction = np.mean(directions)

print(colored('Average Direction:', 'cyan'), average_direction)

# The most often direction
most_often_direction = max(set(directions), key=directions.count)

print(colored('Most Often Direction:', 'cyan'), most_often_direction)

# Importing all necessary libraries
import cv2
import os
import argparse
import hashlib
from pathlib import Path
from math import floor

def get_full_timestamp(millis):
    if millis == 0:
        return '00.00.00.000'
    seconds=(millis/1000)%60
    seconds = str(int(seconds)).zfill(2)
    minutes= (millis/(1000*60))%60
    minutes = str(int(minutes)).zfill(2)
    hours = (millis/(1000*60*60)) % 24
    hours = str(int(hours)).zfill(2)
    return f'{hours}.{minutes}.{seconds}.{str(floor(millis % 1000)).zfill(3)}'

# Read the video from specified path
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('-c', '--captures-per-second', type=int, default=2)
parser.add_argument('-q', '--quality', type=int, default=100)
args = parser.parse_args()
file_path = args.file
quality = args.quality
cam = cv2.VideoCapture(file_path)

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

with open(file_path, "rb") as f:
  file_hash = hashlib.md5(f.read()).hexdigest()
  Path(f'./data/{file_hash}').mkdir(parents=True, exist_ok=True)

# frame
current_frame = 0
frames_per_second = round(cam.get(cv2.CAP_PROP_FPS) / 10) * 10

if args.captures_per_second > frames_per_second:
    print(f'Specified frames to capture per second exceeds FPS; capturing the maximum possible of {frames_per_second} frames per second.')
captures_per_second = min(args.captures_per_second, frames_per_second)
millisecs_per_frame = 1000 / frames_per_second
frames_to_jump = (frames_per_second - (frames_per_second % captures_per_second)) // captures_per_second
print(f'Frames per second: {frames_per_second}')
print(f'Captures per second: {captures_per_second}\nFrames to jump per iteration: {frames_to_jump}')
print(f'Quality of exported frames: {quality}%')

while (True):
    # reading from frame
    ret, frame = cam.read()
    
    # TODO: PICK UP FROM WHERE THE FRAME CAPTURE WAS LEFT OFF

    if ret:
        timestamp_milliseconds = current_frame * millisecs_per_frame
        # TODO: CREATE FUNCTION TO CONVERT TO HH:MM:SS:mmm FROM MILLISECONDS
        timestamp = get_full_timestamp(timestamp_milliseconds)
        # if video is still left continue creating images
        name = f'./data/{file_hash}/{timestamp}.jpg'
        print(f'Creating {name}')

        # writing the extracted images
        cv2.imwrite(name, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

        # Skip frames according to how many captures per second were specified
        current_frame += frames_to_jump
        cam.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
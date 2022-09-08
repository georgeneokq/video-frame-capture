# Importing all necessary libraries
import cv2
import os
import argparse
import hashlib

# Read the video from specified path
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True)
args = parser.parse_args()
file_path = args.file
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

# frame
current_frame = 0

while (True):
    # reading from frame
    ret, frame = cam.read()
    
    # TODO: PICK UP FROM WHERE THE FRAME CAPTURE WAS LEFT OFF

    if ret:
        # if video is still left continue creating images
        name = f'./data/{file_hash}/{current_frame}.jpg'
        print('Creating...' + name)

        # writing the extracted images
        cv2.imwrite(name, frame)

        # increasing counter so that it will
        # show how many frames are created
        current_frame += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
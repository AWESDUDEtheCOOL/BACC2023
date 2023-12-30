"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename.

A GitHub function and image name generator have been provided for you. You may create 
your own functions for these tasks if you wish, but it is not required. You will need 
to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: 
#DATE:

#import libraries
import time
import os
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

#VARIABLES
THRESHOLD = 0       #Any desired value from the accelerometer
REPO_PATH = ""      #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = ""    #Your image folder path in your GitHub repo: ex. /home/pi/FlatSatChallenge/Images/

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo = Repo(REPO_PATH)
        repo.git.add(FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname


def take_photo():
    """
    This function is complete. Takes a photo when the FlatSat is shaken.
    """
    accelX, accelY, accelZ = accel_gyro.acceleration
    if accelX > THRESHOLD or accelY > THRESHOLD or accelZ > THRESHOLD:
        time.sleep(5)
        #Take/save/upload a picture 
        name = "MasonM"     #Last Name, First Initial  ex. MasonM
        imgname = img_gen(name)
        picam2.start_and_capture_file(imgname)
        git_push()


def main():
    while True:
        take_photo()


if __name__ == '__main__':
    main()
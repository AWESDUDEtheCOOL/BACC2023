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
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

#VARIABLES
THRESHOLD = 15       #Any desired value from the accelerometer
REPO_PATH = "/home/pi/BACC2023"      #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "/Images"    #Your image folder path in your GitHub repo: ex. /Images

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
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
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
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        if accelx > THRESHOLD or accely > THRESHOLD or accelz > THRESHOLD:
            print('photo')
            time.sleep(1)
            #Take/save/upload a picture 
            name = "MasonM"     #Last Name, First Initial  ex. MasonM
            imgname = img_gen(name)
            picam2.start(show_preview=False)
            picam2.capture_file(imgname)
            picam2.stop()
            git_push()
        
        time.sleep(1)


def main():
    take_photo()


if __name__ == '__main__':
    main()
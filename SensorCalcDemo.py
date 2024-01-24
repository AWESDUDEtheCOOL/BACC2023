#sensor_calc.py
import time
import numpy as np
import time
import os
import board
import busio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL


i2c = busio.I2C(board.SCL, board.SDA)
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)


#Activity 1: RPY based on accelerometer and magnetometer
def pitch_am(accelX,accelY,accelZ):
    pitch = np.arctan2(accelX, np.sqrt(accelY**2 + accelZ**2))
    return np.rad2deg(pitch)

def roll_am(accelX,accelY,accelZ):
    roll = np.arctan2(accelY, np.sqrt(accelX**2 + accelZ**2))
    return np.rad2deg(roll)

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    pitch = np.deg2rad(pitch_am(accelX,accelY,accelZ))
    roll = np.deg2rad((accelX,accelY,accelZ))
    mag_x = (magX*np.cos(pitch)) + (magY*np.sin(roll)*np.sin(pitch)) + (magZ*np.cos(roll)*np.cos(pitch))
    mag_y = (magY*np.cos(roll)) - (magZ*np.sin(roll))
    return np.rad2deg(np.arctan2(-mag_y, mag_x))

#Activity 2: RPY based on gyroscope
def roll_gy(prev_angle, delT, gyro):
    #TODO
    return roll
def pitch_gy(prev_angle, delT, gyro):
    #TODO
    return pitch
def yaw_gy(prev_angle, delT, gyro):
    #TODO
    return yaw

def set_initial(mag_offset = [0,0,0]):
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
    magX, magY, magZ = mag.magnetic #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    offset = calibrate_mag()
    magX = magX - offset[0]
    magY = magY - offset[1]
    magZ = magZ - offset[2]
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    print("Initial angle set.")
    return [roll,pitch,yaw]

def calibrate_mag():
    #TODO: Set up lists, time, etc
    #print("Preparing to calibrate magnetometer. Please wave around.")
    #time.sleep(3)
    #print("Calibrating...")
    #TODO: Calculate calibration constants
   # print("Calibration complete.")
    return [0,0,0]

def calibrate_gyro():
    #TODO
    #print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    #time.sleep(3)
    #print("Calibrating...")
    #TODO
    #print("Calibration complete.")
    return [0, 0, 0]

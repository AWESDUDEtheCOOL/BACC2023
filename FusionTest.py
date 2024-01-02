import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import imufusion
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.animation import FuncAnimation
import csv
import random


i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)


def fusion():
    gyroscope = np.asarray(accel_gyro.gyro)
    accelerometer = np.asarray(accel_gyro.acceleration)

    # Process sensor data
    ahrs = imufusion.Ahrs()
    ahrs.update_no_magnetometer(gyroscope, accelerometer, 1 / 100)  # 100 Hz sample rate
    euler = ahrs.quaternion.to_euler()
    print(gyroscope, accelerometer, euler)
    return gyroscope, accelerometer, euler


fig, axes = plt.subplots(nrows=3, sharex=True)

x = [0,0,0,0,0,0]
gyromemx = [0,0,0,0,0,0]
gyromemy = [0,0,0,0,0,0]
gyromemz = [0,0,0,0,0,0]

accelmemx = [0,0,0,0,0,0]
accelmemy = [0,0,0,0,0,0]
accelmemz = [0,0,0,0,0,0]

eulermemx = [0,0,0,0,0,0]
eulermemy = [0,0,0,0,0,0]
eulermemz = [0,0,0,0,0,0]

# Plot gyroscope data
gyrox, = axes[0].plot(x, gyromemx, color="red", label="X")
gyroy, = axes[0].plot(x, gyromemy, color="green", label="Y")
gyroz, = axes[0].plot(x, gyromemz, color="blue", label="Z")
axes[0].set_title("Gyroscope")
axes[0].set_ylabel("Degrees/s")
axes[0].grid()
axes[0].legend()

# Plot accelerometer data
accelx, = axes[1].plot(x, accelmemx, color="red", label="X")
accely, = axes[1].plot(x, accelmemy, color="green", label="Y")
accelz, = axes[1].plot(x, accelmemz, color="blue", label="Z")
axes[1].set_title("Accelerometer")
axes[1].set_ylabel("g")
axes[1].grid()
axes[1].legend()

# Plot Euler angles
eulerx, = axes[2].plot(x, eulermemx, color="red", label="Roll")
eulery, = axes[2].plot(x, eulermemy, color="green", label="Pitch")
eulerz, = axes[2].plot(x, eulermemz, color="blue", label="Yaw")
axes[2].set_title("Euler angles")
axes[2].set_xlabel("Seconds")
axes[2].set_ylabel("Degrees")
axes[2].grid()
axes[2].legend()



def animate(frame):
    gyroscope, accelerometer, euler = fusion()
    x.pop(0)
    x.append(frame)
    
    #write function that adds value to end of list and removes first value
    
    
    # Update gyroscope plot
    gyromemx.pop(0)
    gyromemx.append(gyroscope[0])
    gyrox.set_data(x, gyromemx)
    gyromemy.pop(0)
    gyromemy.append(gyroscope[1])
    gyroy.set_data(x, gyromemy)
    gyromemz.pop(0)
    gyromemz.append(gyroscope[2])
    gyroz.set_data(x, gyromemz)
    axes[0].relim()
    axes[0].autoscale_view()

    # Update accelerometer plot
    accelmemx.pop(0)
    accelmemx.append(accelerometer[0])
    accelx.set_data(x, accelmemx)
    accelmemy.pop(0)
    accelmemy.append(accelerometer[1])
    accely.set_data(x, accelmemy)
    accelmemz.pop(0)
    accelmemz.append(accelerometer[2])
    accelz.set_data(x, accelmemz)
    axes[1].relim()
    axes[1].autoscale_view()

    # Update Euler angles plot
    eulermemx.pop(0)
    eulermemx.append(np.degrees(euler[0]))
    eulerx.set_data(x, eulermemx)
    eulermemy.pop(0)
    eulermemy.append(np.degrees(euler[1]))
    eulery.set_data(x, eulermemy)
    eulermemz.pop(0)
    eulermemz.append(np.degrees(euler[2]))
    eulerz.set_data(x, eulermemz)
    axes[2].relim()
    axes[2].autoscale_view()

ani = FuncAnimation(fig, animate, frames = np.linspace(1,1000,1000), interval = 1000)
plt.show()
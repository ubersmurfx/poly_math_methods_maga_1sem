import math
import numpy as np
import matplotlib.pyplot as plt


scan = np.loadtxt('./lab1/laserscan.dat')
angle = np.linspace(-math.pi/2, math.pi/2, np.shape(scan)[0], endpoint='true')

x_robot = 1.0
y_robot = 0.5
theta_robot = math.pi / 4

x_laser_local = 0.2
y_laser_local = 0.0
theta_laser_local = math.pi



T_robot_laser = np.array([[np.cos(theta_laser_local), -np.sin(theta_laser_local), x_laser_local],
                        [np.sin(theta_laser_local), np.cos(theta_laser_local), y_laser_local],
                        [0, 0, 1]])


T_global_robot = np.array([[np.cos(theta_robot), -np.sin(theta_robot), x_robot],
                          [np.sin(theta_robot), np.cos(theta_robot), y_robot],
                          [0, 0, 1]])


laser_points_local = np.vstack((scan * np.cos(angle), scan * np.sin(angle), np.ones(len(angle))))



laser_points_global = T_global_robot @ T_robot_laser @ laser_points_local


plt.figure(figsize=(10,10))
plt.plot(laser_points_global[0,:],laser_points_global[1,:],'.',label='Laser scan')
plt.plot(x_robot,y_robot,'ro',label='Robot')
plt.plot(laser_points_global[0,0],laser_points_global[1,0],'go',label='Laser')
plt.xlabel('x (global)')
plt.ylabel('y (global)')
plt.title('Laser Scan and Robot in Global Coordinates')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
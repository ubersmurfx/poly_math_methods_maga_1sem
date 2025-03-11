import numpy as np
import matplotlib.pyplot as plt

def diffdrive(x, y, theta, v_l, v_r, t, l):
    if v_l == v_r:
        x_n = x + v_l * t * np.cos(theta)
        y_n = y + v_l * t * np.sin(theta)
        theta_n = theta
    else:
        R = l * (v_l + v_r) / (2 * (v_r - v_l))
        omega = (v_r - v_l) / l
        x_n = x + R * (np.sin(theta + omega * t) - np.sin(theta))
        y_n = y + R * (np.cos(theta) - np.cos(theta + omega * t))
        theta_n = theta + omega * t

    return x_n, y_n, theta_n


x, y, theta = 1.5, 2.0, np.pi / 2

commands = [
    (0.3, 0.3, 3),  # c1
    (0.1, -0.1, 1), # c2
    (0.2, 0, 2)     # c3
]

l = 0.5

positions = [(x, y, theta)]

for v_l, v_r, t in commands:
    x, y, theta = diffdrive(x, y, theta, v_l, v_r, t, l)
    positions.append((x, y, theta))


x_coords = [pos[0] for pos in positions]
y_coords = [pos[1] for pos in positions]
theta_coords = [pos[2] for pos in positions]

plt.figure(figsize=(8, 6))
plt.quiver(x_coords[:-1], y_coords[:-1],
           np.diff(x_coords), np.diff(y_coords),
           angles='xy', scale_units='xy', scale=1, color='blue')

plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='red')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Траектория робота с дифференциальным приводом')
plt.grid(True)


#Вывод углов
for i, theta_val in enumerate(theta_coords):
    print(f"Положение {i+1}: Угол = {theta_val:.2f} рад")

plt.show()

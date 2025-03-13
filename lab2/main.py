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


def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1))*np.sqrt((x2 - x1)) + (y2 - y1)*(y2 - y1)


x, y, theta = 1.5, 2.0, np.pi / 2

commands = [
    (0.3, 0.3, 3),  # c1
    (0.1, -0.1, 1), # c2
    (0.2, 0, 2)     # c3
]

l = 0.5
step_size = 0.01

positions = [(x, y, theta)]

for v_l, v_r, t_total in commands:
    t = 0
    x_prev = x
    y_prev = y
    while t < t_total:
        dt = min(t_total - t, 0.01) #This line is crucial for controlling the time step
        x_next, y_next, theta_next = diffdrive(x, y, theta, v_l, v_r, dt, l)
        dist = distance(x,y, x_next, y_next)

        if dist >= step_size:
            # Interpolate to get a position exactly at 0.01m
            ratio = step_size/dist
            x_interp = x + ratio * (x_next-x)
            y_interp = y + ratio * (y_next-y)
            theta_interp = theta + ratio * (theta_next - theta)
            positions.append((x_interp, y_interp, theta_interp))
            x, y, theta = x_interp, y_interp, theta_interp
        else:
            positions.append((x_next, y_next, theta_next))
            x, y, theta = x_next, y_next, theta_next
        t += dt

x_coords = [pos[0] for pos in positions]
y_coords = [pos[1] for pos in positions]
theta_coords = [pos[2] for pos in positions]


plt.figure(figsize=(10, 8))
plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='red', label='Trajectory', markersize=3)

plt.xlim(min(x_coords) - 0.5, max(x_coords) + 0.5)
plt.ylim(min(y_coords) - 0.5, max(y_coords) + 0.5)
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Траектория робота с дифференциальным приводом')
plt.grid(True)
plt.legend()


# Add annotations (less frequent for better readability)
for i in range(0, len(positions), 100): #add annotations every 10th point
    x, y, theta = positions[i]
    plt.annotate(f"({x:.2f}, {y:.2f})\nθ={theta:.2f} rad", (x, y), textcoords="offset points", xytext=(5, 5), ha='left')

plt.show()
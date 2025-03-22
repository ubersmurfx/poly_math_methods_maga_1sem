import numpy as np
import matplotlib.pyplot as plt

def odo_process_model(xt, ut, alpha, sampling_method=None):
    x, y, theta = xt
    dr1, dr2, dt = ut
    a1, a2, a3, a4 = alpha
    if sampling_method is None:
        noise = np.random.normal(0, np.array([a1, a2, a3, a4])) # Box-Muller по умолчанию
    else:
        noise = sampling_method(0, np.array([a1*a1, a2*a2, a3*a3, a4*a4]))  # Вариант с другими методами

    noise1, noise2, noise3, noise4 = noise
    
    dr1 += noise1
    dr2 += noise2
    dt += noise3

    x += (dr1 + dr2)/2 * np.cos(theta + dt + noise4)
    y += (dr1 + dr2)/2 * np.sin(theta + dt + noise4)
    theta += dt + noise4
    return np.array([x, y, theta])


xt = np.array([2.0, 4.0, 0.0])
ut = np.array([np.pi/2, 0.0, 1.0])
alpha = np.array([0.1, 0.1, 0.01, 0.01])
n_simulations = 5000

positions = [odo_process_model(xt, ut, alpha) for _ in range(n_simulations)]

x_coords = np.array([pos[0] for pos in positions])
y_coords = np.array([pos[1] for pos in positions])

plt.figure(figsize=(8, 6))
plt.scatter(x_coords, y_coords, s=1, alpha=0.5, label='Robot Positions')
plt.scatter(2.0, 4.0, s=50, label='robot initial pose')

# Calculate and plot the average position
avg_x = np.mean(x_coords)
avg_y = np.mean(y_coords)
plt.scatter(avg_x, avg_y, color='red', s=50, marker='x', label='Average Position')


plt.xlabel("X координата")
plt.ylabel("Y координата")
plt.title("Положения робота (5000 симуляций)")
plt.legend()
plt.xlim(1.75, 2.75)
plt.ylim(3.75, 5)
plt.show()

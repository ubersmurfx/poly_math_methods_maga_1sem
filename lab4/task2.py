import numpy as np
import matplotlib.pyplot as plt

def sample_normal_distribution(std_dev):
    return np.random.normal(0, std_dev)

def motion_model_odometry(x_t, u_t, alpha):
    x, y, theta = x_t
    delta_rot1, delta_trans, delta_rot2 = u_t

    # добавил угол
    delta_rot1_hat = delta_rot1 + sample_normal_distribution(alpha[0] * abs(delta_rot1) + alpha[1] * delta_trans)
    delta_trans_hat = delta_trans + sample_normal_distribution(alpha[2] * delta_trans + alpha[3] * (abs(delta_rot1) + abs(delta_rot2)))
    delta_rot2_hat = delta_rot2 + sample_normal_distribution(alpha[0] * abs(delta_rot2) + alpha[1] * delta_trans)

    # новая поза
    x_new = x + delta_trans_hat * np.cos(theta + delta_rot1_hat)
    y_new = y + delta_trans_hat * np.sin(theta + delta_rot1_hat)
    theta_new = theta + delta_rot1_hat + delta_rot2_hat

    return np.array([x_new, y_new, theta_new])  

x_t = np.array([2.0, 4.0, 0.0])
u_t = np.array([np.pi / 2, 1.0, 0.0])
alpha = np.array([0.1, 0.1, 0.01, 0.01])

num_samples = 5000
samples = np.zeros((num_samples, 2))

for i in range(num_samples):
    x_t1 = motion_model_odometry(x_t, u_t, alpha)
    samples[i] = x_t1[:2]

    # Визуализация
plt.figure(figsize=(8, 8))
plt.scatter(samples[:, 0], samples[:, 1], s=1, alpha=0.5, label='Predicted positions')
plt.plot(x_t[0], x_t[1], 'ro', label='Initial position')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.legend()
plt.title('5000 Samples of Robot Motion Model')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def likelihood(m, d0, d1, x0, x1, sigma0, sigma1):
    dist0 = np.linalg.norm(m - x0)
    dist1 = np.linalg.norm(m - x1)
    p0 = norm.pdf(dist0, loc=d0, scale=sigma0)
    p1 = norm.pdf(dist1, loc=d1, scale=sigma1)
    return p0 * p1

# Данные
m0 = np.array([10, 8])
m1 = np.array([6, 3])
x0 = np.array([12, 4])
x1 = np.array([5, 7])
d0 = 3.9
d1 = 4.5
sigma0 = 1
sigma1 = np.sqrt(1.5)

x = np.arange(0, 15, 0.5)
y = np.arange(0, 10, 0.5)
X, Y = np.meshgrid(x, y)
m = np.vstack((X.ravel(), Y.ravel())).T


Z = np.array([likelihood(m_i, d0, d1, x0, x1, sigma0, sigma1) for m_i in m])
Z = Z.reshape(X.shape)

print(m0[0], m0[1], m1[0], m1[1], x0[0], x0[1], x1[0], x1[1])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)
ax.scatter(m0[0], m0[1], likelihood(m0, d0, d1, x0, x1, sigma0, sigma1), color='red', label='University')
ax.scatter(m1[0], m1[1], likelihood(m1, d0, d1, x0, x1, sigma0, sigma1), color='green', label='Home')
ax.scatter(x0[0], x0[1], 0, color='blue', label='Tower 0')
ax.scatter(x1[0], x1[1], 0, color='purple', label='Tower 1')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Likelihood')
ax.legend()
plt.show()



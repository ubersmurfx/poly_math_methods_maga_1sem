import numpy as np
import matplotlib.pyplot as plt
import pathlib

image_path = pathlib.Path("./lab0/images/myfirstplot.png")

def calculatePos(x):
  return np.cos(x) * np.exp(x)

def plotPos():
  x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
  y = calculatePos(x)

  plt.plot(x, y)
  plt.xlabel("x")
  plt.ylabel("f(x)")
  plt.title("f(x) = cos(x) * exp(x)")
  plt.grid(True)
  
  plt.savefig(image_path)
  plt.show()

def random_generator():
  #(e)
  np.random.seed(42)  
  
  # (a)
  num_samples = 100000
  mean = 5.0
  mean_square_deviation = 2.0
  normal_samples = np.random.normal(loc=mean, scale=mean_square_deviation, size=num_samples)

  # (b)
  low = 0
  high = 10
  uniform_samples = np.random.uniform(low=low, high=high, size=num_samples)

  # (c)
  normal_mean = np.mean(normal_samples)
  normal_std = np.std(normal_samples)
  uniform_mean = np.mean(uniform_samples)
  uniform_std = np.std(uniform_samples)

  print("Нормальное распределение:")
  print(f"  Математическое ожидание: {normal_mean:.2f}")
  print(f"  Среднеквадратичное отклонение: {normal_std:.2f}")
  print("\nРавномерное распределение:")
  print(f"  Математическое ожидание: {uniform_mean:.2f}")
  print(f"  Среднеквадратичное отклонение: {uniform_std:.2f}")

  # (d)
  plt.figure(figsize=(12, 6))

  plt.subplot(1, 2, 1)
  plt.hist(normal_samples, bins=50, density=True, alpha=0.7, label='Гистограмма')
  x = np.linspace(normal_mean - 3 * normal_std, normal_mean + 3 * normal_std, 100)
  y = (1 / (normal_std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - normal_mean) / normal_std)*((x - normal_mean) / normal_std))
  plt.plot(x, y, label='Функция плотности вероятности')
  plt.title("Нормальное распределение")
  plt.xlabel("Значение")
  plt.ylabel("Плотность")
  plt.legend()

  plt.subplot(1, 2, 2)
  plt.hist(uniform_samples, bins=50, density=True, alpha=0.7, label='Гистограмма')
  x = np.linspace(low, high, 100)
  y = np.full(100, 1 / (high - low))  # Плотность для равномерного распределения
  plt.plot(x, y, label='Функция плотности вероятности')
  plt.title("Равномерное распределение")
  plt.xlabel("Значение")
  plt.ylabel("Плотность")
  plt.legend()

  plt.tight_layout()
  plt.show()

def spiral_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1
    direction = 0

    while num <= n * n:
        if direction == 0:
            for i in range(left, right + 1):
                matrix[top][i] = num
                num += 1
            top += 1
        elif direction == 1:
            for i in range(top, bottom + 1):
                matrix[i][right] = num
                num += 1
            right -= 1
        elif direction == 2:
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = num
                num += 1
            bottom -= 1
        elif direction == 3:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = num
                num += 1
            left += 1
        direction = (direction + 1) % 4

    return matrix


def print_matrix(matrix):
    """Prints the matrix in a user-friendly format."""
    for row in matrix:
        for num in row:
            print(str(num).rjust(2), end=" ")
        print()

if __name__=="__main__":
  #plotPos()
  random_generator()
  n = 10
  spiral = spiral_matrix(n)
  print_matrix(spiral)


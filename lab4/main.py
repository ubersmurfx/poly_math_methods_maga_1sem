import numpy as np
import matplotlib.pyplot as plt
import timeit
from scipy.stats import norm

mu = 0 #среднее значение
sigma2 = 1 #дисперсия
n = 10000 # размер набор чисел


# функция для генерации 10000 рандомных чисел
def uniform_sample(n):
    return np.random.rand(n)

# центральная примерная теорема: среднее из 12 элементов
def normal_sum(mu, sigma2, n):
    samples = np.sum(uniform_sample(12 * n).reshape(n, 12), axis=1)
    return (samples - 6) * sigma2 + mu

# метод отбрасывания, метод отклонения
def normal_rejection(mu, sigma2, n):
    sigma = np.sqrt(sigma2) # вычисляем стандартное отклонение
    samples = [] # список принятых чисел
    while len(samples) < n:
        x = 5 * np.random.uniform(low=-1, high=1) # генерируем число от -5 до 5
        y = np.random.uniform(low=0, high=1) # генерируем случаное число от 0 до 1
        if y <= np.exp(-(x*x)/2): #функция, пропорциональная функции плотности вероятности стандартного нормального распределения
            samples.append(x * sigma + mu) #при выполнении условия число принимается 
    return np.array(samples)

def normal_box_muller(mu, sigma2, n):
    u = uniform_sample(2 * n).reshape(n, 2) # два семпла с распределнием [0;1]
    z = np.sqrt(-2 * np.log(u[:, 0])) * np.cos(2 * np.pi * u[:, 1])
    return mu + sigma2 * z


methods = [
    ('normal_sum', normal_sum),
    ('normal_rejection', normal_rejection),
    ('normal_box_muller', normal_box_muller),
    ('numpy.random.normal', lambda mu, sigma2, n: np.random.normal(mu, np.sqrt(sigma2), n))
]

for name, func in methods:
  execution_time = timeit.timeit(lambda: func(mu, sigma2, n), number=10)
  print(f"{name}: {execution_time:.4f} seconds")

plt.figure(figsize=(15, 10))

for i, (name, func) in enumerate(methods):
    samples = func(mu, sigma2, n)
    mean = np.mean(samples)
    std = np.std(samples)
    print(f"\n{name}:")
    print(f"  Среднее: {mean:.4f}")
    print(f"  Среднеквадратичное отклонение: {std:.4f}")

    plt.subplot(2, 2, i + 1)
    plt.hist(samples, bins=50, density=True, alpha=0.6, label='Гистограмма')
    x = np.linspace(min(samples), max(samples), 100)
    plt.plot(x, norm.pdf(x, mu, np.sqrt(sigma2)), label='Функция плотности вероятности')
    plt.title(f'Распределение {name}')
    plt.xlabel('Значение')
    plt.ylabel('Плотность')
    plt.xlim(-5, 5)
    plt.ylim(0, 0.5)
    plt.legend()

plt.tight_layout()
plt.show()
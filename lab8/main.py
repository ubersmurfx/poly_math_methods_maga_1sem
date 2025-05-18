import numpy as np
import matplotlib.pyplot as plt

def build_grid_map(measurements, prior, grid_resolution, map_length):
    c = np.arange(0, map_length + grid_resolution, grid_resolution)
    log_odds = np.log(prior / (1 - prior)) * np.ones(len(c))

    measurements_less_prob = 0.3
    measurements_high_prob = 0.6
    for z in measurements:
        for i, cell_coord in enumerate(c):
            if cell_coord < z:
                log_odds[i] += np.log(measurements_less_prob / (1 - measurements_less_prob))
            elif cell_coord <= z + 20:
                log_odds[i] += np.log(measurements_high_prob / (1 - measurements_high_prob))
    m = 1 / (1 + np.exp(-log_odds))

    return c, m


if __name__ == '__main__':
    measurements = [101, 82, 91, 112, 99, 151, 96, 85, 99, 105]
    prior = 0.5
    grid_resolution = 10
    map_length = 200

    c, m = build_grid_map(measurements, prior, grid_resolution, map_length)

    # Визуализируем результат
    plt.figure(figsize=(10, 6))
    plt.plot(c, m, marker='o')
    plt.xlabel("расстояние см")
    plt.ylabel("вероятность занятости")
    plt.title("карта")
    plt.grid(True)
    plt.show()

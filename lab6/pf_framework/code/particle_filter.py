import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from read_data import read_world, read_sensor_data
import random

# add random seed for generating comparable pseudo random numbers
np.random.seed(123)

# plot preferences, interactive plotting mode
plt.axis([-1, 12, 0, 10])
plt.ion()
plt.show()


def plot_state(particles, landmarks, map_limits):
    # Visualizes the state of the particle filter.
    #
    # Displays the particle cloud, mean position and landmarks.

    xs = []
    ys = []

    for particle in particles:
        xs.append(particle['x'])
        ys.append(particle['y'])

    # landmark positions
    lx = []
    ly = []

    for i in range(len(landmarks)):
        lx.append(landmarks[i+1][0])
        ly.append(landmarks[i+1][1])

    # mean pose as current estimate
    estimated_pose = mean_pose(particles)

    # plot filter state
    plt.clf()
    plt.plot(xs, ys, 'r.')
    plt.plot(lx, ly, 'bo', markersize=10)
    plt.quiver(estimated_pose[0], estimated_pose[1], np.cos(estimated_pose[2]), np.sin(estimated_pose[2]), angles='xy', scale_units='xy')
    plt.axis(map_limits)

    plt.pause(0.01)


def initialize_particles(num_particles, map_limits):
    # randomly initialize the particles inside the map limits

    particles = []

    for i in range(num_particles):
        particle = dict()

        # draw x,y and theta coordinate from uniform distribution
        # inside map limits
        particle['x'] = np.random.uniform(map_limits[0], map_limits[1])
        particle['y'] = np.random.uniform(map_limits[2], map_limits[3])
        particle['theta'] = np.random.uniform(-np.pi, np.pi)

        particles.append(particle)

    return particles


def mean_pose(particles):
    # calculate the mean pose of a particle set.
    #
    # for x and y, the mean position is the mean of the particle coordinates
    #
    # for theta, we cannot simply average the angles because of the wraparound 
    # (jump from -pi to pi). Therefore, we generate unit vectors from the 
    # angles and calculate the angle of their average 

    # save x and y coordinates of particles
    xs = []
    ys = []

    # save unit vectors corresponding to particle orientations 
    vxs_theta = []
    vys_theta = []

    for particle in particles:
        xs.append(particle['x'])
        ys.append(particle['y'])

        # make unit vector from particle orientation
        vxs_theta.append(np.cos(particle['theta']))
        vys_theta.append(np.sin(particle['theta']))

    # calculate average coordinates
    mean_x = np.mean(xs)
    mean_y = np.mean(ys)
    mean_theta = np.arctan2(np.mean(vys_theta), np.mean(vxs_theta))

    return [mean_x, mean_y, mean_theta]


def sample_motion_model(odometry, particles):
    # Samples new particle positions, based on old positions, the odometry measurements and the motion noise

    delta_rot1 = odometry['r1']
    delta_trans = odometry['t']
    delta_rot2 = odometry['r2']

    # the motion noise parameters: [alpha1, alpha2, alpha3, alpha4]
    noise = [0.1, 0.1, 0.05, 0.05]
    alpha1, alpha2, alpha3, alpha4 = noise #unpack the noise parameters

    # "move" each particle according to the odometry measurements plus sampled noise to generate new particle set
    new_particles = []
    for particle in particles:
        # Add noise to odometry measurements
        delta_rot1_noisy = delta_rot1 + np.random.normal(0, alpha1 * abs(delta_rot1) + alpha2 * delta_trans)
        delta_trans_noisy = delta_trans + np.random.normal(0, alpha3 * delta_trans + alpha4 * (abs(delta_rot1) + abs(delta_rot2)))
        delta_rot2_noisy = delta_rot2 + np.random.normal(0, alpha1 * abs(delta_rot2) + alpha2 * delta_trans)

        # Update particle pose using noisy odometry
        x_new = particle['x'] + delta_trans_noisy * np.cos(particle['theta'] + delta_rot1_noisy)
        y_new = particle['y'] + delta_trans_noisy * np.sin(particle['theta'] + delta_rot1_noisy)
        theta_new = particle['theta'] + delta_rot1_noisy + delta_rot2_noisy
        theta_new = np.arctan2(np.sin(theta_new), np.cos(theta_new)) # Normalize theta to [-pi, pi]

        new_particles.append({'x': x_new, 'y': y_new, 'theta': theta_new})

    return new_particles


def eval_sensor_model(sensor_data, particles, landmarks):
    # Вычисляет правдоподобие наблюдений для всех частиц, учитывая положения частиц и ориентиров, а также измерения датчика.
    # Используется модель датчика, измеряющего только дальность.

    sigma_r = 0.2  # Среднеквадратичное отклонение шума измерений

    # Измеренные идентификаторы ориентиров и дальности
    ids = sensor_data['id']
    ranges = sensor_data['range']

    weights = []  # Список весов для частиц

    for particle in particles:
        particle_x = particle['x']
        particle_y = particle['y'] # Предполагается, что частицы представлены как [x, y, theta] или подобно
        particle_weight = 1.0  # Инициализация веса для частицы

        for i, landmark_id in enumerate(ids):
            # Находим соответствующий ориентир
            landmark = landmarks[landmark_id]
            landmark_x, landmark_y = landmark

            # Вычисляем ожидаемую дальность
            expected_range = np.sqrt((landmark_x - particle_x)**2 + (landmark_y - particle_y)**2)

            # Вычисляем правдоподобие с использованием функции плотности вероятности Гаусса
            likelihood = (1.0 / (sigma_r * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((ranges[i] - expected_range) / sigma_r)**2)

            # Обновляем вес частицы. Предполагается независимость измерений.
            particle_weight *= likelihood

        weights.append(particle_weight)

    # Нормализуем веса
    normalizer = sum(weights)
    weights = np.array(weights) / normalizer

    return weights


def resample_particles(particles, weights):
    # Resamples particles using stochastic universal sampling (SUS).

    N = len(particles)
    new_particles = []
    cumulative_sum = np.cumsum(weights)  #Cumulative sum of weights.

    #This is Stochastic Universal Sampling (SUS):
    r = random.uniform(0, 1/N) #Random start point between 0 and 1/N

    i = 0
    c = r
    for _ in range(N):
        while c > cumulative_sum[i]:
            i += 1
        new_particles.append(particles[i])
        c += 1/N #Increment for the next sample

    return new_particles


def main():
    # implementation of a particle filter for robot pose estimation

    print("Reading landmark positions")
    landmarks = read_world("./data/world.dat")

    print("Reading sensor data")
    sensor_readings = read_sensor_data("./data/sensor_data.dat")

    # initialize the particles
    map_limits = [-1, 12, 0, 10]
    particles = initialize_particles(1000, map_limits)

    # run particle filter
    for timestep in range(len(sensor_readings) // 2):

        # plot the current state
        plot_state(particles, landmarks, map_limits)

        # predict particles by sampling from motion model with odometry info
        new_particles = sample_motion_model(sensor_readings[timestep, 'odometry'], particles)
        #print(new_particles[0])

        # calculate importance weights according to sensor model
        weights = eval_sensor_model(sensor_readings[timestep, 'sensor'], new_particles, landmarks)
        # print(weights)

        # resample new particle set according to their importance weights
        particles = resample_particles(new_particles, weights)

    plt.show(block=True)


if __name__ == "__main__":
    main()
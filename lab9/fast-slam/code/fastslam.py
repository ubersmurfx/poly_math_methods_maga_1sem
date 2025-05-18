from read_data import read_world, read_sensor_data
from misc_tools import *
import numpy as np
import math
import copy

# plot preferences, interactive plotting mode
plt.axis([-1, 12, 0, 10])
plt.ion()
plt.show()


def initialize_particles(num_particles, num_landmarks):
    # initialize particle at pose [0, 0, 0] with an empty map

    particles = []

    for _ in range(num_particles):
        particle = dict()

        # initialize pose: at the beginning, robot is certain it is at [0, 0, 0]
        particle['x'] = 0
        particle['y'] = 0
        particle['theta'] = 0

        # initial weight
        particle['weight'] = 1.0 / num_particles

        # particle history aka all visited poses
        particle['history'] = []

        # initialize landmarks of the particle
        landmarks = dict()

        for i in range(num_landmarks):
            landmark = dict()

            # initialize the landmark mean and covariance
            landmark['mu'] = [0, 0]
            landmark['sigma'] = np.zeros([2, 2])
            landmark['observed'] = False

            landmarks[i + 1] = landmark

        # add landmarks to particle
        particle['landmarks'] = landmarks

        # add particle to set
        particles.append(particle)

    return particles

import numpy as np

def sample_motion_model(odometry, particles):
    # Updates the particle positions, based on old positions, the odometry
    # measurements and the motion noise 

    delta_rot1 = odometry['r1']
    delta_trans = odometry['t']
    delta_rot2 = odometry['r2']

    # the motion noise parameters: [alpha1, alpha2, alpha3, alpha4]
    noise = [0.1, 0.1, 0.05, 0.05]

    alpha1 = noise[0]
    alpha2 = noise[1]
    alpha3 = noise[2]
    alpha4 = noise[3]

    num_particles = len(particles)

    for i in range(num_particles):
        # Add noise to the odometry readings
        delta_rot1_hat = delta_rot1 - np.random.normal(0, alpha1 * abs(delta_rot1) + alpha2 * delta_trans)
        delta_trans_hat = delta_trans - np.random.normal(0, alpha3 * delta_trans + alpha4 * (abs(delta_rot1) + abs(delta_rot2)))
        delta_rot2_hat = delta_rot2 - np.random.normal(0, alpha1 * abs(delta_rot2) + alpha2 * delta_trans)

        # Get current particle state
        x = particles[i]['x']
        y = particles[i]['y']
        theta = particles[i]['theta']

        # Update the particle's position using the noisy odometry
        x_new = x + delta_trans_hat * np.cos(theta + delta_rot1_hat)
        y_new = y + delta_trans_hat * np.sin(theta + delta_rot1_hat)
        theta_new = theta + delta_rot1_hat + delta_rot2_hat
        theta_new = (theta_new + np.pi) % (2 * np.pi) - np.pi  # Normalize angle

        # Update the particle's state in the particles list
        particles[i]['x'] = x_new
        particles[i]['y'] = y_new
        particles[i]['theta'] = theta_new

        # Add the new pose to the particle's history
        particles[i]['history'].append([x_new, y_new, theta_new])

    return particles

def measurement_model(particle, landmark):
    # Compute the expected measurement for a landmark
    # and the Jacobian with respect to the landmark.

    px = particle['x']
    py = particle['y']
    p_theta = particle['theta']

    lx = landmark['mu'][0]
    ly = landmark['mu'][1]

    # calculate expected range measurement
    meas_range_exp = np.sqrt((lx - px) ** 2 + (ly - py) ** 2)
    meas_bearing_exp = math.atan2(ly - py, lx - px) - p_theta

    h = np.array([meas_range_exp, meas_bearing_exp])

    # Compute the Jacobian h_j of the measurement function h
    # wrt the landmark location

    h_j = np.zeros((2, 2))
    h_j[0, 0] = (lx - px) / h[0]
    h_j[0, 1] = (ly - py) / h[0]
    h_j[1, 0] = (py - ly) / (h[0] ** 2)
    h_j[1, 1] = (lx - px) / (h[0] ** 2)

    return h, h_j

def eval_sensor_model(sensor_data, particles):
    # Correct landmark poses with a measurement and
    # calculate particle weight

    # sensor noise
    q_t = np.array([[0.1, 0],
                    [0, 0.1]])

    # measured landmark ids and ranges
    ids = sensor_data['id']
    ranges = sensor_data['range']
    bearings = sensor_data['bearing']

    # update landmarks and calculate weight for each particle
    for particle in particles:

        landmarks = particle['landmarks']
        particle['weight'] = 1.0  # Reset weight for each iteration

        px = particle['x']
        py = particle['y']
        p_theta = particle['theta']

        # loop over observed landmarks
        for i in range(len(ids)):

            # current landmark
            lm_id = ids[i]
            landmark = landmarks[lm_id]

            # measured range and bearing to current landmark
            meas_range = ranges[i]
            meas_bearing = bearings[i]

            # Predicted landmark location based on measurement
            lx_est = px + meas_range * np.cos(p_theta + meas_bearing)
            ly_est = py + meas_range * np.sin(p_theta + meas_bearing)
            z_est = np.array([meas_range, meas_bearing])


            if not landmark['observed']:
                # landmark is observed for the first time

                # initialize landmark mean and covariance.
                landmark['mu'] = [lx_est, ly_est]
                landmark['sigma'] = q_t  # Initialize covariance with sensor noise
                landmark['observed'] = True

            else:
                # landmark was observed before

                # update landmark mean and covariance.
                # Predicted range and bearing
                range_est = np.sqrt((landmark['mu'][0] - px)**2 + (landmark['mu'][1] - py)**2)
                bearing_est = np.arctan2(landmark['mu'][1] - py, landmark['mu'][0] - px) - p_theta
                bearing_est = (bearing_est + np.pi) % (2 * np.pi) - np.pi  # Normalize to [-pi, pi]
                z_hat = np.array([range_est, bearing_est])


                # Calculate Jacobian of measurement model
                H = np.array([
                    [(landmark['mu'][0] - px) / range_est, (landmark['mu'][1] - py) / range_est],
                    [-(landmark['mu'][1] - py) / (range_est**2), (landmark['mu'][0] - px) / (range_est**2)]
                ])

                # Calculate Kalman gain
                S = H @ landmark['sigma'] @ H.T + q_t
                K = landmark['sigma'] @ H.T @ np.linalg.inv(S)

                # Measurement innovation
                z = np.array([meas_range, meas_bearing])
                y = z - z_hat

                # Update landmark mean and covariance
                landmark['mu'] = landmark['mu'] + K @ y
                landmark['sigma'] = (np.eye(2) - K @ H) @ landmark['sigma']

                # Calculate particle weight
                particle['weight'] *= (1 / (2 * np.pi * np.linalg.det(S))**0.5) * np.exp(-0.5 * y.T @ np.linalg.inv(S) @ y)
                if particle['weight'] == 0.0:
                    particle['weight'] = 1e-300
    # normalize weights
    normalizer = sum([p['weight'] for p in particles])

    for particle in particles:
        particle['weight'] = particle['weight'] / normalizer
    return particles

def resample_particles(particles):
    # Returns a new set of particles obtained by performing
    # stochastic universal sampling, according to the particle 
    # weights.

    num_particles = len(particles)
    new_particles = []

    # Extract weights
    weights = [p['weight'] for p in particles]

    # Calculate cumulative sum of weights
    cumulative_weights = np.cumsum(weights)

    # Initialize starting point for sampling
    u = np.random.uniform(0, 1 / num_particles)

    # Perform stochastic universal sampling
    i = 0
    for m in range(num_particles):
        while u > cumulative_weights[i]:
            i += 1
            if i >= num_particles:  # Handle edge case
                i = num_particles - 1
                break
        new_particle = copy.deepcopy(particles[i])
        new_particle['weight'] = 1.0 / num_particles  # Reset weight after resampling
        new_particles.append(new_particle)
        u += 1 / num_particles

    return new_particles


def main():
    print("Reading landmark positions")
    landmarks = read_world("./data/world.dat")

    print("Reading sensor data")
    sensor_readings = read_sensor_data("./data/sensor_data.dat")

    num_particles = 100
    num_landmarks = len(landmarks)

    # create particle set
    particles = initialize_particles(num_particles, num_landmarks)

    # run FastSLAM
    for timestep in range(len(sensor_readings) // 2):

        # predict particles by sampling from motion model with odometry info
        sample_motion_model(sensor_readings[timestep, 'odometry'], particles)

        # evaluate sensor model to update landmarks and calculate particle weights
        eval_sensor_model(sensor_readings[timestep, 'sensor'], particles)

        # plot filter state
        plot_state(particles, landmarks)

        # calculate new set of equally weighted particles
        particles = resample_particles(particles)

    plt.show(block=True)


if __name__ == "__main__":
    main()

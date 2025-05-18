from misc_tools import *

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

''' performs closest point matching of two point sets

    Arguments:
    x -- reference point set
    p -- point set to be matched with the reference

    Output:
    p_matched -- reordered p, so that the elements in p match the elements in x
'''


def closest_point_matching(x, p):
    # Use KDTree for efficient nearest neighbor search
    kdtree = KDTree(x.T)
    distances, indices = kdtree.query(p.T)  # Query KDTree to find indices of nearest neighbors in x for each point in p

    # Reorder p to match the order of the nearest neighbors in x
    p_matched = p[:, indices]

    return p_matched


def icp(x, p, do_matching):
    p0 = p
    for i in range(10):
        # calculate RMSE
        rmse = 0
        for j in range(p.shape[1]):
            rmse += math.pow(p[0, j] - x[0, j], 2) + math.pow(p[1, j] - x[1, j], 2)
        rmse = math.sqrt(rmse / p.shape[1])

        # print and plot
        print("Iteration:", i, " RMSE:", rmse)
        plot_icp(x, p, p0, i, rmse)

        # data association
        if do_matching:
            p = closest_point_matching(x, p)

        # subtract center of mass
        mx = np.transpose([np.mean(x, 1)])
        mp = np.transpose([np.mean(p, 1)])
        x_prime = x - mx
        p_prime = p - mp

        # singular value decomposition
        w = np.dot(x_prime, p_prime.T)
        u, s, v = np.linalg.svd(w)

        # calculate rotation and translation
        r = np.dot(u, v.T)
        t = mx - np.dot(r, mp)

        # apply transformation
        p = np.dot(r, p) + t

    return


def main():
    x, p1, p2, p3, p4 = generate_data()

    #icp(x, p1, False)
    #icp(x, p2, False)
    icp(x, p3, True)
    #icp(x, p4, True)

    plt.waitforbuttonpress()


if __name__ == "__main__":
    main()

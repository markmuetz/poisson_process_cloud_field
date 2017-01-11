import sys
from collections import namedtuple

import numpy as np
import scipy as sp
import pylab as plt

LX = 100
LY = 100


class Cloud(object):
    def __init__(self, x, y, age, max_age):
        self.x = x 
        self.y = y 
        self.age = age 
        self.max_age = max_age


def calc_cloud_stats(clouds, use_min_dist=True):
    dists = []
    for i in range(len(clouds)):
        cloud = clouds[i]
        for j in range(i + 1, len(clouds)):
            test_cloud = clouds[j]
            min_dist = 1e99
            for ii in [-1, 0, 1]:
                for jj in [-1, 0, 1]:
                    x = test_cloud.x + ii * LX
                    y = test_cloud.y + jj * LY
                    dist = np.sqrt((cloud.x - x)**2 + (cloud.y - y)**2)
                    if use_min_dist:
                        min_dist = min(dist, min_dist)
                    else:
                        dists.append(dist)
            if use_min_dist:
                dists.append(min_dist)
    return dists


def show_cloud_field(clouds, dists):
    plt.figure(1)
    plt.clf()
    for cloud in clouds:
        plt.plot(cloud.x, cloud.y, 'bo')

    plt.xlim((0, LX))
    plt.ylim((0, LY))
    plt.pause(0.01)

    plt.figure(2)
    plt.clf()
    n, bins, patch = plt.hist(dists, LY)
    plt.pause(0.01)

    plt.figure(3)
    plt.clf()
    areas = np.pi * (bins[1:]**2 - bins[:-1]**2)
    plt.plot(bins[1:], n / areas)
    plt.pause(0.01)


def create_clouds(mu=3):
    clouds = []
    n_cloud = sp.random.poisson(mu)
    for i in range(n_cloud):
        x = np.random.random() * LX
        y = np.random.random() * LY
        max_age = 3
        clouds.append(Cloud(x, y, 0, max_age))
    return clouds


def main(nt=100, mu=3.):
    clouds = []
    dists = []
    for time in range(nt):
        if time % 1000 == 0:
            print(time)
        for cloud in clouds:
            cloud.age += 1
            if cloud.age > cloud.max_age:
                # print('Killing cloud')
                clouds.remove(cloud)
        new_clouds = create_clouds(mu)
        clouds.extend(new_clouds)
        new_dists = calc_cloud_stats(clouds)
        # show_cloud_field(clouds, new_dists)
        dists.extend(new_dists)
    show_cloud_field(clouds, dists)
    return dists


if __name__ == '__main__':
    dists = main(int(sys.argv[1]), float(sys.argv[2]))
from __future__ import division
import sys
from collections import namedtuple

import numpy as np
import scipy as sp
import pylab as plt

LX = 256000
LY = 256000

MIN_SEP = 25000


class Cloud(object):
    def __init__(self, x, y, age, max_age):
        self.x = x 
        self.y = y 
        self.age = age 
        self.max_age = max_age


def calc_dists(cloud, test_cloud, use_min_dist=False):
    dists = []
    for ii in [-1, 0, 1]:
        for jj in [-1, 0, 1]:
            x = test_cloud.x + ii * LX
            y = test_cloud.y + jj * LY
            dist = np.sqrt((cloud.x - x)**2 + (cloud.y - y)**2)
            dists.append(dist)
    return dists


def calc_cloud_stats(clouds):
    dists = []
    for i in range(len(clouds)):
        cloud = clouds[i]
        for j in range(i + 1, len(clouds)):
            test_cloud = clouds[j]
            new_dists = calc_dists(cloud, test_cloud)
            dists.extend(new_dists)
    return dists


def show_cloud_field(nt, mean_clouds, clouds, dists):
    if False:
        plt.figure(1)
        plt.clf()
        print(len(clouds))
        for cloud in clouds:
            print(cloud)
            plt.plot(cloud.x, cloud.y, 'bo')

        plt.xlim((0, LX))
        plt.ylim((0, LY))
        plt.pause(0.01)

    plt.figure(2)
    plt.clf()
    n, bins, patch = plt.hist(dists, 1000)
    plt.pause(0.01)
    rho_cloud = mean_clouds / (LX * LY)

    print(len(dists))
    plt.figure(3)
    #plt.clf()
    areas = np.pi * (bins[1:]**2 - bins[:-1]**2)
    cloud_densities = n / areas
    imax = np.argmax(bins[1:] > (LX / 2))
    mean_density = n[:imax].sum() / (np.pi * bins[imax]**2)
    xpoints = (bins[:-1] + bins[1:]) / 2
    plt.plot(xpoints, cloud_densities / mean_density)
    plt.xlim((0, LX / 2.))
    plt.pause(0.01)
    return cloud_densities, areas, bins



def create_clouds(clouds, mu=3, mode='normal'):
    if mode not in ['normal', 'enhance', 'inhibit']:
        raise Exception(mode)

    n_cloud = sp.random.poisson(mu)
    if len(clouds) and n_cloud and mode == 'enhance':
        parent_cloud = clouds[np.random.randint(0, len(clouds))]
        x = parent_cloud.x + np.random.random() * MIN_SEP
        y = parent_cloud.y + np.random.random() * MIN_SEP
        max_age = 3
        cloud = Cloud(x, y, 0, max_age)
        n_cloud -= 1
        clouds.append(cloud)

    while n_cloud:
        #print(i)
        x = np.random.random() * LX
        y = np.random.random() * LY
        max_age = 3
        cloud = Cloud(x, y, 0, max_age)
        suppress = False

        for test_cloud in clouds:
            #print(test_cloud)
            dists = calc_dists(cloud, test_cloud)
            min_dist = min(dists)
            if mode == 'inhibit':
                if min_dist < MIN_SEP:
                    if min_dist / MIN_SEP < np.random.random():
                        suppress = True
                        break
        if suppress:
            continue
        clouds.append(cloud)
        n_cloud -= 1
    return clouds


def main(nt=100, mu=3., mode='normal'):
    clouds = []
    dists = []
    total_clouds = 0
    for time in range(nt):
        if time % 1000 == 0:
            print(time)
        for cloud in clouds:
            cloud.age += 1
            if cloud.age > cloud.max_age:
                # print('Killing cloud')
                clouds.remove(cloud)
            #else:
            #    cloud.x = cloud.x + np.random.random() * 1000
            #    cloud.y = cloud.y + np.random.random() * 1000

        clouds = create_clouds(clouds, mu, mode)
        total_clouds += len(clouds)
        new_dists = calc_cloud_stats(clouds)
        # show_cloud_field(clouds, new_dists)
        dists.extend(new_dists)
    mean_clouds = total_clouds/nt
    print(mean_clouds)
    cloud_densities, areas, bins = show_cloud_field(nt, mean_clouds, clouds, dists)
    return dists, cloud_densities, areas, bins 


if __name__ == '__main__':
    plt.ion()
    dists, cloud_densities, areas, bins  = main(int(sys.argv[1]), float(sys.argv[2]), sys.argv[3])

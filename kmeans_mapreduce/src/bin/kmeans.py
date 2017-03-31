"""kmeans.py: Run the k-means algorithm."""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import random
import re
import sys
sys.tracebacklimit = 0

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class KmeansRunner():

    def retrieveData(self, file):
        """Retrieve the data points from the input file.

        :param self: An instance of the class KmeansRunner.
        :param file: A file with the input data.
        :return: An array with the input data points.
        """
        df_points = pd.read_csv(file, header=None, names=["x", "y"], sep=" ")
        if (len(df_points.index) < 1):
            raise Exception("The input file is empty!")
        data = [tuple(row) for row in df_points.values]
        points = np.array([data_point for data_point in data])
        return points

    def initialCentroids(self, file, nclusters):
        """Calculate the initial centroids to be used by the k-means
            clustering algorithm.

        :param self: An instance of the class KmeansRunner.
        :param file: A file with the input data.
        :param nclusters: The number of clusters.
        :return: A list with the initial centroids.
        """
        points = self.retrieveData(file)
        initial_centroids = [list(random.choice(points))]
        dist = []
        if nclusters < 2:
            raise Exception("Error the number of clusters should be" +
                            " greater than or equal to 2!")
        for i in range(2, nclusters + 1):
            dist.append([np.linalg.norm(np.array(point) -
                        initial_centroids[i - 2])**2 for point in points])
            min_dist = dist[0]
            if (len(dist) > 1):
                min_dist = np.minimum(
                    min_dist, (dist[index] for index in range(1, len(dist))))

            sumValues = sum(min_dist)
            probabilities = [float(value) / sumValues for value in min_dist]
            cumulative = np.cumsum(probabilities)

            random_index = random.random()
            index = np.where(cumulative >= random_index)[0][0]
            initial_centroids.append(list(points[index]))

        return initial_centroids

    def retrieveCentroids(self, file):
        """Retrieve the centroids coordinated from the centroids file.

        :param self: An instance of the class KmeansRunner.
        :param file: A file with the centroids.
        :return: A list with the centroids.
        """
        with open(file, "r") as inputFile:
            output_data = inputFile.readlines()

        centroids = []
        for point in output_data:
            p = re.search("\[(.*?)\]", point).group()
            p = p.replace("[", "").replace("]", "")
            p.strip()
            axisx, axisy = p.split(",")
            axisx = float(axisx)
            axisy = float(axisy)
            point_list = [axisx, axisy]
            centroids.append(point_list)
        return centroids

    def retrieveLabels(self, dataFile, centroidsFile):
        """Retrieve the labels of the imput data points.

        :param self: An instance of the class KmeansRunner.
        :param dataFile: A file with the input data points.
        :param centroidsFile: A file with the centroids.
        :return: A list with the labels.
        """
        data_points = self.retrieveData(dataFile)
        centroids = self.retrieveCentroids(centroidsFile)
        labels = []
        for data_point in data_points:
            distances = [np.linalg.norm(data_point - centroid)
                         for centroid in centroids]
            cluster = np.argmin(distances)
            labels.append(int(cluster))
        return labels

    def writeCentroids(self, centroids, file):
        """Write centroids to a file.

        :param self: An instance of the class KmeansRunner.
        :param centroids: A list with the centroids.
        :param file: A file to write the centroids.
        """
        f = open(CENTROIDS_FILE, "w+")
        for item in centroids:
            f.write("%s\n" % str(item))
        f.close()

    def plotClusters(self, data_points, centroids, labels):
        """Plot the clusters with the centroids and save the plot as an image.

        :param self: An instance of the class KmeansRunner.
        :param data_points: An array with the input data points.
        :param centroids: A list with the centroids.
        :param labels: The labels of the input data points.
        """
        plt.scatter(data_points[:, 0], data_points[:, 1], c=labels)
        for i in range(len(centroids)):
            label = "Centroid " + str(i)
            colors = ["red", "green", "blue"]
            plt.scatter(centroids[i][0], centroids[i][1], s=50,
                        c=colors[i], label=label)
        plt.legend(loc="best", fancybox=True)
        fig = plt.gcf()
        plt.show()
        directory = "../images"
        if not os.path.isdir(directory):
            os.makedirs(directory)
        fig.savefig("../images/clusters.png")


CENTROIDS_FILE = "centroids.txt"
OUTPUT_FILE = "output.txt"

if __name__ == "__main__":

    parser = argparse
    parser = argparse.ArgumentParser(description="k-means algorithm"
                                     " implementation on Hadoop",
                                     epilog="Go ahead and try it!")
    parser.add_argument("inputFile", type=str,
                        help="Input data points for the clustering algorithm.")
    parser.add_argument("centroids", type=int,
                        help="Number of clusters.")
    args = parser.parse_args()

    data = args.inputFile
    k = args.centroids
    instanceKmeans = KmeansRunner()
    centroids = instanceKmeans.initialCentroids(data, int(k))
    instanceKmeans.writeCentroids(centroids, CENTROIDS_FILE)

    outputFile = open(OUTPUT_FILE, "w+")
    outputFile.close()

    i = 1
    while True:
        print "k-means iteration #%i" % i

        command = "python kmeansAlgorithm.py < " \
                  + data + " --k=" \
                  + str(k) + " --centroids=" \
                  + CENTROIDS_FILE + " > " + OUTPUT_FILE \
                  + " -r hadoop"
        os.popen(command)

        new_centroids = instanceKmeans.retrieveCentroids(OUTPUT_FILE)

        if sorted(centroids) != sorted(new_centroids):
            centroids = new_centroids
            instanceKmeans.writeCentroids(centroids, CENTROIDS_FILE)
        else:
            break
        i += 1

    os.remove(OUTPUT_FILE)
    labels = instanceKmeans.retrieveLabels(data, CENTROIDS_FILE)
    labelsFile = open("labels.txt", "w+")
    for label in labels:
        labelsFile.write("%s\n" % str(label))
    labelsFile.close()
    data_points = instanceKmeans.retrieveData(data)
    instanceKmeans.plotClusters(data_points, centroids, labels)

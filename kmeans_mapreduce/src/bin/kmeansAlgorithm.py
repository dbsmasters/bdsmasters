# pylint: disable=invalid-name, anomalous-backslash-in-string, abstract-method
"""kmeansAlgorithm.py: Implement the k-means clustering
    algorithm on the input data."""

import re
from mrjob.job import MRJob
from mrjob.job import MRStep
import numpy as np

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class KmeansAlgorithm(MRJob):
    """Implement required methods for kmeans algorithm on Hadoop.
    """
    def configure_options(self):
        """Set the arguments for the class KmeansAlgorithm.

        :param self: A instance of the class KmeansAlgorithm.
        """
        super(KmeansAlgorithm, self).configure_options()
        self.add_passthrough_option(
            "--k", type="int", help="Number of clusters.")
        self.add_file_option("--centroids")

    @staticmethod
    def retrieveCentroids(centroidsFile):
        """Retrieve the centroids coordinated from the centroids file.

        :param centroidsFile: A file with the centroids.
        :return: A list with the centroids.
        """
        with open(centroidsFile, "r") as inputFile:
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

    def assignPointtoCluster(self, _, line):
        """Assign each point to its closest cluster - Mapper Function.

        :param self: An instance of the class KmeansAlgorithm.
        :param line: A line from the input data, with data points in
            the form [axisx axisy]
        :yield: The identifier of a cluster and a point belonging to it.
        """
        axisx, axisy = line.split()
        data_point = np.array([float(axisx), float(axisy)])
        centroids = self.retrieveCentroids(self.options.centroids)
        distances = [np.linalg.norm(data_point - centroid)
                     for centroid in centroids]
        cluster = np.argmin(distances)
        yield int(cluster), data_point.tolist()

    @staticmethod
    def calculatePartialSum(cluster, data_points):
        """Calculate the partial sum of the data points belonging to
            each cluster - Combiner Function.

        :param cluster: An identifier for each cluster.
        :param data_points: A list of points belonging to each cluster.
        :yield: The identifier of a cluster, the partial sum of its
            data points and their number.
        """
        sum_points = np.array(data_points.next())
        counter = 1
        for data_point in data_points:
            sum_points += data_point
            counter += 1
        yield cluster, (sum_points.tolist(), counter)

    @staticmethod
    def calculateNewCentroids(cluster, partial_sums):
        """Calculate the new centroids of the clusters - Reduce Function.

        :param cluster: An identifier for each cluster.
        :param partial_sums: A list with the partial sum of the
            data points of a cluster and their number.
        :yield: The identifier of a cluster and its new centroid.
        """
        total_sum, total_counter = partial_sums.next()
        total_sum = np.array(total_sum)
        for partial_sum, counter in partial_sums:
            total_sum += partial_sum
            total_counter += counter
        yield cluster, (total_sum / total_counter).tolist()

    def steps(self):
        """Set the steps of the MRJob.

        :param self: An instance of the class KmeansAlgorithm.

        :return: a list of steps constructed with MRStep().
        """
        return [MRStep(mapper=self.assignPointtoCluster,
                       combiner=self.calculatePartialSum,
                       reducer=self.calculateNewCentroids)]


if __name__ == "__main__":
    KmeansAlgorithm.run()

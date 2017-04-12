# pylint: disable=invalid-name, anomalous-backslash-in-string, abstract-method

"""createDataPoints.py: Generate data points for clustering."""

import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class DataGenerator(object):
    """Implement method to generate data points.
    """

    @staticmethod
    def generateData(points, dataFile):
        """Generate the input data points.

        :param self: An instance of the class DataGenerator.
        :param points: The number of data points to be generated.
        :param dataFile: The file to save the data points.
        """
        centers = [[25, 25], [-1, -1], [-25, -25]]
        X, labels_true = make_blobs(n_samples=long(points),
                                    centers=centers, cluster_std=3.5,
                                    n_features=2)

        df = pd.DataFrame(X)
        df.to_csv(dataFile, header=False, index=False, sep=" ")

        plt.scatter(X[:, 0], X[:, 1], c=labels_true)
        directory = "../images"
        if not os.path.isdir(directory):
            os.makedirs(directory)
        plt.savefig("../images/data_points.png")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dataFile", type=str,
                        help="File to save the generated data points.")

    parser.add_argument("points", type=int,
                        help="Number of data points to create.")
    args = parser.parse_args()
    instanceDataGenerator = DataGenerator()
    instanceDataGenerator.generateData(args.points, args.dataFile)

"""
plotSilhouetteScore.py: Selecting the number of clusters with
                     silhouette analysis on k-means clustering.

Silhouette analysis can be used to study the separation distance between the
resulting clusters. The silhouette plot displays a measure of how close each
point in one cluster is to points in the neighboring clusters and thus provides
a way to assess parameters like number of clusters visually. This measure has a
range of [-1, 1].

Silhouette coefficients (as these values are referred to as) near +1 indicate
that the sample is far away from the neighboring clusters. A value of 0
indicates that the sample is on or very close to the decision boundary between
two neighboring clusters and negative values indicate that those samples might
have been assigned to the wrong cluster.

Source:
http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html

"""

import argparse
from kmeans import KmeansRunner
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

__author__ = "Scikit-Learn"


class SilhouetteScore():

    def calculateSilhouetteScore(self, dataFile):
        """Calculate the silhouette score for different numbers of clusters.

        :param self: An instance of the class SilhouetteScore.
        :param dataFile: An array with the input data points.
        :return: A list with the names of the image files created.
        """
        instanceKmeans = KmeansRunner()
        X = instanceKmeans.retrieveData(dataFile)
        if (X.shape[0] > 10000):
            size = round(X.shape[0] * 0.001)
            idx = np.random.randint(X.shape[0], size=size)
            subset = X[idx, :]
            X = subset
        range_n_clusters = [2, 3, 4, 5, 6]
        list_images = []

        for n_clusters in range_n_clusters:

            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches(18, 7)

            ax1.set_xlim([-0.1, 1])

            ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

            clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            cluster_labels = clusterer.fit_predict(np.array(X))

            silhouette_avg = silhouette_score(X, cluster_labels)
            print("For n_clusters =", n_clusters,
                  "The average silhouette_score is :", silhouette_avg)

            sample_silhouette_values = silhouette_samples(X, cluster_labels)

            y_lower = 10
            for i in range(n_clusters):

                ith_cluster_silhouette_values = \
                    sample_silhouette_values[cluster_labels == i]

                ith_cluster_silhouette_values.sort()

                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.spectral(float(i) / n_clusters)
                ax1.fill_betweenx(np.arange(y_lower, y_upper),
                                  0, ith_cluster_silhouette_values,
                                  facecolor=color, edgecolor=color, alpha=0.7)

                ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                y_lower = y_upper + 10

            ax1.set_title("The silhouette plot for the various clusters.")
            ax1.set_xlabel("The silhouette coefficient values")
            ax1.set_ylabel("Cluster label")

            ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax1.set_yticks([])
            ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
            ax2.scatter(X[:, 0], X[:, 1], marker=".", s=30, lw=0, alpha=0.7,
                        c=colors)

            centers = clusterer.cluster_centers_
            ax2.scatter(centers[:, 0], centers[:, 1],
                        marker="o", c="white", alpha=1, s=200)

            for i, c in enumerate(centers):
                ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50)

            ax2.set_title("The visualization of the clustered data.")
            ax2.set_xlabel("Feature space for the 1st feature")
            ax2.set_ylabel("Feature space for the 2nd feature")

            plt.suptitle(("Silhouette analysis for k-means"
                          "clustering on sample data "
                          "with n_clusters = %d" % n_clusters),
                         fontsize=14, fontweight="bold")
            fig.savefig("cluster_" + str(n_clusters) + ".png")
            list_images.append("cluster_" + str(n_clusters) + ".png")
        return list_images

    def silhouetteScoretoPNG(self, list_images):
        """Save the results of the plots in asingle image file.

        :param self: An instance of the class SilhouetteScore.
        :param list_images: A list with the name of the image files created.
        """
        clusterImages = [PIL.Image.open(i) for i in list_images]
        minSize = sorted([(np.sum(i.size), i.size)
                          for i in clusterImages])[0][1]

        imagesCombination = np.vstack((np.asarray(i.resize(minSize))
                                       for i in clusterImages))
        imagesCombination = PIL.Image.fromarray(imagesCombination)
        directory = "../images"
        if not os.path.isdir(directory):
            os.makedirs(directory)
        imagesCombination.save("../images/clustersScore.png")
        for image in list_images:
            os.remove(image)
        print ("The silhouette score for the number of"
               " clusters ranging from 2 "
               "to 6 has been saved in the file clustersScore.png!")


if __name__ == "__main__":

    parser = argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("dataFile", type=str,
                        help="File to retrieve the generated data points.")
    args = parser.parse_args()
    instanceSilhouetteScore = SilhouetteScore()
    images = instanceSilhouetteScore.calculateSilhouetteScore(args.dataFile)
    instanceSilhouetteScore.silhouetteScoretoPNG(images)

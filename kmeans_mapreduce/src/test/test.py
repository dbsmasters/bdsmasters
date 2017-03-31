import unittest
from createDataPoints import DataGenerator
from kmeans import KmeansRunner

__author__ = "Stratos Gounidellis, Lamprini Koutsokera"
__copyright__ = "Copyright 2017, BDSMasters"


class TestStringMethods(unittest.TestCase):

    def test_dataPoints(self):
        instanceData = DataGenerator()
        fname = "test.txt"
        instanceData.generateData(100, fname)
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        i + 1
        self.assertEqual(100, i+1)

    def test_exceptionClustersNumber(self):
        fname = "test.txt"
        instanceKmeans = KmeansRunner()
        with self.assertRaises(Exception) as context:
            instanceKmeans.initialCentroids(fname, 1)
        self.assertIn("Error the number of clusters should be greater" +
                      "than or equal to 2!", "".join(context.exception))

    def test_fileLength(self):
        fname = "test.txt"
        instanceKmeans = KmeansRunner()
        testFile = open(fname, "w+")
        testFile.close()
        with self.assertRaises(Exception) as context:
            instanceKmeans.retrieveData(fname)
        self.assertIn("The input file is empty!", "".join(context.exception))


if __name__ == "__main__":
    unittest.main()

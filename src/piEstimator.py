import sys
import random
import os

from pyspark.sql import SparkSession


# Spark can also be used for compute-intensive tasks.
# This code estimates π by "throwing darts" at a circle.
# We pick random points in the unit square ((0, 0) to (1,1)) and see how many fall
# in the unit circle. The fraction should be π / 4, so we use this to get our estimate.
def inside(_):
    x, y = random.random(), random.random()
    return x * x + y * y < 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\033[91mERROR: Samples is required \033[0m')
        sys.exit(1)

    samples = int(sys.argv[1])
    samplesStr = '{:,}'.format(samples).replace(',', '.')

    # Create SparkSession (the entry point to any Spark program)
    spark = SparkSession.builder.appName(f"piEstimator({samplesStr})").getOrCreate()
    # Get the SparkContext from SparkSession
    sc = spark.sparkContext

    piRDD = sc.parallelize(range(1, samples)).filter(inside)
    count = piRDD.count()
    spark.stop()

    # count / samples should approximate π / 4
    pi = 4.0 * count / samples
    print(f"\033[92mOK: Pi is roughly {pi} \033[0m")

    # Save estimation
    currentDir = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(f"{currentDir}/results", exist_ok=True)
    outputFile = f"{currentDir}/results/pi_{samplesStr}.txt"
    estimationFile = open(outputFile, "w")
    estimationFile.write(str(pi))
    estimationFile.close()
    print(f"\033[92mOK: Pi estimation saved in {outputFile} \033[0m")

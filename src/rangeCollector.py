import sys
import os

from pyspark.sql import SparkSession


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\033[91mERROR: Limit is required \033[0m')
        sys.exit(1)

    limit = int(sys.argv[1])
    limitStr = '{:,}'.format(limit).replace(',', '.')

    # Create SparkSession (the entry point to any Spark program)
    spark = SparkSession.builder.appName(f"rangeCollector({limitStr})").getOrCreate()
    # Get the SparkContext from SparkSession
    sc = spark.sparkContext

    # Collect range
    rangeRDD = sc.parallelize(range(1, limit))
    collectedRange = rangeRDD.collect()
    spark.stop()
    print("\033[92mOK: Range collected \033[0m")

    # Save range
    currentDir = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(f"{currentDir}/results", exist_ok=True)
    outputFile = f"{currentDir}/results/range_{limitStr}.txt"
    rangeFile = open(outputFile, "w")
    rangeFile.write(str(collectedRange))
    rangeFile.close()
    print(f"\033[92mOK: Range saved in {outputFile} \033[0m")



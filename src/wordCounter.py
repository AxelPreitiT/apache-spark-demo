import sys
import os

from pyspark.sql import SparkSession


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('\033[91mERROR: Text file is required \033[0m')
        sys.exit(1)

    textFileSrc = sys.argv[1]
    textFileName = ".".join(textFileSrc.split("/")[-1].split(".")[:-1])
    textFile = open(textFileSrc, "r")

    # Create SparkSession (the entry point to any Spark program)
    spark = SparkSession.builder.appName(f"wordCounter({textFileName})").getOrCreate()
    # Get the SparkContext from SparkSession
    sc = spark.sparkContext

    # Load text file
    text = sc.textFile(textFileSrc)
    # Given the text file, the RDD will:
    # 1. Split the text into words separated by spaces
    # 2. Map each word to a tuple (word, 1)
    # 3. Reduce the tuples by key (word) summing the values (1)
    # 4. Sort the tuples by the times the word appears in the text in descending order
    # So it calculates the number of times each word appears in the text doing a map-reduce operation
    timesPerWordRDD = text.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda curr, new: curr + new).sortBy(lambda tuple: tuple[1], ascending=False)
    timesPerWord = timesPerWordRDD.collect()
    spark.stop()

    print("\033[92mOK: Word counter calculated \033[0m")
    for (word, times) in timesPerWord[:5]:
        print(f"\033[92m('{word}', {times})\033[0m")
    print("...")
    for (word, times) in timesPerWord[-5:]:
        print(f"\033[92m('{word}', {times})\033[0m")

    # Save word counter
    currentDir = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(f"{currentDir}/results", exist_ok=True)
    outputFile = f"{currentDir}/results/wordCounter_{textFileName}.txt"
    wordCounterFile = open(outputFile, "w")
    wordCounterFile.write(str(timesPerWord))
    wordCounterFile.close()

    print(f"\033[92mOK: Word counter saved in {outputFile} \033[0m")




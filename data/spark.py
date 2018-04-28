from pyspark import SparkContext
from itertools import permutations

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split("\t")))   # tell each worker to split each line of it's partition

# Create a key-value pair of username and a list of items they've looked at, removing duplicates
# for example, (bhm5zr, 1), (bhm5zr, 4), (bhm5zr, 1), (sz4dd, 2) will turn into (bhm5zr, [1, 4]), (sz4dd, [2])
user_items = pairs.distinct().groupByKey()

# for each user, we create pairs of pages they viewed without their username attached
# for example, (tmh6de, [1,2,3]) will turn into (1,2), (2,1), (1,3), (3,1), (2,3), (3,2)
page_pairs = user_items.flatMap(lambda x: permutations(x[1], 2))
# Add a 1 to each pair of pages, so that we can count the instances in the future
# for example (1,2), (2,1), (1,2) will turn into ((1,2), 1), ((2,1), 1), ((1,2), 1)
pages = page_pairs.map(lambda pair: (pair, 1))

# Count up all pairs of pages
# for example, ((1,2), 1), ((2,1), 1), ((1,2), 1) will turn into ((1,2), 2), ((2,1), 1)
count = pages.reduceByKey(lambda x, y: int(x)+int(y))

# Only keep the pairs that have a count greater than or equal to 3
final_recommendation_pairs = count.filter(lambda x: x[1] >= 3)

output = final_recommendation_pairs.collect()  # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id1 %s page_id2 %d" % (page_id, count))
print ("Popular items done")

sc.stop()

from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/view_log.txt", 2)     # each worker loads a piece of the data file



pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
output = pairs.collect()
for thing in output:
    print("user_id %s page_id %s" % (thing[0], thing[1]))
print("line done")
print("\n\n\n")


pairs_tuples = pairs.map(lambda pair: (pair[0], pair[1]))
output = pairs_tuples.collect()
print(output)
print("pairs_tuples done")
print("\n\n\n")


item_lists = pairs_tuples.groupByKey().mapValues(list)
output = item_lists.collect()
print(output)
print("items_list done")
print("\n\n\n")


distinct_items = item_lists.map(lambda pair: (pair[0], sorted(list(set(pair[1])))))
output = distinct_items.collect()
print(output)
print("distinct_items done")
print("\n\n\n")


def get_pairs(pair):
    user = pair[0]
    item_list = pair[1]
    all_pairs = []
    for i in range(len(item_list)):
        for j in range(i+1, len(item_list), 1):
            all_pairs.append((user, (item_list[i], item_list[j])))
    return all_pairs

item_pairs = distinct_items.flatMap(get_pairs)
output = item_pairs.collect()
print(output)
print("item pairs finished")
print("\n\n\n")


swapped_pairs = item_pairs.map(lambda pair: (pair[1], pair[0]))
output = swapped_pairs.collect()
print(output)
print("swapped pairs finished")
print("\n\n\n")


user_list = swapped_pairs.groupByKey().mapValues(list)
output = user_list.collect()
print(output)
print("user list finished")
print("\n\n\n")


pair_count = user_list.map(lambda pair: (pair[0], len(pair[1])))
output = pair_count.collect()
print(output)
print("pair count finished")
print("\n\n\n")


related_pairs = pair_count.filter(lambda pair: pair[1] >= 3)
output = related_pairs.collect()
print(output)
print("related pairs finished")
print("\n\n\n")


sc.stop()

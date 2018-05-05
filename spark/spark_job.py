from pyspark import SparkContext
import MySQLdb

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/view_log.txt", 2)     # each worker loads a piece of the data file


# Each line is split into a list of [user_id, page_id]
pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
output = pairs.collect()
for thing in output:
    print("user_id %s page_id %s" % (thing[0], thing[1]))
print("line done")
print("\n\n\n")

# Each list is turned into a tuple of (user_id, page_id)
pairs_tuples = pairs.map(lambda pair: (str(pair[0]), str(pair[1])))
output = pairs_tuples.collect()
print(output)
print("pairs_tuples done")
print("\n\n\n")

# Each tuple is turned into a tuple of (user_id, [page_id_1, page_id_2])
item_lists = pairs_tuples.groupByKey().mapValues(list)
output = item_lists.collect()
print(output)
print("items_list done")
print("\n\n\n")

# Each list of pages a user visited is made distinct (no duplicates) and sorted
distinct_items = item_lists.map(lambda pair: (pair[0], sorted(list(set(pair[1])))))
output = distinct_items.collect()
print(output)
print("distinct_items done")
print("\n\n\n")

# Each user with page list is turned into multiple tuples of (user_id, (page1, page2))
# Since the list was sorted, the first page in the tuple will always have a smaller id
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

# Each tuple is swapped so it's now ((page_1, page_2), user_id)
swapped_pairs = item_pairs.map(lambda pair: (pair[1], pair[0]))
output = swapped_pairs.collect()
print(output)
print("swapped pairs finished")
print("\n\n\n")

# Each tuple is grouped to be ((page_1, page_2), [user_id_1, user_id_2])
user_list = swapped_pairs.groupByKey().mapValues(list)
output = user_list.collect()
print(output)
print("user list finished")
print("\n\n\n")

# The count of each tuple replaces the list of users: ((page_1, page_2), #of_users_to_access_both)
pair_count = user_list.map(lambda pair: (pair[0], len(pair[1])))
output = pair_count.collect()
print(output)
print("pair count finished")
print("\n\n\n")

# Any pair of pages with less than 3 common users is filtered out
related_pairs = pair_count.filter(lambda pair: pair[1] >= 3)
output = related_pairs.collect()
print(output)
print("related pairs finished")
print("\n\n\n")

# Each pair of pages is copied in forward and reverse order (now ignoring the count):
# ((page_1, page_2), count) -> [(page_1, page_2), (page_2, page_1)]
duplicated_pairs = related_pairs.flatMap(lambda pair: [(pair[0][0], pair[0][1]), (pair[0][1], pair[0][0])])
output = duplicated_pairs.collect()
print(output)
print("duplicated pairs finished")
print("\n\n\n")

# Each pair is grouped by key to get a list of related pages for each page: (page_1, [page_2, page_3])
related_lists = duplicated_pairs.groupByKey().mapValues(list)
output = related_lists.collect()
print(output)
print("related lists finished")
print("\n\n\n")

# Each list of related pages is turned into a comma-separated string: (page_1, "page_2,page_3")
string_lists = related_lists.map(lambda pair: (int(pair[0]), ",".join(pair[1])))
all_string_lists = list(string_lists.collect())
print(all_string_lists)
print("string lists finished")
print("\n\n\n")


conn = MySQLdb.connect(host="mysql", user="www", passwd="$3cureUS", db="cs4501")
c = conn.cursor()

c.execute("SHOW TABLES;")
tables_list = map(lambda tuple: tuple[0], c.fetchall())
if "app_recommendations" not in tables_list:
    c.execute("""CREATE TABLE app_recommendations (Page_id INT, Related_pages VARCHAR(100));""")
else:
    c.execute("""DELETE FROM app_recommendations;""")

c.executemany("""INSERT INTO app_recommendations VALUES (%s, %s);""", all_string_lists)
c.execute("""SELECT * FROM app_recommendations;""")
print(c.fetchall())

c.close()
conn.close()
sc.stop()

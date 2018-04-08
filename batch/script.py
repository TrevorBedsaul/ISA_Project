from kafka import KafkaConsumer
import json
import time
from elasticsearch import Elasticsearch

consumer = None
es = None
while consumer is None:
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        es = Elasticsearch(['es'])
    except:
        time.sleep(1)

loaded_es = False
book_from_fixture_1 = {"seller": {"name": "Steven", "id": 1}, "id": 1, "type_name": "HC", "edition": 1, "author": "Cristopher Robin", "condition": "NW", "year": "1902", "buyer": None, "price": 100.0, "status": "AV", "ISBN": "098-765-4321", "class_id": "ENGL 1020", "title": "Winnie the Pooh"}
book_from_fixture_2 = {"buyer": None, "class_id": "ENGL 1020", "condition": "NW", "edition": 1, "type_name": "HC", "price": 100.0, "seller": {"name": "Steven", "id": 1}, "title": "book 2", "ISBN": "098-765-4321", "status": "AV", "year": "1902", "author": "Cristopher Robin", "id": 2}
time.sleep(10)
while not loaded_es:
    try:
        es.index(index='listing_index', doc_type='listing', id=book_from_fixture_1['id'], body=book_from_fixture_1)
        es.index(index='listing_index', doc_type='listing', id=book_from_fixture_2['id'], body=book_from_fixture_2)
        es.indices.refresh(index="listing_index")
        loaded_es = True
    except:
        time.sleep(1)

while True:
    for message in consumer:
        message_dict = json.loads((message.value).decode('utf-8'))
        es.index(index='listing_index', doc_type='listing', id=message_dict['id'], body=message_dict)
    es.indices.refresh(index="listing_index")

from kafka import KafkaConsumer
import json
import time
from elasticsearch import Elasticsearch

consumer = None
while consumer is None:
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(1)
es = Elasticsearch(['es'])

while True:
    for message in consumer:
        message_dict = json.loads((message.value).decode('utf-8'))
        es.index(index='listing_index', doc_type='listing', id=message_dict['id'], body=message_dict)
    es.indices.refresh(index="listing_index")

from kafka import KafkaConsumer, KafkaProducer
import time
import json

consumer = None
while consumer is None:
    try:
        consumer = KafkaConsumer('pageview-topic', group_id='pageview-tracker', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(1)

#file = open("view_log.txt","a")

while True:
    for message in consumer:
        # Printing stuff doesn't seem to be doing anything, so i'm instead
        # making a new entry in elasticsearch to confirm that something is happening/kafka is working
        book_from_fixture_1 = {"seller": 1, "id": 40, "type_name": "HC", "edition": 1, "author": "Cristopher Robin",
                               "condition": "NW", "year": "1902", "buyer": None, "price": 100.0, "status": "AV",
                               "ISBN": "098-765-4321", "class_id": "ENGL 1020", "title": "book from pageview script"}
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('new-listings-topic', json.dumps(book_from_fixture_1).encode('utf-8'))


        message_dict = json.loads((message.value).decode('utf-8'))
        viewer = message_dict["user_id"]
        item = message_dict["book_id"]
        write_string = str(viewer) + "\t" + str(item)
        print(write_string)
        #file.write(write_string)
    print("here")


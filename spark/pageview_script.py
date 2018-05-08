from kafka import KafkaConsumer, KafkaProducer
import time
import json

consumer = None
while consumer is None:
    try:
        consumer = KafkaConsumer('pageview-topic', group_id='pageview-tracker', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(1)

while True:
    for message in consumer:
        message_dict = json.loads((message.value).decode('utf-8'))
        viewer = message_dict["user_id"]
        item = message_dict["book_id"]
        write_string = str(viewer) + "\t" + str(item) + "\n"
        with open("view_log.txt", "a") as file:
            file.write(write_string)

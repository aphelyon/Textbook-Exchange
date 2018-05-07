from kafka import KafkaConsumer
from time import sleep
from json import loads

if __name__ == "__main__":
    sleep(60)
    print("Batch container starting")
    consumer = KafkaConsumer('new-recommendation-topic', group_id='recommendation-indexer', bootstrap_servers=['kafka:9092'])
    f = open('access.log', 'w+')
    while True:
        for message in consumer:
            message_dict = loads((message.value).decode('utf-8'))
            #some kind of write needed, I don't think this works.
            f.write(meesage_dict)

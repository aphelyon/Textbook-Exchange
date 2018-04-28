from kafka import KafkaConsumer
from json import loads
from time import sleep

if __name__ == "__main__":
    sleep(20)
    print("spark_batch container starting")
    consumer = KafkaConsumer('new-recommendations-topic', group_id='recommendation-indexer', bootstrap_servers=['kafka:9092'])
    
    while True:
        for message in consumer:
            print(loads((message.value).decode('utf-8')))

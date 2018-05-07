from kafka import KafkaConsumer
from json import loads
from time import sleep

if __name__ == "__main__":
    sleep(20)
    print("spark_batch container starting")
    consumer = KafkaConsumer('new-recommendations-topic', group_id='recommendation-indexer', bootstrap_servers=['kafka:9092'])
    
    while True:
        for message in consumer:
            with open('/tmp/data/access.log', 'a') as f:
                message_dict = loads((message.value).decode('utf-8'))
                f.write(message_dict['user_id'] + '\t' + message_dict['item_id'] + '\n')
                print(message_dict)

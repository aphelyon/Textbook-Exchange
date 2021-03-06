from elasticsearch import Elasticsearch
from elasticsearch import exceptions
from kafka import KafkaConsumer
from time import sleep
from json import loads

if __name__ == "__main__":
    sleep(60)
    print("Batch container starting")
    es = Elasticsearch(['es'])
    # If user searches before any listings are created, add the index just in case
    try:
        es.indices.create(index='listing_index')
    except exceptions.RequestError:
        pass
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    while True:
        for message in consumer:
            message_dict = loads((message.value).decode('utf-8'))
            es.index(index='listing_index', doc_type='listing', id=int(message_dict['id']), body=message.value)
            print("Added",message_dict,"to search index")
            es.indices.refresh(index="listing_index")

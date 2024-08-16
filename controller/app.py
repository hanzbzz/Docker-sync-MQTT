import pika

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabitmq-broker'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()

import time

while True:
    main()
    time.sleep(30)

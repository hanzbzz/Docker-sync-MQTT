import pika
from functools import partial
from utils import print_now

workers = ["worker1"]

def response_callback(channel, method_frame, header_frame, body, responses, connection):
    body = body.decode()
    print_now(f"[*] RESPONSE: RECEIVE {body}")
    responses.append(body)
    # all workers finished
    if responses == workers:
        print_now("[+] JOB finished")
        # stop consuming
        connection.close()

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabitmq-broker'))
    channel = connection.channel()
    # declare queues
    channel.queue_declare(queue='command')
    channel.queue_declare(queue='response')

    # start job1
    channel.basic_publish(exchange='', routing_key='command', body='job1')
    print_now("[+] COMMAND: SEND job1")

    responses = []
    channel.basic_consume(queue='response', on_message_callback=partial(response_callback, responses=responses, connection=connection) , auto_ack=True)
    channel.start_consuming()

import time

while True:
    main()
    time.sleep(30)

import pika
from functools import partial
from utils import print_now

workers = {"worker1", "worker2", "worker3", "worker4"}

def response_callback(channel, method_frame, header_frame, body, responses):
    body = body.decode()
    print_now(f"[*] RESPONSE: RECEIVE {body}")
    responses.add(body)
    # all workers finished
    if responses == workers:
        print_now("[+] JOB finished")
        # stop consuming
        channel.basic_cancel("tag")

def start_job(channel, name):
    for worker in workers:
        channel.basic_publish(exchange='', routing_key=worker, body=name)
        print_now(f"[+] COMMAND: SEND {name}")
    responses = set()
    channel.basic_consume(queue='response', on_message_callback=partial(response_callback, responses=responses) , auto_ack=True, consumer_tag="tag")
    channel.start_consuming()

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabitmq-broker'))
    channel = connection.channel()
    # declare queues
    for worker in workers:
        channel.queue_declare(queue=worker)

    # start job1
    start_job(channel, "job1")
    
    # start job2
    start_job(channel, "job2")

import time

while True:
    main()
    time.sleep(30)

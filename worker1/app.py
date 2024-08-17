import pika
import random
import time
from utils import print_now

def job1():
    for i in range(5):
        time.sleep(random.randint(0,2))

def job2():
    for i in range(10):
        time.sleep(random.randint(0,1))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabitmq-broker'))
    channel = connection.channel()

    channel.queue_declare(queue='command')
    channel.queue_declare(queue='response')

    def callback(ch, method, properties, body):
        body = body.decode()
        print_now(f"[+] COMMAND: RECEIVE {body}")
        if body == "job1":
            job1()
            channel.basic_publish(exchange='', routing_key='response', body='worker1')
            print_now("[*] RESPONSE: SEND job1")
        elif body == "job2":
            job2()
            channel.basic_publish(exchange='', routing_key='response', body='worker1')
            print_now("[*] RESPONSE: SEND job2")

    channel.basic_consume(queue='command', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

main()
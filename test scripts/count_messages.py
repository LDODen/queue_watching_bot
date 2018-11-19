import pika
connection = pika.BlockingConnection()

channel = connection.channel()
q = channel.queue_declare("test")
q_len = q.method.message_count
print(q_len)
import telebot
from telebot.apihelper import ApiException
import time
import pika
import os
import requests
import logging
import json
from bt import BOT_TOKEN, CHANNEL_NAME

bot = telebot.TeleBot(BOT_TOKEN)


def read_settigs():
    with open("set.json", "r") as sett:
            return json.loads(sett.read())

def send_queues_stat(itms, conn_params):
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    for item in itms:
        print(item['name'])
        
        if item['durable'] == 'True':
            q = channel.queue_declare(item['name'], durable=True)
        else:
            q = channel.queue_declare(item['name'])
        
        q_len = q.method.message_count
        
        print(q_len)
        limit = int(item['limit'])
        if q_len >= limit:
            try:
                bot.send_message(CHANNEL_NAME, "length of queue '{}' is:{}".format(item, q_len))
            except ApiException:
                continue
        # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
        time.sleep(1)
 
    return


@bot.message_handler(content_types=["text"])
def handle(msg):
    print(msg.chat.id)
    print(msg)
    bot.send_message(msg.chat.id, "You said '{}'".format(msg.text))
    

if __name__ == '__main__':
    print ('Listening ...')
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
   

    while True:
        incoming = bot.get_updates(timeout=0)
        # Пауза в 15 секунд перед повторной проверкой
        for mes in incoming:
            try:
                print(mes.channel_post.text)
            except AttributeError:
                continue
        #qsett = read_settigs()
        #credentials = pika.PlainCredentials(qsett['user'], qsett['password'])
        #parameters = pika.ConnectionParameters(qsett['host'], int(qsett['port']), '/', credentials)
        #send_queues_stat(qsett["queues"], parameters)
        #logging.info('[App] Script went to sleep.')
        time.sleep(15)


    logging.info('[App] Script exited.\n')

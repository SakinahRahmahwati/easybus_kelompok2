# utils/logger.py

import pika
import json

def kirim_log(aksi, keterangan, user_id=None, status="sukses"):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='log_queue', durable=True)
        log = {
            "user_id": user_id,
            "aksi": aksi,
            "status": status,
            "keterangan": keterangan
        }
        channel.basic_publish(
            exchange='',
            routing_key='log_queue',
            body=json.dumps(log),
            properties=pika.BasicProperties(
                delivery_mode=2  # supaya durable
            )
        )
        connection.close()
    except Exception as e:
        print("Gagal mengirim log:", e)
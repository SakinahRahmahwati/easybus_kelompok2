import pika
import json
import os
from datetime import datetime

# Buat folder logs jika belum ada
os.makedirs("logs", exist_ok=True)

def write_log_to_file(log):
    with open("logs/activity.log", "a") as f:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = log.get("user_id", "-")
        aksi = log.get("aksi", "-")
        status = log.get("status", "-")
        keterangan = log.get("keterangan", "-")
        f.write(f"[{waktu}] [user_id={user_id}] [{aksi}] Status: {status} - {keterangan}\n")

def callback(ch, method, properties, body):
    print(" [v] Pesan diterima dari queue.") 
    log_data = json.loads(body)
    print(" [v] Konten log:", log_data)  
    write_log_to_file(log_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Ganti localhost → variabel environment, default tetap localhost jika dijalankan lokal
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='log_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='log_queue', on_message_callback=callback)

print(" [*] Logging worker aktif. Menunggu pesan...")
channel.start_consuming()

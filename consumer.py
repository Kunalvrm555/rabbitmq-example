import pika
import json
import subprocess
# RabbitMQ configuration
exchange = 'file_upload'
queue = 'file_upload_queue'
routing_key = 'file_uploaded'

def process_message(channel, method, properties, body):
    # Parse the message
    message = body.decode('utf-8')
    file_metadata = json.loads(message)

    # Extract necessary information from the file metadata
    file_id = file_metadata['fileId']
    original_name = file_metadata['originalName']

    # Construct the command to run the Python script
    python_script = 'rename.py'  # Replace with the actual Python script filename
    command = f'py {python_script} {file_id}'
    print(f'Running command: {command}')

    # Run the Python script as a subprocess
    subprocess.run(command, shell=True)

    # Acknowledge the message to remove it from the queue
    channel.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',  # RabbitMQ server host
        port=5673,         # RabbitMQ server port (default: 5672)
        virtual_host='/',  # Virtual host (default: '/')
        credentials=pika.credentials.PlainCredentials(
            username='guest',  # Username (default: guest)
            password='guest'   # Password (default: guest)
        )
    )
)
    channel = connection.channel()

    # Declare the exchange, queue, and binding
    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    # Set the prefetch count to limit the number of unacknowledged messages
    channel.basic_qos(prefetch_count=1)

    # Start consuming messages
    channel.basic_consume(queue=queue, on_message_callback=process_message)

    print('Consumer started. Waiting for messages...')
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer()

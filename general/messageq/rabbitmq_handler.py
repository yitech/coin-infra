import pika
from pika.credentials import PlainCredentials

class RabbitMQHandler:
    def __init__(self, url, port, username, password):
        self._connection_params = pika.ConnectionParameters(
            host=url,
            port=port,
            credentials=PlainCredentials(username, password)
        )
        self._connection = None
        self._channel = None

    def connect(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self._connection_params)
            self._channel = self._connection.channel()

    def declare_queue(self, queue_name):
        self.connect()
        self._channel.queue_declare(queue=queue_name)

    def publish(self, queue_name, message):
        self.connect()
        self._channel.basic_publish(exchange='',
                                    routing_key=queue_name,
                                    body=message)

    def consume(self, queue_name, callback):
        self.connect()
        self._channel.basic_consume(queue=queue_name,
                                    on_message_callback=callback,
                                    auto_ack=True)
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.stop_consuming()
        except Exception as e:
            print(f"An error occurred: {e}")

    def close(self):
        if self._connection:
            self._connection.close()
            
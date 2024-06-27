import pika

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host='localhost',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='guest',  # Имя пользователя по умолчанию
        password='guest'   # Пароль по умолчанию
    )
)

# Установка соединения
connection = pika.BlockingConnection(connection_params)

# Создание канала
channel = connection.channel()


# Имя очереди
queue_name = 'hello'
message = 'Hello, RabbitMQ!'


# # Отправка сообщения
# channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)


# # Функция, которая будет вызвана при получении сообщения
# def callback(ch, method, properties, body):
#     print(f"Received: {body}")
#     print(type(body))
#     # connection.close()


# # Подписка на очередь и установка обработчика сообщений
# channel.basic_consume(
#     queue=queue_name,
#     on_message_callback=callback,
#     auto_ack=True  # Автоматическое подтверждение обработки сообщений
# )

# print('Waiting for messages. To exit, press Ctrl+C')
# channel.start_consuming()


# Пример настройки обменов
channel.exchange_declare(exchange='order_events', exchange_type='topic')


# Пример подписки на сообщения
def process_order_created(ch, method, properties, body):
    order_data = body.decode('utf-8')
    # Здесь происходит обработка события
    print("Событие 'order.created':", order_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.queue_declare(queue='order_created_queue', durable=True)
channel.queue_bind(exchange='order_events', queue='order_created_queue', routing_key='order.created')
channel.basic_consume(queue='order_created_queue', on_message_callback=process_order_created)

print('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()

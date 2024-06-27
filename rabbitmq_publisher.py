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
# channel.queue_delete(queue=queue_name)
# channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)

# Пример отправки сообщения
channel.basic_publish(
    exchange='order_events',
    routing_key='order.created',
    body='Данные о заказе #12345',
)

channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body=message
)

print(f"Sent: '{message}'")

# Закрытие соединения
connection.close()

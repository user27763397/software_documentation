import json
from abc import ABC, abstractmethod

class IOutputStrategy(ABC):
    @abstractmethod
    def write_data(self, data: dict) -> None:
        pass

class ConsoleOutputStrategy(IOutputStrategy):
    def write_data(self, data: dict) -> None:
        data_string = ",".join(str(value) for value in data.values())
        print(f"[КОНСОЛЬ]: {data_string}")

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = None
        try:
            from kafka import KafkaProducer
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("🔧 Обрано стратегію: KAFKA (Успішне підключення)")
        except Exception:
            print(f"⚠️Увага: Не вдалося підключитися до Kafka на {bootstrap_servers}. Сервер Kafka запущено?")
            print("🔧 Обрано стратегію: KAFKA")

    def write_data(self, data: dict) -> None:
        if self.producer:
            self.producer.send(self.topic, data)
            self.producer.flush()
        else:
            data_string = ",".join(str(value) for value in data.values())
            print(f"[ІМІТАЦІЯ KAFKA -> топік '{self.topic}']: {data_string}")
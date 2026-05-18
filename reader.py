import csv
from strategies import IOutputStrategy

class DataReader:
    def __init__(self, output_strategy: IOutputStrategy):
        self.output_strategy = output_strategy

    def process_csv(self, filepath: str) -> None:
        print(f"Починаємо читання файлу: {filepath}...")
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.output_strategy.write_data(row)
            print("Читання завершено успішно.")
        except FileNotFoundError:
            print(f"Помилка: Файл {filepath} не знайдено.")
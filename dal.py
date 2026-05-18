import csv
from sqlalchemy.orm import sessionmaker
from interfaces import IDataAccess

class DataAccessLayer(IDataAccess):
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def read_from_csv(self, filepath: str) -> list:
        data = []
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def save_to_db(self, entities: list) -> None:
        with self.Session() as session:
            for entity in entities:
                session.merge(entity)
            session.commit()
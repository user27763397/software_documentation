from abc import ABC, abstractmethod

class IDataAccess(ABC):
    @abstractmethod
    def read_from_csv(self, filepath: str) -> list:
        pass

    @abstractmethod
    def save_to_db(self, entities: list) -> None:
        pass

class IBusinessLogic(ABC):
    @abstractmethod
    def process_data(self, filepath: str) -> None:
        pass

class IPresentation(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
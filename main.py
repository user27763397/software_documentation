from sqlalchemy import create_engine
from models import Base
from dal import DataAccessLayer
from bll import BusinessLogicLayer
from interfaces import IPresentation, IBusinessLogic

class PresentationLayer(IPresentation):
    def __init__(self, bll: IBusinessLogic):
        self.bll = bll

    def run(self) -> None:
        print("UI: Запуск програми. Ініціалізація завантаження даних...")
        self.bll.process_data("data.csv")
        print("UI: Роботу завершено.")

if __name__ == "__main__":
    engine = create_engine('sqlite:///lab_database.db')
    Base.metadata.create_all(engine)

    dal_instance = DataAccessLayer(engine)
    
    bll_instance = BusinessLogicLayer(dal_instance)
    
    app = PresentationLayer(bll_instance)

    app.run()
import json
from sqlalchemy import create_engine
from models import Base
from dal import DataAccessLayer
from bll import BusinessLogicLayer
from interfaces import IPresentation, IBusinessLogic
from strategies import ConsoleOutputStrategy, KafkaOutputStrategy

def load_config(config_path: str = "config.json") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

class PresentationLayer(IPresentation):
    def __init__(self, bll: IBusinessLogic):
        self.bll = bll

    def run(self) -> None:
        self.bll.process_data("data.csv")

if __name__ == "__main__":
    config = load_config()
    target = config.get("output_target", "console")

    if target == "kafka":
        kafka_conf = config.get("kafka", {})
        strategy = KafkaOutputStrategy(
            bootstrap_servers=kafka_conf.get("bootstrap_servers", "localhost:9092"),
            topic=kafka_conf.get("topic", "songs_data") 
        )
    else:
        strategy = ConsoleOutputStrategy()

    engine = create_engine('sqlite:///lab_database.db')
    Base.metadata.create_all(engine)
    dal_instance = DataAccessLayer(engine)
    bll_instance = BusinessLogicLayer(dal_instance, strategy)
    
    app = PresentationLayer(bll_instance)
    app.run()
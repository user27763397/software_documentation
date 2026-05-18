from interfaces import IBusinessLogic, IDataAccess
from models import User, Account, Song

class BusinessLogicLayer(IBusinessLogic):
    def __init__(self, dal: IDataAccess):
        self.dal = dal

    def process_data(self, filepath: str) -> None:
        print("BLL: Виклик DAL для зчитування даних...")
        raw_data = self.dal.read_from_csv(filepath)
        
        entities_to_save = []
        processed_users = set()
        processed_songs = set()

        print("BLL: Парсинг даних та створення моделей...")
        for row in raw_data:
            if row['user_id'] not in processed_users:
                new_account = Account(
                    account_id=row['account_id'],
                    balance=float(row['balance']),
                    is_active=True
                )
                new_user = User(
                    user_id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    account=new_account
                )
                entities_to_save.append(new_user)
                processed_users.add(row['user_id'])
            
            if row['song_id'] not in processed_songs:
                new_song = Song(
                    song_id=row['song_id'],
                    title=row['title'],
                    artist=row['artist'],
                    genre=row['genre'],
                    price=float(row['price'])
                )
                entities_to_save.append(new_song)
                processed_songs.add(row['song_id'])

        print(f"BLL: Виклик DAL для збереження {len(entities_to_save)} унікальних сутностей...")
        self.dal.save_to_db(entities_to_save)
        print("BLL: Логіка успішно завершена.")
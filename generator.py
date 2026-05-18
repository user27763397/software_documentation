import csv
import uuid
import random

def generate_data(filename="data.csv", num_rows=1050):
    users = []
    for i in range(100):
        user_id = str(uuid.uuid4())
        account_id = str(uuid.uuid4())
        users.append({
            "user_id": user_id,
            "username": f"user_{i}",
            "email": f"user_{i}@example.com",
            "account_id": account_id,
            "balance": round(random.uniform(10.0, 500.0), 2)
        })

    songs = []
    for i in range(200):
        songs.append({
            "song_id": str(uuid.uuid4()),
            "title": f"Song {i}",
            "artist": f"Artist {i%20}",
            "genre": random.choice(["Rock", "Pop", "Jazz", "Electronic"]),
            "price": round(random.uniform(0.99, 15.99), 2)
        })

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "username", "email", "account_id", "balance", 
                         "song_id", "title", "artist", "genre", "price"])
        
        for _ in range(num_rows):
            u = random.choice(users)
            s = random.choice(songs)
            writer.writerow([
                u["user_id"], u["username"], u["email"], u["account_id"], u["balance"],
                s["song_id"], s["title"], s["artist"], s["genre"], s["price"]
            ])
    print(f"Файл {filename} успішно згенеровано ({num_rows} рядків).")

if __name__ == "__main__":
    generate_data()
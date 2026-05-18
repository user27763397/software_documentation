import uuid
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Song


class SongDAL:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Song).all()

    def get_by_id(self, song_id):
        return self.session.query(Song).get(song_id)

    def add(self, song):
        self.session.add(song)
        self.session.commit()

    def update(self):
        self.session.commit()

    def delete(self, song):
        self.session.delete(song)
        self.session.commit()

class SongBLL:
    def __init__(self, dal: SongDAL):
        self.dal = dal

    def get_all_songs(self):
        return self.dal.get_all()

    def get_song(self, song_id):
        return self.dal.get_by_id(song_id)

    def create_song(self, title, artist, genre, price):
        if not title or not artist:
            raise ValueError("Назва та виконавець є обов'язковими")
            
        new_song = Song(
            song_id=str(uuid.uuid4()), 
            title=title, 
            artist=artist, 
            genre=genre, 
            price=float(price)
        )
        self.dal.add(new_song)

    def update_song(self, song_id, title, artist, genre, price):
        song = self.dal.get_by_id(song_id)
        if song:
            song.title = title
            song.artist = artist
            song.genre = genre
            song.price = float(price)
            self.dal.update()

    def delete_song(self, song_id):
        song = self.dal.get_by_id(song_id)
        if song:
            self.dal.delete(song)


app = Flask(__name__)


engine = create_engine('sqlite:///lab_database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

dal = SongDAL(db_session)
bll = SongBLL(dal)



@app.route('/')
def index():
    songs = bll.get_all_songs()
    return render_template('index.html', songs=songs)

@app.route('/song/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        bll.create_song(
            title=request.form['title'],
            artist=request.form['artist'],
            genre=request.form['genre'],
            price=request.form['price']
        )
        return redirect(url_for('index'))
    return render_template('form.html', action="Додати", song=None)

@app.route('/song/edit/<song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = bll.get_song(song_id)
    if request.method == 'POST':
        bll.update_song(
            song_id=song_id,
            title=request.form['title'],
            artist=request.form['artist'],
            genre=request.form['genre'],
            price=request.form['price']
        )
        return redirect(url_for('index'))
    return render_template('form.html', action="Редагувати", song=song)

@app.route('/song/delete/<song_id>', methods=['POST'])
def delete_song(song_id):
    bll.delete_song(song_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    """Site user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True, 
                   )
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )
    
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls,first_name,last_name,email,username,password):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        

class Shared_songs(db.Model):
    __tablename__ = "shared_songs"

    shared_song_id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True, 
                   )

    song_id = db.Column(db.Text, 
                        
                        nullable=False)                   
    song_name = db.Column(db.String(100), nullable=False)
    sender_username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
    receiver_username = db.Column(
    db.String(20),
    db.ForeignKey('users.username'),
    nullable=False,
    )
    note = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    

class Playlists(db.Model):
    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(
        db.String(20),
        db.ForeignKey('users.user_id'),
        nullable=False,
    )
    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=True,
    )

class Lyrics(db.Model):
    __tablename__ = "lyrics"

    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(
        db.String(20),
        db.ForeignKey('users.user_id'),
        nullable=False,
    )


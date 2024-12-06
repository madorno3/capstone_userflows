from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional, DataRequired
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    """User registration form."""

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

class Playlistform(FlaskForm):
    playlist_title = StringField(
        "Playlist",
        validators=[InputRequired(), Length(min=1, max=55)],
    )
    description = StringField(
        "Description",
        validators=[InputRequired(), Length(min=0, max=200)],
    )

class SongForm(FlaskForm):
    song_search = StringField(
        "song",
        validators=[InputRequired(), Length(min=1, max=55)],
    )


class ShareSongForm(FlaskForm):
    song_search = StringField(
        "Song you're sending",  
        validators=[InputRequired(), Length(min=1, max=500)],
    )
    receiver_username = StringField(
        "Receiver Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    note = StringField(
        "What do you want to say?",
        validators=[InputRequired(), Length(min=1, max=500)],
    )


class LyricsSearchForm(FlaskForm):
    artist = StringField(
        "artist",
        validators=[DataRequired(message=None)],
    )
    song = StringField(
        "song",
        validators=[DataRequired(message=None)],
    )
    


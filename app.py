import os
from flask import Flask, render_template, redirect, session, url_for, request, jsonify, flash, url_for, abort 
from models import connect_db, db, Users, Playlists, Lyrics, Shared_songs
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, Playlistform, SongForm, ShareSongForm, LyricsSearchForm
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import json
import argparse
import logging
import requests
from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect()


logger = logging.getLogger('examples.create_playlist')
logging.basicConfig(level='DEBUG')

app = Flask(__name__)
# csrf = CSRFProtect(app)
# csrf.init_app(app)


app.config["SECRET_KEY"] = "abc123"

client_id = '9b3cf596038e484db04c2e5a7f039c93'
client_secret = '675e4f620ac141bab18e49cfc687b093'
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private,playlist-modify-public,playlist-modify-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

app.app_context().push()
connect_db(app)

db.create_all()

# index that links to login and register forms
@app.route("/")
def home():
    return render_template('/index.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = Users.register(first_name, last_name, email, username, password)
        session["user_id"] = user.user_id
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    
    return render_template('/signup.html', form=form)


# login form
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.authenticate(username, password)
        if user:
            session['username'] = user.username
            session['user_id'] = user.user_id  # Assuming you have a user_id attribute
            session.permanent = True
            # app.permanent_session_lifetime = timedelta(days=30)  # Set session lifetime as needed
            return redirect(f"/profile/{user.user_id}")
        else:
            flash("Invalid username or password")
    return render_template('login.html', form=form)


# users profile page that includes lyric search form
@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    form = LyricsSearchForm()
    user = Users.query.get_or_404(user_id)
    display_lyrics = None
    song = None

    if form.validate_on_submit():
        artist = form.artist.data
        song = form.song.data

        try:
            # Make API request
            api_url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
            response = requests.get(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                display_lyrics = data.get('lyrics', '').strip().replace('\r\n', '\n')
            else:
                print(f"API request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            abort(500, description="Error fetching lyrics")
        
    return render_template('/profile.html', form=form, user=user, display_lyrics=display_lyrics, song=song)

# gets playlists
def playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

# gets token from spotfy
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    return redirect(url_for('get_playlists'))

# gets titles. when a title is clicked it redirects to another page which gives the playlist titles
@app.route('/get_playlists', methods=["GET"])
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    username = session.get('username')
    user_id = session.get('user_id')
    if username is None:
        flash("User not logged in")
        return redirect(url_for('login'))
    
    playlists = sp.current_user_playlists()
    print(username)
    print(user_id)
    return render_template('playlists.html', playlists=playlists, username=username,user_id=user_id)

# @app.route('/get_playlists', methods=["GET"])
# def get_playlists():
#     # loop over playlist urls for hyperlinks and playlist details?
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
#     if 'user_id' in session:
#         user_id = session['user_id']
    
#     playlists = sp.current_user_playlists()
#     print(user_id)
    

#     return render_template('playlists.html', playlists=playlists)

# shows playlist details from playlist that was chosen previously
@app.route('/playlist_details/<playlist_id>', methods=["GET", "POST"])
def playlist_details(playlist_id):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    username = session.get('username')
    user_id = session.get('user_id')
    current_playlist = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
    tracks = [[item['track']['name']] for item in current_playlist['tracks']['items']]
    cover_res = sp.playlist_cover_image(playlist_id)
    cover = cover_res[0]['url']

    print(current_playlist)
    return render_template("playlist_details.html", current_playlist=current_playlist, cover=cover, tracks=tracks, user_id=user_id,username=username)



# send songs to another user by accepting form data, saving it to a table, and using the saved data to send requests to spotify
@app.route("/share_song/<username>", methods=["GET", "POST"])
def sharesong(username):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    if "username" not in session or username != session['username']:
            raise Unauthorized()
    username = session.get('username')
    user_id = session.get('user_id')
    user = Users.query.filter_by(username=username).first()
    song=None
    sharesong_form = ShareSongForm()
    song_form = SongForm()
    user_id = user.user_id
    id = None
    name = None

        
    if sharesong_form.validate_on_submit():
        song_search = song_form.song_search.data
        result = sp.search(song_search, limit=1, offset=0, type='track', market=None)
        id = [item['id'] for item in result['tracks'].get('items', [])]
        song_id = ''.join(id)
        name = [item['name'] for item in result['tracks'].get('items', [])]
        url_list = [item['external_urls']['spotify'] for item in result['tracks'].get('items', [])]
        url = ''.join(url_list)
        song_name = ''.join(name)
        sender_username = user.username
        receiver_username = sharesong_form.receiver_username.data
        note = sharesong_form.note.data
        shared_song = Shared_songs(song_id=song_id,song_name=song_name,sender_username=sender_username,receiver_username=receiver_username,note=note,url=url)
        db.session.add(shared_song)
        db.session.commit()
        return render_template("shared_song_sucess.html")
    return render_template("share_song.html", user=user, sharesong_form=sharesong_form,song_form=song_form, user_id=user_id, username=username)

# a list of the messages/songs the user has sent to others
@app.route("/<username>/sent_messages", methods=["GET", "POST"])
def messages(username):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    # Check if the user exists
    username = session.get('username')
    user_id = session.get('user_id')
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    sent_notes = Shared_songs.query.filter_by(sender_username=username).all()
    
    return render_template("sent_messages.html", user=user, sent_notes=sent_notes, username=username, user_id=user_id)


# a list of messages/songs the user has received
@app.route("/<username>/inbox", methods=["GET", "POST"])
def inbox(username):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    username = session.get('username')
    user_id = session.get('user_id')
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    received_notes = Shared_songs.query.filter_by(receiver_username=username).all()
    
    return render_template("inbox.html", user=user, received_notes=received_notes, user_id=user_id,username=username)

# user logout
@app.route('/logout/<username>')
def logout(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    session.pop("username")
    return redirect("/")

# allows user to delete a song from the '/new_playlist_details' and redirects to "/updated_playlist"
@app.route('/delete_track/<id>')
def delete_playlist(id):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    playlists = sp.current_user_playlists()
    playlist_id = playlists['items'][0]['id']
    results = sp.playlist_remove_all_occurrences_of_items(playlist_id,[id],snapshot_id=None)
    return redirect("/updated_playlist")


#route that gives playlist details for a newly created playlist and searches for songs to add to the playlist
# songs that are deleted will redirect to "/delete_track/<id>"
@app.route('/new_playlist_details', methods=["GET", "POST"])
def new_playlist_details():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    username = session.get('username')
    user_id = session.get('user_id')
    
    playlists = sp.current_user_playlists()
    
    playlist_id = playlists['items'][0]['id']
    form = SongForm()
    result = None
    song = None
    playlist_info = []
    playlist_tracks = []
    cover_res=None
    cover=None
    track_id=None
    pl_ids=[]
    track_int=None
    pl_ids_strings = []
    
    if form.validate_on_submit():
        song_search = form.song_search.data
        result = sp.search(song_search, limit=1, offset=0, type='track', market=None)
        track_id = [item['id'] for item in result['tracks'].get('items', [])]
        song = [item['name'] for item in result['tracks'].get('items', [])]
        new_pl_track = sp.playlist_add_items(playlist_id, track_id, position=None)
        playlist_info = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
        playlist_tracks = [[item['track']['name']] for item in playlist_info['tracks']['items']]
        
        pl_ids = [[item['track']['id']] for item in playlist_info['tracks']['items']]
        pl_ids_strings = [item[0] for item in pl_ids]

        cover_res = sp.playlist_cover_image(playlist_id)
        cover = cover_res[0]['url']
        
       
    return render_template('/new_playlist_details.html', 
                           playlists=playlists,
                           form=form,
                           cover=cover,
                           playlist_info=playlist_info,
                           playlist_tracks=playlist_tracks,
                           pl_ids_strings=pl_ids_strings,
                           username=username,
                           user_id=user_id
                           )

# once a song was deleted from a newly created playlist, and redirected to 'delete_track/<id>' it leads here. it lists the playlist without the deleted song.
# if a song is deleted here, it will show the rest of the playlist without the deleted song.
@app.route('/updated_playlist', methods=["GET", "POST"])
def update_playlist():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    username = session.get('username')
    user_id = session.get('user_id')
    playlists = sp.current_user_playlists()
    playlist_id = playlists['items'][0]['id']
    form = SongForm()
    result = None
    song = None
    playlist_info = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
    playlist_tracks = [[item['track']['name']] for item in playlist_info['tracks']['items']]
    pl_ids = [[item['track']['id']] for item in playlist_info['tracks']['items']]
    pl_ids_strings = [item[0] for item in pl_ids]
    cover_res = sp.playlist_cover_image(playlist_id)
    cover = cover_res[0]['url']

    if form.validate_on_submit():
        song_search = form.song_search.data
        result = sp.search(song_search, limit=1, offset=0, type='track', market=None)
        track_id = [item['id'] for item in result['tracks'].get('items', [])]
        song = [item['name'] for item in result['tracks'].get('items', [])]
        new_pl_track = sp.playlist_add_items(playlist_id, track_id, position=None)
        playlist_info = sp.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
        playlist_tracks = [[item['track']['name']] for item in playlist_info['tracks']['items']]
        
        pl_ids = [[item['track']['id']] for item in playlist_info['tracks']['items']]
        pl_ids_strings = [item[0] for item in pl_ids]
        cover_res = sp.playlist_cover_image(playlist_id)
        cover = cover_res[0]['url']
            
    return render_template('/new_playlist_details.html', 
                           playlists=playlists,
                           form=form,
                           cover=cover,
                           playlist_info=playlist_info,
                           playlist_tracks=playlist_tracks,
                           playlist_id=playlist_id,
                           pl_ids_strings=pl_ids_strings,
                           username=username,
                           user_id=user_id
                           )


# route that creates playlist. Makes playlist title and description and posts to Spotify
@app.route('/make_playlist', methods=["GET", "POST"])
def main():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    form = Playlistform()
    username = session.get('username')
    user_id = session.get('user_id')
    if form.validate_on_submit():

        playlist_title = form.playlist_title.data
        description = form.description.data
        print(sp.me()['id'])
        user_id = sp.me()['id']
        sp.user_playlist_create(user_id, playlist_title, description=description)

        return redirect("/new_playlist_details")
    else:
        return render_template("/new_playlist.html", form=form, username=username, user_id=user_id)

# deletes user
@app.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

# logs out of spotify
@app.route('/spotify_logout')
def spotify_logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)





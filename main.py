import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id="Your client id",
        client_secret="Your client secret",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
type_chart = input("Which type of chart do you want the songs from? Type number corresponding to your choice:\n1) Hot 100  2) Year end Hot 100  3) Hot Trending Songs of the week  :")
if type_chart == "1":
    a = input("Enter the date you want the songs from in yyyy-mm-dd format: ")
    num_song = int(input("How many songs do you want in your playlist: "))
    year = a.split("-")[0]
    url = requests.get(f"https://www.billboard.com/charts/hot-100/{a}")
    soup = BeautifulSoup(url.text, "html.parser")
    name = soup.select("li h3")
    if num_song < 93:
        songs = [((name[i].getText()).replace("\n", "")).replace("\t", "") for i in range(0, num_song+7)]
    else:
        songs = [((name[i].getText()).replace("\n", "")).replace("\t", "") for i in range(0, num_song)]
    song_uris = []
    for song in songs:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
            print(song)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    if len(song_uris)>num_song:
        for i in range(0,len(song_uris)-num_song):
            song_uris.pop(-1)
    playlists = sp.user_playlist_create(user=user_id, name=f"{a} Billboard Top {num_song}",public=False)
    print(playlists["external_urls"]["spotify"])
    sp.user_playlist_add_tracks(playlist_id=playlists["id"], tracks=song_uris, user=user_id)
elif type_chart == "2":
    a = input("Enter the year you want the songs from: ")
    num_song = int(input("How many songs do you want in your playlist: "))
    url = requests.get(f"https://www.billboard.com/charts/year-end/{a}/hot-100-songs/")
    soup = BeautifulSoup(url.text, "html.parser")
    name = soup.select("li h3")
    if num_song < 93:
        songs = [((name[i].getText()).replace("\n", "")).replace("\t", "") for i in range(0, num_song + 7)]
    else:
        songs = [((name[i].getText()).replace("\n", "")).replace("\t", "") for i in range(0, num_song)]
    song_uris = []
    for song in songs:
        result = sp.search(q=f"track:{song} year:{a}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
            print(song)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    if len(song_uris)>num_song:
        for i in range(0,len(song_uris)-num_song):
            song_uris.pop(-1)
    playlists = sp.user_playlist_create(user=user_id, name=f"{a} Billboard Top {num_song}", public=False)
    print(playlists["external_urls"]["spotify"])
    sp.user_playlist_add_tracks(playlist_id=playlists["id"], tracks=song_uris, user=user_id)
elif type_chart == "3":
    a = input("Enter the date you want the songs of the week from in yyyy-mm-dd format: ")
    num_song = int(input("How many songs do you want in your playlist (max-20): "))
    year = a.split("-")[0]
    url = requests.get(f"https://www.billboard.com/charts/twitter-hot-trending-songs/{a}/")
    soup = BeautifulSoup(url.text, "html.parser")
    name = soup.select("li h3")
    song_uris = []
    songs = [((name[i].getText()).replace("\n", "")).replace("\t", "") for i in range(0, 20)]
    for song in songs:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
            print(song)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    if len(song_uris)>num_song:
        for i in range(0,len(song_uris)-num_song):
            song_uris.pop(-1)
    playlists = sp.user_playlist_create(user=user_id, name=f"{a} Billboard Top {num_song} of the week",public=False)
    print(playlists["external_urls"]["spotify"])
    sp.user_playlist_add_tracks(playlist_id=playlists["id"], tracks=song_uris, user=user_id)
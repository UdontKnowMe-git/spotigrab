try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import yt_dlp
    import os
    import configparser
except Exception as e:
    print(e)
    print("Please install the required packages using the command: pip install -r requirements.txt")

config = configparser.ConfigParser()
config.read('config.ini')

# Spotify API credentials | Replace with your own credentials in config.ini file
SPOTIPY_CLIENT_ID = config['Spotify']['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = config['Spotify']['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = config['Spotify']['SPOTIPY_REDIRECT_URI']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"))

def get_liked_songs():
    liked_songs = []
    results = sp.current_user_saved_tracks()

    for item in results['items']:
        track = item['track']
        song_name = track['name']
        artist_name = track['artists'][0]['name']
        liked_songs.append(f"{song_name} - {artist_name}")

    return liked_songs

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'default_search': 'ytsearch',
        'format': 'bestaudio/best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in result:
            return result['entries'][0]['webpage_url']
        return None

# Download the song as MP3
def download_song(video_url, song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"downloads/{song_name}.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

os.makedirs("Downloads", exist_ok=True)

# Main function: Fetch, Search, Download
def main():
    liked_songs = get_liked_songs()
    
    for song in liked_songs:
        print(f"Searching for: {song}...")
        video_url = search_youtube(song)
        
        if video_url:
            print(f"Downloading: {song} from {video_url}")
            download_song(video_url, song)
        else:
            print(f"❌ No match found for {song}")

    print("✅ All downloads complete!")

# Run the script
if __name__ == "__main__":
    main()
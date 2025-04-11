try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import yt_dlp
    import os
    import configparser
    import concurrent.futures
    import signal
    import sys
    from tqdm import tqdm

except Exception as e:
    print(e)
    print("Please install the required packages using: pip install -r requirements.txt")
    exit(1)

# Read config file
config = configparser.ConfigParser()
config.read("config.ini")

# Load Spotify API credentials
try:
    SPOTIFY_CLIENT_ID = config["spotify"]["client_id"]
    SPOTIFY_CLIENT_SECRET = config["spotify"]["client_secret"]
    SPOTIFY_REDIRECT_URI = config["spotify"]["redirect_uri"]
    THREAD_COUNT = int(config["settings"]["thread_count"])  # Read thread count from config
    PLAYLIST_NAME = config["settings"]["playlist_name"]  # Read playlist name
except KeyError:
    raise ValueError("❌ Missing settings in config.ini")

# Spotify API Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-library-read playlist-read-private"
))

# Ensure downloads folder exists
os.makedirs("downloads", exist_ok=True)

# Graceful exit handler
executor = concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT)

def graceful_exit(signal, frame):
    print("\n🛑 Stopping downloads safely...")
    executor.shutdown(wait=True)  # Wait for active threads to finish
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)

# Fetch liked songs
def get_liked_songs():
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  # Get 50 songs per request

    while results:
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            liked_songs.append(f"{song_name} - {artist_name}")

        results = sp.next(results) if results['next'] else None  # Pagination

    return liked_songs

# Fetch songs from a specific playlist
def get_playlist_songs(playlist_name):
    playlists = sp.current_user_playlists(limit=50)  # Get all playlists
    playlist_id = None

    for playlist in playlists["items"]:
        if playlist["name"].lower() == playlist_name.lower():
            playlist_id = playlist["id"]
            break

    if not playlist_id:
        print(f"❌ Playlist '{playlist_name}' not found! Defaulting to liked songs.")
        return get_liked_songs()

    songs = []
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            songs.append(f"{song_name} - {artist_name}")

        results = sp.next(results) if results['next'] else None  # Pagination

    return songs

# Search for a song on YouTube
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

# Download the song as MP3 (with retry logic)
def download_song(song, retries=3):
    file_path = f"downloads/{song}.mp3"

    if os.path.exists(file_path):
        print(f"✅ {song} already exists. Skipping download.")
        return

    video_url = search_youtube(song)

    if not video_url:
        print(f"❌ No match found for {song}")
        return

    print(f"⬇ Downloading: {song} from {video_url}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path.replace(".mp3", ".%(ext)s"),  # Correct file format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'socket_timeout': 30  # Increase timeout to prevent failures
    }

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print(f"✅ Downloaded {song}")
            return
        except Exception as e:
            print(f"⚠️ Error downloading {song}: {e}")
            if attempt < retries - 1:
                print("🔄 Retrying...")
            else:
                print("❌ Failed after multiple attempts.")

# Main function: Fetch, Search, Download
def main():
    if PLAYLIST_NAME.lower() == "liked songs":
        songs = get_liked_songs()
    else:
        songs = get_playlist_songs(PLAYLIST_NAME)

    print(f"🎶 Found {len(songs)} songs from '{PLAYLIST_NAME}'. Downloading with {THREAD_COUNT} threads...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        list(tqdm(executor.map(download_song, songs), total=len(songs), desc="Downloading Songs"))

    print("✅ All downloads complete!")

# Run the script
if __name__ == "__main__":
    main()

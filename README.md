Here's your **`README.md`** for your banger of an app! 🚀🎵  

---

# **SpotiGrab** 🎶🚀  
**Download your Spotify liked songs or playlist tracks effortlessly as high-quality MP3s!**  

## **🔥 Features**  
✅ **Fetch Liked Songs** – Automatically get your entire liked songs list from Spotify.  
✅ **Download from YouTube** – Finds and downloads the best quality MP3 using YouTube.  
✅ **Multithreaded Downloads** – Faster downloads using multiple threads (configurable).  
✅ **Safe Exit** – Press `CTRL+C` anytime, and the app will stop gracefully.  
✅ **Playlist Support** – Choose a specific Spotify playlist to download.  
✅ **Skip Already Downloaded Songs** – Avoid duplicate downloads and save time.  

---

## **🔧 Setup & Installation**  

### **1️⃣ Install Dependencies**  
Make sure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### **2️⃣ Configure `config.ini`**  
Create a `config.ini` file and add your **Spotify API credentials**:  
```ini
[spotify]
client_id = your_client_id
client_secret = your_client_secret
redirect_uri = http://127.0.0.1:8888/callback

[settings]
threads = 5  # Adjust thread count for parallel downloads
```

### **3️⃣ Get Your Spotify API Credentials**  
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).  
2. Create an **app** and get your `client_id` and `client_secret`.  
3. Set the **Redirect URI** to `http://127.0.0.1:8888/callback`.  

---

## **🚀 Usage**  

### **1️⃣ Run the Script**  
```bash
python main.py
```

### **2️⃣ Choose What to Download**  
- **Liked Songs** – The script fetches your liked songs by default.  
- **Playlist Tracks** – Select a playlist when prompted.  

### **3️⃣ Enjoy Your Music Offline!** 🎧  

---

## **📌 Notes**  
- Downloads are saved in the **`downloads/`** folder.  
- If a song is already downloaded, it **won’t be downloaded again**.  
- To **increase speed**, adjust the `threads` count in `config.ini`.  

---

## **📜 License**  
This project is for **educational purposes only**. Do not use it for piracy. 🎵🚀  

---
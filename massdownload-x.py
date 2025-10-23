import os
import glob
import yt_dlp
import snscrape.modules.twitter as sntwitter

# --- CONFIG ---
USERNAME = "target_username"   # ganti dengan username target (tanpa @)
MAX_TWEETS = 1000              # maksimal tweet yang diperiksa
OUTDIR = r"D:\twit"            # folder tujuan di D:\twit
ID_LOG = os.path.join(OUTDIR, "downloaded_ids.txt")
# ----------------

os.makedirs(OUTDIR, exist_ok=True)

def sanitize_filename(text):
    """Hilangkan karakter ilegal di nama file Windows."""
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.strip().replace("\n", " ")
    return text

def get_caption_prefix(text, n=5):
    """Ambil n kata pertama dari caption tweet."""
    if not text:
        return "no_caption"
    words = text.split()
    prefix = " ".join(words[:n])
    return sanitize_filename(prefix)

def download_tweet_video(tweet_url, prefix):
    """Download video dari tweet dengan awalan nama file custom."""
    outtmpl = os.path.join(OUTDIR, f"{prefix}_%(upload_date)s_%(id)s.%(ext)s")
    ydl_opts = {
        'outtmpl': outtmpl,
        'format': 'bestvideo+bestaudio/best',
        'quiet': False,
        'no_warnings': True,
        'cachedir': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([tweet_url])
            return True
        except Exception as e:
            print(f"[ERROR] Gagal mendownload {tweet_url}: {e}")
            return False

def already_downloaded(tweet_id):
    # cek file di OUTDIR yang berisi _<tweet_id>.<ext>
    pattern = os.path.join(OUTDIR, f"*_{tweet_id}.*")
    matches = glob.glob(pattern)
    return len(matches) > 0

def append_id_log(tweet_id):
    try:
        with open(ID_LOG, "a", encoding="utf-8") as f:
            f.write(f"{tweet_id}\n")
    except Exception:
        pass  # jangan crash karena logging

def download_tweet_video(tweet_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([tweet_url])
            return True
        except Exception as e:
            print(f"[ERROR] Gagal mendownload {tweet_url}: {e}")
            return False

def main():
    print(f"Mulai scraping tweets dari @{USERNAME}. Output ke: {OUTDIR}")
    scraped = 0
    downloaded_count = 0

    for tweet in sntwitter.TwitterUserScraper(USERNAME).get_items():
        if scraped >= MAX_TWEETS:
            break
        scraped += 1

        media = getattr(tweet, "media", None)
        if not media:
            continue

        # deteksi video / animated gif
        has_video = any(getattr(m, "type", "").lower() in ("video", "animated_gif") for m in media)
        if not has_video:
            continue

        tweet_id = tweet.id
        if already_downloaded(tweet_id):
            print(f"Skip tweet {tweet_id} — sudah ada file di {OUTDIR}")
            continue

        tweet_url = f"https://twitter.com/{tweet.user.username}/status/{tweet_id}"
        print(f"Downloading media from {tweet_url} ...")
        success = download_tweet_video(tweet_url)
        if success:
            downloaded_count += 1
            append_id_log(tweet_id)

    print(f"Selesai. Total video didownload: {downloaded_count}")

if __name__ == "__main__":
    main()

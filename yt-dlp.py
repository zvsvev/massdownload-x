import os
import subprocess

# Folder output
output_dir = r"D:\twit"
os.makedirs(output_dir, exist_ok=True)

# File yang berisi list tweet URL, satu URL per baris
input_file = "tweet.txt"

def download_tweet_video(url):
    # Template output filename: pakai ID tweet + ekstensi
    output_template = os.path.join(output_dir, '%(id)s.%(ext)s')

    # Command yt-dlp untuk download best video + best audio dan merge otomatis
    command = [
        'yt-dlp',
        '-f', 'bestvideo+bestaudio',
        '-o', output_template,
        url
    ]

    print(f"Downloading: {url}")
    try:
        subprocess.run(command, check=True)
        print("Downloaded successfully.\n")
    except subprocess.CalledProcessError:
        print("Failed to download.\n")

def main():
    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        download_tweet_video(url)

if __name__ == "__main__":
    main()

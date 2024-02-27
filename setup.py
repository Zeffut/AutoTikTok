import time, os, yt_dlp
from save_shorts import get_short_links

def download_random_video(csv_file_path, output_folder):
    video_link = "https://www.youtube.com/shorts/lNDUe267U8E?"
    output_file_path = os.path.join(output_folder, "video.mp4")
    ydl_opts = {
        'outtmpl': output_file_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])

def main():
    print("[-] Starting setup...")
    time.sleep(3)
    channel_url = input("[-] Enter the youtube channel URL you choose : ")
    get_short_links(channel_url)
    print("[-] Shorts links saved !")
    print("[-] Youtube downloader setup...")
    download_random_video("short_links.csv", "VideosDirPath")
    os.remove(os.path.join("VideosDirPath", "video.mp4"))

    print("[+] Setup complete !")
    print("[-] Closing in 5 seconds...")
    time.sleep(5)
    exit()

main()

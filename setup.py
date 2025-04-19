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
    
    # Ask for the number of channels to add
    while True:
        try:
            num_channels = int(input("[-] How many YouTube channels would you like to add? "))
            if num_channels > 0:
                break
            print("[-] Please enter a positive number.")
        except ValueError:
            print("[-] Please enter a valid number.")
    
    # Collect the URLs of the channels
    channel_urls = []
    for i in range(num_channels):
        channel_url = input(f"[-] Enter the URL of YouTube channel {i+1}/{num_channels}: ")
        channel_urls.append(channel_url)
    
    # Process each channel
    for i, channel_url in enumerate(channel_urls, 1):
        print(f"[-] Processing channel {i}/{num_channels}...")
        get_short_links(channel_url)
    
    print("[-] All short links have been saved!")
    print("[-] Youtube downloader setup...")
    download_random_video("short_links.csv", "VideosDirPath")
    os.remove(os.path.join("VideosDirPath", "video.mp4"))

    print("[+] Setup complete!")
    print("[-] Closing in 5 seconds...")
    time.sleep(5)
    exit()

main()

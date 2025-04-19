import time
import random
import csv
import yt_dlp
import os
from tiktok_uploader.upload import upload_video
from datetime import datetime
import pytz
import requests

def upload(video_name, video_title):
    upload_video(video_name, video_title, headless=True, cookies="cookies.txt", browser="chromium")

def download_random_video(csv_file_path, output_folder):
    print("Downloading random video...")
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        random_row = random.choice(rows)
        video_name, video_link = random_row[1].strip(), random_row[0].strip()
        output_file_path = os.path.join(output_folder, "video.mp4")
        ydl_opts = {
            'outtmpl': output_file_path,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])

        return video_name

def send_telegram_message(chat_id, message):
    bot_token = ''  # Replace with your bot token
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Optionnel, pour le formatage
    }
    response = requests.post(url, json=payload)
    return response.json()

def daily_task():
    csv_file_path = "short_links.csv"
    output_folder = "VideosDirPath"
    tags = " #setup #your #hashtags #here"
    title = download_random_video(csv_file_path, output_folder)
    title = clean_title(title) + tags
    video_path = os.path.join(output_folder, "video.mp4")
    print("Uploading video...")
    upload(video_path, title)
    
    chat_id = ''
    message = f"Video posted : {title}"
    send_telegram_message(chat_id, message)
    
    os.remove(video_path)

def clean_title(title):
    parties = title.split("#", 1)
    nouveau_titre = parties[0].strip()
    return nouveau_titre

def main():
    #Best hours for all days
    Monday = ['06:00', '10:00', '22:00']
    Tuesday = ['02:00', '04:00', '09:00']
    Wednesday = ['07:00', '08:00', '23:00']
    Thursday = ['09:00', '12:00', '19:00']
    Friday = ['05:00', '13:00', '15:00']
    Saturday = ['11:00', '19:00', '20:00']
    Sunday = ['07:00', '08:00', '16:00']
    print("Starting...")
    daily_task()
    
    try:
        # Set the French timezone
        timezone = pytz.timezone('Europe/Paris')
        
        while True:
            # Obtenir l'heure actuelle en France
            now = datetime.now(timezone)
            jour = now.strftime("%A")
            heure = now.strftime("%H:%M")
            
            if jour == "Monday":
                if heure in Monday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Tuesday":
                if heure in Tuesday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Wednesday":
                if heure in Wednesday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Thursday":
                if heure in Thursday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Friday":
                if heure in Friday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Saturday":
                if heure in Saturday:
                    daily_task()
                    time.sleep(60)
            elif jour == "Sunday":
                if heure in Sunday:
                    daily_task()
                    time.sleep(60)

            time.sleep(1)
            print("Date : " + now.strftime("%H:%M:%S %d/%m/%Y"))
    except KeyboardInterrupt:
        print("Stopping...")

main()

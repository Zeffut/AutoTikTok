import time
import random
import csv
import yt_dlp
import os
from api import tiktok_cli
from datetime import datetime

def upload(video_name, video_title):
    class ArgsNamespace:
        subcommand = "upload"
        users = "zeffut"
        video = video_name
        title = video_title
        schedule = 0
        comment = 1
        duet = 0
        stitch = 0
        visibility = 0
        brandorganic = 0
        brandcontent = 0
        ailabel = 0
        proxy = ""
        youtube = None
    args = ArgsNamespace()
    tiktok_cli(args)

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

def daily_task():
    csv_file_path = "short_links.csv"
    output_folder = "VideosDirPath"
    tags = " #tags #examples"
    title = download_random_video(csv_file_path, output_folder)
    title = clean_title(title) + tags
    upload("video.mp4", title)
    os.remove(os.path.join(output_folder, "video.mp4"))

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

    try:
        while True:
            jour = time.strftime("%A")
            heure = time.strftime("%H:%M")
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
            print("Date : " + time.strftime("%H:%M:%S %d/%m/%Y"))
    except KeyboardInterrupt:
        print("Stopping...")

main()

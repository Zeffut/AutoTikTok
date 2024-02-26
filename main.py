import time
import subprocess
import random
import csv
import yt_dlp
import os
from api import tiktok_cli
from datetime import datetime

def upload(video_name, video_title):
    print("Envoi de la vidéo...")
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
    print("Téléchargement d'une vidéo aléatoire...")
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
    print("Action quotidienne en cours...")
    csv_file_path = "short_links.csv"
    output_folder = "VideosDirPath"
    tags = " #argent #yomidenzel #buisness #entrepreneur #foryou #fyp #foryoupage #tiktok #oussamaammar #podcast"
    title = download_random_video(csv_file_path, output_folder)
    title = clean_title(title) + tags
    upload("video.mp4", title)
    os.remove(os.path.join(output_folder, "video.mp4"))

def get_current_time():
    return time.strftime("%A %H:%M")

def clean_title(title):
    parties = title.split("#", 1)
    nouveau_titre = parties[0].strip()
    return nouveau_titre


def main():
    heures_minutes_jours = [
        ('Monday', ['06:00', '10:00', '22:00']),
        ('Tuesday', ['02:00', '04:00', '09:00']),
        ('Wednesday', ['07:00', '08:00', '23:00']),
        ('Thursday', ['09:00', '12:00', '19:00']),
        ('Friday', ['05:00', '13:00', '15:00']),
        ('Saturday', ['11:00', '19:00', '20:00']),
        ('Sunday', ['07:00', '08:00', '16:00']),
    ]

    try:
        while True:
            current_time = get_current_time()
            for day, times in heures_minutes_jours:
                if current_time in times:
                    daily_task()
                    print(f"Action quotidienne effectuée pour {day} à {current_time}.")
                    time.sleep(60)
            time.sleep(10)
            print("Date : " + current_time)
    except KeyboardInterrupt:
        print("Arrêt du programme.")

main()

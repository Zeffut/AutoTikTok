import yt_dlp
import csv
import os

def get_short_links(channel_url, output_csv='short_links.csv'):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_end': 100,
    }

    # Modifie le format de l'URL si nécessaire
    if '/@' in channel_url:
        channel_username = channel_url.split('/@')[1].split('/')[0]
        channel_url = f'https://www.youtube.com/@{channel_username}/shorts'
    else:
        # Supprime les parties inutiles de l'URL
        suffixes_to_remove = ['/about', '/community', '/playlist', '/playlists', '/streams', '/featured', '/videos']
        for suffix in suffixes_to_remove:
            channel_url = channel_url.split(suffix)[0]
        channel_url += '/shorts'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url, download=False)
        if 'entries' in result:
            video_info_list = []
            existing_links = set()

            # Lire les liens existants si le fichier existe
            if os.path.isfile(output_csv):
                with open(output_csv, 'r', newline='', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if row:  # Vérifier que la ligne n'est pas vide
                            existing_links.add(row[0])  # Ajouter le lien à l'ensemble

            for entry in result['entries']:
                video_id = entry['id']
                video_title = entry.get('title', 'N/A')
                short_link = f'https://www.youtube.com/shorts/{video_id}'

                # Vérifier si le lien n'existe pas déjà
                if short_link not in existing_links:
                    video_info_list.append((short_link, video_title))

            # Enregistre la liste dans un fichier CSV en mode 'a' (append) si le fichier existe, sinon en mode 'w' (write)
            with open(output_csv, mode='a' if os.path.isfile(output_csv) else 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                # Écrit l'en-tête seulement si le fichier vient d'être créé
                if not os.path.isfile(output_csv):
                    csv_writer.writerow(['Short Link', 'Video Title'])

                for video_info in video_info_list:
                    csv_writer.writerow(video_info)

            print(f"[+] {len(video_info_list)} nouveaux liens ont été ajoutés à {output_csv}")
            return video_info_list
        else:
            print("[-] Aucune vidéo trouvée sur la chaîne.")
            return []
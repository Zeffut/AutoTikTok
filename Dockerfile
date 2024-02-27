FROM python:3.12
RUN apt-get update && apt-get install -y python3.10 ffmpeg
COPY . .
RUN pip install -r requirements.txt
CMD ["python3 setup.py"]
CMD ["python3 main.py"]

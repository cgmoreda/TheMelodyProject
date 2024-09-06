FROM debian:unstable-slim

# Set the working directory

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y wget

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 

RUN dpkg -i google-chrome-stable_current_amd64.deb  # problem here
RUN apt -f install -y

RUN rm google-chrome-stable_current_amd64.deb

COPY . /app



RUN pip install -r requirments.txt


RUN google-chrome



CMD ["python3", "Melody.py"]

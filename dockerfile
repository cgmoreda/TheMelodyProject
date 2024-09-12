FROM python:3.11.9-bookworm

# Set the working directory
WORKDIR /app

# Install dependencies as root
USER root

RUN apt-get update && \
    apt-get install -y wget xvfb fonts-liberation libnss3 libxss1 libappindicator3-1 libgbm-dev

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Handle broken dependencies if any
RUN apt-get -f install -y

# Add a new user
ARG user=appuser
ARG group=appuser
ARG uid=1000
ARG gid=1000

RUN groupadd -g ${gid} ${group} && \
    useradd -u ${uid} -g ${group} -s /bin/sh -m ${user}





# Create a script to run Xvfb and Chrome
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1280x1024x24 &\n\
export DISPLAY=:99\n\
sleep 5\n\
python3 Melody.py' > /app/start.sh && chmod +x /app/start.sh

# Switch to the new user
USER ${uid}:${gid}

COPY ./requirments.txt /app/requirments.txt

RUN pip install -r requirments.txt

# Copy application files
COPY . /app

EXPOSE 443:443 
EXPOSE 80:80

# Default command to run the script
CMD ["/app/start.sh" ]

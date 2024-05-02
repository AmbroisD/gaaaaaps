# Dockerfile

FROM debian:bookworm-20240311

LABEL maintainer="OCA Team version: 0.1"

# Create a user and group for the application
RUN groupadd -g 1000 sysop && useradd -u 1000 -g sysop sysop

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    zsh \
    wget \
    gnupg \
    vim \
    software-properties-common \
    python3 \
    python3-pip \
    python3-fastapi \
    python3-uvicorn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
#RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
#RUN apt-get update && apt-get install -y nodejs

# Install FastAPI and Uvicorn
#RUN pip install fastapi uvicorn

# Copy the FastAPI application code #--chown=sysop:sysop
#COPY ../gaaaaaps /gaps 
#WORKDIR /gaps

# Copie du répertoire de l'application dans l'image Docker
COPY . /app
COPY static /app/gaaaaaps/static
COPY templates/app.html /app/gaaaaaps/app.html

# Copie du fichier cronjob dans le répertoire cron.d
COPY config/cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob

RUN chmod +x /app/config/start.sh

WORKDIR /app/gaaaaaps

EXPOSE 8000

# Démarre le script de démarrage au démarrage du conteneur
CMD ["/app/config/start.sh"]


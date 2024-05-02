#!/bin/bash

# Démarrer le service cron en arrière-plan
cron -f &

python3 /app/config/init_config.py &

# Démarrer l'application FastAPI
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000

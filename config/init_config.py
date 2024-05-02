import os
import json

DEFAULT_CONFIG = {
    "available_year": ["2024"],
    "white_list": ["ISO"]
}

def main():
    config_dir = "/config"
    config_file = os.path.join(config_dir, "config.json")

    # Vérifie si le répertoire de configuration existe
    if not os.path.exists(config_dir):
        print(f"Error: Configuration directory {config_dir} does not exist.")
        exit(1)

    # Vérifie si le fichier de configuration existe
    if not os.path.exists(config_file):
        print("Creating default configuration file...")
        with open(config_file, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

if __name__ == "__main__":
    main()

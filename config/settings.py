import os

class Settings:
    SESSION_DIR = os.path.join("instaloader")
    os.makedirs(SESSION_DIR, exist_ok=True)
    
    DOWNLOAD_DIR = os.path.join("Downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

settings = Settings()
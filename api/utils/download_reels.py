from pathlib import Path
import instaloader
import json
from django.conf import settings

def load_instaloader_session(username):
    """
    Loads an Instaloader session from a saved cookie file.
    """
    session_dir = settings.BASE_DIR / "sessions"
    session_file = session_dir / f"instagram_cookies_{username}.json"
    try:
        loader = instaloader.Instaloader()

        # Load session cookies from JSON file
        with open(session_file, "r") as file:
            cookies = {cookie["name"]: cookie["value"] for cookie in json.load(file)}

        loader.load_session(username=username, session_data=cookies)
        print(f"Session loaded successfully for {username}.")
        return loader
    except FileNotFoundError:
        print("Session file not found. Please ensure you have logged in and saved cookies.")
        raise
    except Exception as e:
        print(f"Error loading session: {e}")
        raise

def download_instagram_reel(username: str, reel_url: str):
    """
    Downloads a single Instagram reel using Instaloader.
    """
    try:
        # Initialize Instaloader
        loader = load_instaloader_session(username)
        
        reel_shortcode = reel_url.split("/")[-2]
        
        reel = instaloader.Post.from_shortcode(loader.context, reel_shortcode)
        
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'reel'
        target_dir.mkdir(exist_ok=True)
        loader.download_post(reel, target=target_dir)
        
        
        post_details = [{
            # "username": reel.owner_username,
            # "reel_url": reel_url,
            # "shortcode": reel.shortcode,
            # "caption": reel.caption or "No caption",
            "media_url": [str(f) for f in target_dir.iterdir() if f.suffix in [".mp4"]]
        }]
        return post_details
    except Exception as e:
        print(f"An error occurred while downloading the reel: {e}")
        raise
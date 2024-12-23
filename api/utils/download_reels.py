from pathlib import Path
import instaloader
import json, shutil
from django.conf import settings
from django.http import HttpRequest

def load_instaloader_session(username):
    """
    Loads an Instaloader session from a saved cookie file.
    """
    session_dir = settings.BASE_DIR / "sessions"
    session_file = session_dir / f"instagram_cookies_{username}.json"
    try:
        loader = instaloader.Instaloader()
        with open(session_file, "r") as file:
            cookies = {cookie["name"]: cookie["value"] for cookie in json.load(file)}
        loader.load_session(username=username, session_data=cookies)
        return loader
    except FileNotFoundError as e:
        raise e
    except Exception as exception:
        raise exception

def download_instagram_reel(request: HttpRequest, username: str, url: str):
    """
    Downloads a single Instagram reel using Instaloader and renames the file.
    """
    try:
        loader = load_instaloader_session(username)
        reel_shortcode = url.split("/")[-2]
        reel = instaloader.Post.from_shortcode(loader.context, reel_shortcode)
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'reel' / reel_shortcode
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        loader.download_post(reel, target=target_dir)
        renamed_file = None
        for file in target_dir.iterdir():
            if file.suffix == ".mp4":
                new_name = f"{reel_shortcode}.mp4"
                new_file_path = target_dir / new_name
                file.rename(new_file_path)
                media_url = request.build_absolute_uri(f'/media/downloads/reel/{reel_shortcode}/{new_file_path.name}')
                renamed_file = media_url
        if renamed_file:
            post_details = {
                "media_url": renamed_file
            }
            return post_details
        else:
            raise FileNotFoundError("Reel file (.mp4) not found in the download directory.")
    except Exception as e:
        print(f"An error occurred while downloading the reel: {e}")
        raise
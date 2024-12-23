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
    except FileNotFoundError:
        raise
    except Exception as e:
        raise

def download_instagram_post(request: HttpRequest, username: str, url: str):
    """
    Downloads a single Instagram post using Instaloader and retrieves the exact file path without lists.
    """
    try:
        loader = load_instaloader_session(username)
        post_shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'posts' / post_shortcode
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        loader.download_post(post, target=target_dir)
        renamed_file = None
        media_data = []
        for file in target_dir.iterdir():
            if not len(file.suffix) > 1:
                if file.suffix == ".jpg":
                    new_name = f"{post_shortcode}.jpg"
                    new_file_path = target_dir / new_name
                    file.rename(new_file_path)
                    media_url = request.build_absolute_uri(f'/media/downloads/posts/{post_shortcode}/{new_file_path.name}')
                    renamed_file = media_url
                    media_data.append({"media_url":renamed_file})
            else:
                if file.suffix == ".jpg":
                    media_url = request.build_absolute_uri(f'/media/downloads/posts/{post_shortcode}/{file.name}')
                    media_data.append({
                        "media_url": media_url
                    })
        print("MEDIA DATA ----->", media_data)
        return media_data
    except Exception as e:
        print(f"An error occurred while downloading the post: {e}")
        raise
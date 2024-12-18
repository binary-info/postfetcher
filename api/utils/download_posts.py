from pathlib import Path
import instaloader
import json, glob
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

def download_instagram_post(username: str, post_url: str):
    """
    Downloads a single Instagram post using Instaloader and retrieves the exact file path without lists.
    """
    try:
        # Initialize Instaloader session
        loader = load_instaloader_session(username)

        # Extract post shortcode from the URL
        post_shortcode = post_url.split("/")[-2]
        
        # Fetch the post using its shortcode
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
        
        # Target directory for downloaded posts
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'posts'
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the post
        loader.download_post(post, target=target_dir)

        # File search pattern
        file_pattern = "*UTC.mp4" if post.is_video else "*UTC.jpg"

        # Find the first matching file without converting to a list
        file_path = None
        for file in target_dir.glob(file_pattern):
            file_path = file
            print("File path -->", file_path)
            break  # Stop after the first match

        if not file_path:
            print("No files found for the downloaded post.")
            return []

        # Convert file path to URL
        media_url = Path(settings.MEDIA_ROOT) / 'downloads' / 'posts' / file.name
        print("media url -->", media_url)

        # Prepare post metadata
        post_details = [{
            # "username": post.owner_username,
            # "post_url": post_url,
            # "shortcode": post.shortcode,
            # "caption": post.caption or "No caption",
            # "media_type": "video" if post.is_video else "image",
            "media_url": str(media_url)  # Single URL
        }]
        
        print("File downloaded to:", file_path)
        return post_details

    except Exception as e:
        print(f"An error occurred while downloading the post: {e}")
        raise
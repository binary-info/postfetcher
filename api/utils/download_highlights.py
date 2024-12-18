from pathlib import Path
import instaloader, json, re, aiohttp
from django.conf import settings
from rest_framework.exceptions import APIException

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
        print("Session loaded Successfully....")
        return loader
    except FileNotFoundError:
        print("Session file not found. Please ensure you have logged in and saved cookies.")
        raise
    except Exception as e:
        print(f"Error loading session: {e}")
        raise

def download_highlight(username: str, url: str):
    """
    Downloads Instagram highlights using the provided link.
    """
    try:
        # Load session
        loader = load_instaloader_session(username)

        # Extract story_media_id from the link
        match = re.search(r"story_media_id=([\d_]+)", url)
        if not match:
            raise ValueError("Invalid link format. Unable to extract story_media_id.")

        story_media_id = match.group(1)
        print(f"Extracted story_media_id: {story_media_id}")
        
        user_id = story_media_id.split("_")[1]
        story_id = story_media_id.split("_")[0]
        # Load the target profile
        profile = instaloader.Profile.from_id(loader.context, user_id)
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'highlights'
        target_username = profile.username
        highlights = loader.get_highlights(profile)
        
        # Download all highlights for the user
        print(f"Downloading highlights for user: {target_username}")
        highlight_metadata = []
        for highlight in highlights:
            for item in highlight.get_items():
                if story_id == str(item.mediaid):
                    print("media id =>", type(item.mediaid))
                    loader.download_storyitem(item, target_dir)
                    file_extension = "mp4" if item.is_video else "jpg"
                    file_pattern = f"*UTC.{file_extension}"  # Files like 2024-12-16_15-55-08_UTC.mp4
                    matching_files = list(target_dir.glob(file_pattern))
                    if matching_files:
                        file_path = matching_files[-1]  # Assuming the most recent match
                        print("File found:", file_path)
                        highlight_metadata.append({
                            # "mediaid":item.mediaid,
                            # "username": target_username,
                            # "highlight_url": item.url,
                            # "media_type": "video" if item.is_video else "image",
                            "media_url": str(file_path)
                            # "timestamp": item.date,
                        })
                        return highlight_metadata
                    
        print("Highlight downloaded successfully.")
        return highlight_metadata
    except Exception as e:
        raise APIException(f"An error occurred: {e}")
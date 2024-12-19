from pathlib import Path
import json, requests, instaloader, re
from django.conf import settings

def load_instaloader_session_for_profile(username):
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

def fetch_instagram_profile(username: str, url: str):
    """
    Downloads the Instagram profile picture and returns profile data.
    """
    try:
        # Initialize Instaloader with session
        loader = load_instaloader_session_for_profile(username)

        # Extract the target username from the URL
        match = re.match(r"https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.-]+)", url)
        if not match:
            raise ValueError(f"Invalid Instagram URL: {url}")

        target_username = match.group(1)

        # Fetch profile data
        profile_data = instaloader.Profile.from_username(loader.context, target_username)
        print(profile_data.userid)
        # Directory for saving profile pictures
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'profile_pictures'
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Download profile picture
        profile_pic_url = profile_data.profile_pic_url
        print("Profile pic URL:", profile_pic_url)

        response = requests.get(profile_pic_url, stream=True)
        if response.status_code == 200:
            filename = target_dir / f"{profile_data.username}_profile_picture.jpg"
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Profile picture saved as {filename}.")

            # Prepare profile data for response
            response_data = [
                {
                    # "username": profile_data.username,
                    # "full_name": profile_data.full_name,
                    # "profile_id":profile_data.userid,
                    "media_url": str(filename)
                }
            ]
            return response_data
        else:
            print(f"Failed to download profile picture. HTTP Status: {response.status_code}")
            return {"message": "Failed to download profile picture."}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise
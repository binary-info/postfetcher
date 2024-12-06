import os
import instaloader
import json
from config.settings import settings

async def get_followees(username: str, target_username: str):
    loader = instaloader.Instaloader()
    session_file = f"{settings.SESSION_DIR}/instagram_cookies_{username}.json"
    try:
        with open(session_file, 'r') as file:
            cookies = {cookie["name"]: cookie["value"] for cookie in json.load(file)}
            
        if not os.path.exists(session_file):
            raise Exception(f"Session file not found for {username}")

        loader.context.load_session(username, cookies)

        profile = instaloader.Profile.from_username(loader.context, target_username)
        followees = [
            {"username": f.username, "full_name": f.full_name, "profile_pic_url": f.profile_pic_url}
            for f in profile.get_followees()
        ]
        return followees

    except instaloader.exceptions.InvalidArgumentException:
        os.remove(session_file)
        raise Exception("Corrupted session file. Please log in again.")
    except instaloader.exceptions.ConnectionException as e:
        raise Exception(f"Network issue: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching followees: {str(e)}")

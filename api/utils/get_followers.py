import json, instaloader, re
from django.conf import settings

def get_followers(username: str, url: str):
    """
    Fetches the followees of a target username.
    """
    session_dir = settings.BASE_DIR / "sessions"
    session_file = session_dir / f"instagram_cookies_{username}.json"
    try:
        with open(session_file, 'r') as file:
            cookies = {cookie["name"]: cookie["value"] for cookie in json.load(file)}

        loader = instaloader.Instaloader()
        loader.load_session(username=username, session_data=cookies)
        
        match = re.match(r"https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.-]+)",url)
        target_username = match.group(1)
        
        print("Target Username -->", target_username)
        profile = instaloader.Profile.from_username(loader.context, target_username)
        
        print("Profile of that user --->", profile)
        followees = [
            {"username": f.username, "full_name": f.full_name, "profile_pic_url": f.profile_pic_url}
            for f in profile.get_followers()
        ]
        return followees
    except Exception as e:
        raise Exception(f"Error fetching followees: {str(e)}")
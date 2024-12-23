from pathlib import Path
import instaloader
import json, re, shutil
from django.conf import settings
from rest_framework.exceptions import APIException
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

def download_instagram_stories(request: HttpRequest ,username: str, url: str):
    """
    Downloads Instagram stories for a target user and returns metadata about the downloaded files.
    """
    try:
        loader = load_instaloader_session(username)
        match = re.search(r"stories/[^/]+/(\d+)", url)
        link = match.group()
        target_username = link.split("/")[1]
        story_id = link.split("/")[2]
        profile = instaloader.Profile.from_username(loader.context, target_username)
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'stories' / target_username
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        stories = loader.get_stories(userids=[profile.userid])
        renamed_file = None
        for story in stories:
            for item in story.get_items():
                if story_id == str(item.mediaid):
                    loader.download_storyitem(item, target=target_dir)
                    file_extension = "mp4" if item.is_video else "jpg"
                    file_pattern = f"*UTC.{file_extension}"
                    matching_files = list(target_dir.glob(file_pattern))
                    if matching_files:
                        file_path = matching_files[-1]
                        print("File found:", file_path)
                        media_url = request.build_absolute_uri(f'/media/downloads/stories/{target_username}/{file_path.name}')
                        renamed_file = media_url
                        story_metadata = {
                            "media_url": renamed_file
                        }
                        return story_metadata
    except Exception as e:
        raise APIException(f"An error occurred while downloading stories: {str(e)}")
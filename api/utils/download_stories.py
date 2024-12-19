from pathlib import Path
import instaloader
import json, re
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

def download_instagram_stories(username: str, url: str):
    """
    Downloads Instagram stories for a target user and returns metadata about the downloaded files.
    """
    try:
        # Initialize Instaloader with session
        loader = load_instaloader_session(username)

        # Fetch the profile of the target user
        match = re.search(r"stories/[^/]+/(\d+)", url)
        link = match.group()
        # print("Matching file -->", link)
        target_username = link.split("/")[1]
        story_id = link.split("/")[2]
        # print("Story Id -->", story_id)
        profile = instaloader.Profile.from_username(loader.context, target_username)
        # Directory for downloads
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'stories'
        target_dir.mkdir(parents=True, exist_ok=True)

        # Download the target user's stories
        stories = loader.get_stories(userids=[profile.userid])
        story_metadata = []

        for story in stories:
            print("Story -->", story)
            for item in story.get_items():
                if story_id == str(item.mediaid):
                    # Download the story item
                    print("media Id ==>", item.mediaid)
                    loader.download_storyitem(item, target=target_dir)
                    # Search for the file with matching media name
                    file_extension = "mp4" if item.is_video else "jpg"
                    file_pattern = f"*UTC.{file_extension}"  # Files like 2024-12-16_15-55-08_UTC.mp4
                    matching_files = list(target_dir.glob(file_pattern))
                    if matching_files:
                        file_path = matching_files[-1]  # Assuming the most recent match
                        print("File found:", file_path)
                        # Add file metadata
                        story_metadata = [{
                            # "username": target_username,
                            # "story_url": item.url,
                            # "media_type": "video" if item.is_video else "image",
                            "media_url": str(file_path)
                            # "timestamp": item.date,
                        }]
                        return story_metadata
    except Exception as e:
        raise APIException(f"An error occurred while downloading stories: {str(e)}")
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

        # Extract highlight ID from the link
        match = re.search(r"story_media_id=(\d+)_(\d+)", url)
        if not match:
            raise ValueError("Invalid link format. Unable to extract highlight ID.")
        
        highlight_id = match.group(1)
        print(f"Extracted highlight ID: {highlight_id} (type: {type(highlight_id)})")
        user_id = match.group(2)
        print(f"Extracted User ID: {user_id} (type: {type(user_id)})")
        
        # Load profile
        profile = instaloader.Profile.from_id(loader.context, int(user_id))
        print(f"Profile data --> Username: {profile.username}, ID: {profile.userid}")
        
        # Fetch highlights
        highlights = loader.get_highlights(profile.userid)
        target_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'highlights'

        highlight_metadata = []
        print("Iterating through highlights...")

        for highlight in highlights:
            print(f"Highlight Title: {highlight.title}, ID: highlight.mediaid")
            
            # Debug highlight items
            try:
                items = list(highlight.get_items())
                print(f"Total items in highlight '{highlight.title}': {len(items)}")
                
                for item in items:
                    print(f"Processing Item ID: {item.mediaid} (Type: {type(item.mediaid)})")
                    
                    if str(highlight_id) == str(item.mediaid):
                        print("Match found. Downloading item...")
                        loader.download_storyitem(item, target_dir)
                        
                        file_extension = "mp4" if item.is_video else "jpg"
                        file_pattern = f"*UTC.{file_extension}"
                        matching_files = list(target_dir.glob(file_pattern))
                        
                        if matching_files:
                            file_path = matching_files[-1]
                            print(f"File downloaded: {file_path}")
                            highlight_metadata.append({
                                "media_url": str(file_path)
                            })
                        
                        return highlight_metadata  # Return after successful download
                
            except Exception as item_error:
                print(f"Error processing highlight items: {item_error}")
        
        print("No matching highlight found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        raise APIException(f"An error occurred: {e}")
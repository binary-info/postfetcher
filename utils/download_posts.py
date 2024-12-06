import requests
import instaloader
from config.settings import settings
import json
from models.schemas import LoginRequest

def load_instaloader_session(username):
    """
    Loads an Instaloader session from a saved cookie file.
    
    Args:
        username (str): Instagram username.

    Returns:
        instaloader.Instaloader: Instaloader instance with session loaded.
    """
    try:
        loader = instaloader.Instaloader()
        
        # Load session cookies from a JSON file
        with open(f"{settings.SESSION_DIR}/instagram_cookies_{username}.json", "r") as file:
            cookies = {cookie["name"]: cookie["value"] for cookie in json.load(file)}
        
        if cookies:
            loader.load_session(username=username, session_data=cookies)
            print(f"Session loaded successfully for {username}.")
            return loader
        else:
            raise FileNotFoundError("Session cookies are empty.")
    except FileNotFoundError:
        print("Session file not found. Please ensure you have logged in and saved cookies.")
        raise
    except Exception as e:
        print(f"Error loading session: {e}")
        raise

def download_instagram_post(username: str, post_url: str):
    """
    Downloads a single Instagram post using Instaloader.
    
    Args:
        post_url (str): The URL of the Instagram post to download.
        target_dir (str): The directory where the post will be saved.
    """
    try:
        # Initialize Instaloader
        loader = load_instaloader_session(username)

        post_shortcode = post_url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
        target_dir = settings.DOWNLOAD_DIR
        loader.download_post(post, target=target_dir)
        print(f"Post from {post_url} downloaded successfully.")
        post_details = [{
            "username": post.owner_username,
            "post_url": post_url,
            "shortcode": post.shortcode,
            "caption": post.caption or "No caption",
            "likes": post.likes,
            "comments": post.comments,
            "media_url": post.url
        }]
        return post_details
    except FileNotFoundError:
        print(f"Session for {username} not found. Please log in first.")
        raise
    
    except Exception as e:
        print(f"An error occurred while downloading the post: {e}")
        raise
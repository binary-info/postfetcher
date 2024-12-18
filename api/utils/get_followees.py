import json, instaloader, re
from django.conf import settings

# def is_genuine_profile(profile):
#     """
#     Determines whether a profile is likely genuine or a bot based on heuristic checks.
#     """
#     # Check for suspicious patterns
#     low_follower_ratio = profile.followers < 0.1 * profile.followees  # Fewer followers compared to followees
#     high_follower_ratio = profile.followees < 0.1 * profile.followers  # Follows very few compared to followers
#     no_posts = profile.mediacount == 0  # No posts
#     no_profile_pic = not profile.profile_pic_url  # No profile picture
#     suspicious_username = re.match(r".*\d{4,}.*", profile.username)  # Contains 4+ consecutive digits
    
#     # Heuristic: Accounts meeting 2 or more of these criteria are likely bots
#     bot_score = sum([low_follower_ratio, high_follower_ratio, no_posts, no_profile_pic, suspicious_username is not None])
#     return bot_score < 2  # Return True if the profile is likely genuine

def get_followees(username: str, url: str):
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
            for f in profile.get_followees()
        ]
        return followees
    except Exception as e:
        raise Exception(f"Error fetching followees: {str(e)}")
    
        # checking of profile that we have has genuine followers or not
    #     print(f"Analyzing followers of {target_username}...")
    #     followers_analysis = []
    #     followers = profile.get_followers()
    #     for follower in followers:
    #         genuine = is_genuine_profile(follower)
    #         followers_analysis.append({
    #             "username": follower.username,
    #             "is_genuine": genuine
    #             # "profile_pic":f
    #         })

    #     # Analyze following
    #     print(f"Analyzing following of {username}...")
    #     following_analysis = []
    #     for following in profile.get_followees():
    #         genuine = is_genuine_profile(following)
    #         following_analysis.append({
    #             "username": following.username,
    #             "is_genuine": genuine
    #         })

    #     # Return results
    #     return {
    #         "followers": followers_analysis,
    #         "following": following_analysis
    #     }

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return {"error":e}
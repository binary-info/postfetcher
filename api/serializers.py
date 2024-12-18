from rest_framework import serializers

class LoginRequestSerializer(serializers.Serializer):
    """
    Serializer for Instagram Login response.
    """
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class FolloweesResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Followings response.
    """
    username = serializers.CharField(max_length=100)
    full_name = serializers.CharField(max_length=100)
    profile_pic_url = serializers.URLField()
    
class FollowersResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Followers response.
    """
    username = serializers.CharField(max_length=100)
    full_name = serializers.CharField(max_length=100)
    profile_pic_url = serializers.URLField()

class ProfileResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Profile Picture download response.
    """
    # username = serializers.CharField(max_length=100)
    # full_name = serializers.CharField(max_length=100)
    media_url = serializers.URLField()
    # biography = serializers.CharField()

class PostDownloadResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Post download response.
    """
    # username = serializers.CharField(max_length=100)
    # post_url = serializers.URLField()
    # shortcode = serializers.CharField()
    # caption = serializers.CharField()
    media_url = serializers.URLField()
    # likes = serializers.IntegerField()
    # comments = serializers.IntegerField()
    
class ReelDownloadResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Reel download response.
    """
    # username = serializers.CharField(max_length=100)
    # reel_url = serializers.URLField()
    # shortcode = serializers.CharField()
    # caption = serializers.CharField()
    media_url = serializers.URLField()
    
class StoryDownloadResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram story download response.
    """
    # username = serializers.CharField(max_length=120)
    # story_url = serializers.URLField()
    # media_type = serializers.ChoiceField(choices=["image", "video"])
    media_url = serializers.CharField(max_length=1024)
    # timestamp = serializers.DateTimeField()
    
class HighlightsDownloadResponseSerializer(serializers.Serializer):
    """
    Serializer for Instagram Highlights download response.
    """
    # username = serializers.CharField(max_length=120)
    # highlight_url = serializers.URLField()
    # media_type = serializers.ChoiceField(choices=["image", "video"])
    media_url = serializers.CharField(max_length=1024)
    # timestamp = serializers.DateTimeField()
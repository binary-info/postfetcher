from api.serializers import *
from api.utils.login import login_data
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.get_followees import get_followees
from api.utils.get_followers import get_followers
from rest_framework.exceptions import APIException
from api.utils.profile_data import fetch_instagram_profile
from api.utils.download_highlights import download_highlight
from api.utils.download_posts import download_instagram_post
from api.utils.download_reels import download_instagram_reel
from api.utils.download_stories import download_instagram_stories

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            result = login_data(username=username, password=password)
            return Response({"message": "Login successful", "data": result})
        except Exception as e:
            raise APIException(str(e))

class ProfileView(APIView):
    def get(self, request):
        """
        Asynchronous view for fetching Instagram profile info.
        """
        username = request.query_params.get('username')
        url = request.query_params.get('url')

        if not username or not url:
            raise APIException("Both 'username' and 'url' are required.")

        try:
            # Properly await the asynchronous function
            profile_info = fetch_instagram_profile(username, url)

            # Return the response as a valid DRF Response object
            return Response(profile_info)  # This ensures the response is properly formatted
        except Exception as e:
            raise APIException(str(e))
        
class PostDownloadView(APIView):
    def get(self, request):
        username = request.query_params.get('username')
        url = request.query_params.get('url')
        try:
            post_details = download_instagram_post(username=username, post_url=url)
            return Response(post_details)
        except APIException as api_exception:
            return Response({"error": str(api_exception)}, status=400)
        except Exception as e:
            raise APIException(f"An unexpected error occurred: {str(e)}")

class ReelDownloadView(APIView):
    """
    API view to download Instagram reels of a target user.
    """
    def get(self, request):
        username = request.query_params.get('username')
        url = request.query_params.get('url')
        try:
            reel_detail = download_instagram_reel(username=username, reel_url=url)
            serializer = ReelDownloadResponseSerializer(reel_detail, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise APIException(str(e))
        
class StoryDownloadView(APIView):
    """
    API view to download Instagram stories of a target user.
    """
    def get(self, request):
        username = request.query_params.get('username')
        url = request.query_params.get('url')
        try:
            # Call the story downloading function
            story_detail = download_instagram_stories(username=username, url=url)
            return Response(story_detail)
            # Serialize the response
            # serializer = StoryDownloadResponseSerializer(data=story_detail, many=True)
            # if serializer.is_valid():
            #     return Response(serializer.data)
            # else:
            #     return Response(serializer.errors, status=400)
        except APIException as api_exception:
            return Response({"error": str(api_exception)}, status=400)
        except Exception as e:
            raise APIException(f"An unexpected error occurred: {str(e)}")

class HighlightDownloadView(APIView):
    """
    API view to download Instagram highlights of a target user.
    """
    def get(self, request):
        username = request.query_params.get('username')
        url = request.query_params.get('url')
        try:
            # Call the story downloading function
            highlight_detail = download_highlight(username=username, url=url)
            return Response(highlight_detail)
            # Serialize the response
            # serializer = HighlightsDownloadResponseSerializer(data=story_detail, many=True)
            # if serializer.is_valid():
            #     return Response(serializer.data)
            # else:
            #     return Response(serializer.errors, status=400)
        except APIException as api_exception:
            return Response({"error": str(api_exception)}, status=400)
        except Exception as e:
            raise APIException(f"An unexpected error occurred: {str(e)}")

class FolloweingsView(APIView):
    def get(self, request):
        try:
            username = request.query_params.get('username')
            url = request.query_params.get('url')
            followings = get_followees(username, url)
            return followings
            # serializer = FolloweesResponseSerializer(followees, many=True)
            # return Response(serializer.data)
        except Exception as e:
            raise APIException(str(e))
        
class FollowersView(APIView):
    def get(self, request):
        try:
            username = request.query_params.get('username')
            url = request.query_params.get('url')
            followers = get_followers(username, url)
            serializer = FollowersResponseSerializer(data=followers, many=True)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except APIException as api_exception:
            return Response({"error": str(api_exception)}, status=400)
        except Exception as e:
            raise APIException(f"An unexpected error occurred: {str(e)}")    
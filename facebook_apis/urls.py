from django.urls import path, include
from facebook_apis.views import *

urlpatterns = [
    path('auth/login', FacebookLoginAPIView.as_view(), name='login'),
    # path('profile', ProfileView.as_view(), name='profile'),
    path('download-post', FacebookPostDownloaderAPIView.as_view(), name='download_posts'),
    # path('download-reel', ReelDownloadView.as_view(), name='download_reels'),
    # path('download-story', StoryDownloadView.as_view(), name='download_story'),
    # path('download-highlight', HighlightDownloadView.as_view(), name='download_highlights'),
    # path('followings', FolloweingsView.as_view(), name='followees'),
    # path('followeers', FollowersView.as_view(), name='followeers'),
]
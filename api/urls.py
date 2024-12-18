from django.urls import path
from api.views import *

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('download-post', PostDownloadView.as_view(), name='download_posts'),
    path('download-reel', ReelDownloadView.as_view(), name='download_reels'),
    path('download-story', StoryDownloadView.as_view(), name='download_story'),
    path('download-highlight', HighlightDownloadView.as_view(), name='download_highlights'),
    path('followings', FolloweingsView.as_view(), name='followees'),
    path('followeers', FollowersView.as_view(), name='followeers'),
]
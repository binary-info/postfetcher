from django.urls import path, include
from api.views import *

urlpatterns = [
    path('facebook/', include('facebook_apis.urls')),
    path('auth/login', LoginView.as_view(), name='login'),
    path('download', InstaDownload.as_view(), name='downloads')
    # path('profile', InstaDownload.ProfileView.as_view(), name='profile'),
    # path('download-post', InstaDownload.PostDownloadView.as_view(), name='download_posts'),
    # path('download-reel', InstaDownload.ReelDownloadView.as_view(), name='download_reels'),
    # path('download-story', InstaDownload.StoryDownloadView.as_view(), name='download_story'),
    # path('download-highlight', InstaDownload.HighlightDownloadView.as_view(), name='download_highlights'),
    # path('followings', InstaDownload.FolloweingsView.as_view(), name='followees'),
    # path('followeers', InstaDownload.FollowersView.as_view(), name='followeers'),
]
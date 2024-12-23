from django.urls import path, include
from .views import *

urlpatterns = [
    path('', instagram_downloader_view, name='instagram_downloader')
]
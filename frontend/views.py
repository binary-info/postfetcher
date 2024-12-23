from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def instagram_downloader_view(request):
    return render(request, 'instagram_facebook_downloader.html')
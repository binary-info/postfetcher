from fastapi import APIRouter, HTTPException
from utils.download_posts import download_instagram_post
from models.schemas import PostDownloadResponse

router = APIRouter()

@router.get("", response_model=list[PostDownloadResponse])
def download_post(username: str, url: str):
    try:
        post_details = download_instagram_post(username=username,post_url=url)
        return post_details
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

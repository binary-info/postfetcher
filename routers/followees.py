from fastapi import APIRouter, HTTPException
from utils.get_followees import get_followees
from models.schemas import FolloweesResponse

router = APIRouter()
print("---- into following----")
@router.get("/followees/{username}/{target_username}", response_model=list[FolloweesResponse])
async def fetch_followees(username: str, target_username: str):
    try:
        followees = await get_followees(username, target_username)
        return followees
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

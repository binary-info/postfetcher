from fastapi import APIRouter, HTTPException
from utils.apiRequest import make_authenticated_request
from models.schemas import ProfileResponse

router = APIRouter()
print("---- into profile----")

@router.get("/profile/{username}/{target_username}", response_model=ProfileResponse)
async def fetch_profile(username: str, target_username: str):
    try:
        profile_info = await make_authenticated_request(username, target_username)
        return profile_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

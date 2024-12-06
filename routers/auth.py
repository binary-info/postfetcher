from fastapi import APIRouter, HTTPException, Request
from utils.loginData import login_data
from models.schemas import LoginRequest

router = APIRouter()
print("--- Into Auth ---------------- ")
@router.post("/login")
async def login(username: str, password: str):
    print("-------------- into login ------------------")
    try:
        username = username
        password = password
        print("Testing Playwright functionality...")
        # page_title = await test_playwright()
        # print(f"Playwright test passed. Page title: {page_title}")
        print("----- username -----", username, "---- Password -------", password)
        print(f"Login attempt for username: {username}")
        result = await login_data(username=username, password=password)
        return {"message": "Login successful", "data": result}
    except HTTPException as he:
        print(f"HTTPException during login: {he.detail}")
        raise
    except Exception as e:
        print(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")

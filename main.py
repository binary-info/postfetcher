import uvicorn
from fastapi import FastAPI
from routers import auth, followees, profile, postDownload
from fastapi.responses import RedirectResponse

app = FastAPI(title="Facebook - Instagram Tool API")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(followees.router, prefix="/followees", tags=["Followees"])
app.include_router(profile.router, prefix="/profile", tags=["Profile Info"])
app.include_router(postDownload.router, prefix="/download-posts", tags=["Download Posts"])
print("after--------")

@app.get("/")
async def root():
    # Include routers
    print("--- Welcome To app --")
    return RedirectResponse("docs")

if __name__=="__main__":
    print(" --- Welcome to App ---")
    uvicorn.run(app, host="13.60.92.165", port=8501)

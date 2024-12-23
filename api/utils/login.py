import json, instaloader
from playwright.sync_api import sync_playwright
from django.conf import settings
# from api.models import UserSession

def login_data(username, password):
    """
    Logs in to Instagram using Playwright and saves session cookies.
    """
    session_dir = settings.BASE_DIR / "sessions"
    session_file = session_dir / f"instagram_cookies_{username}.json"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("Navigating to Instagram login page...")
            page.goto("https://www.instagram.com/accounts/login/")
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")

            print("Waiting for redirection...")
            page.wait_for_timeout(20000)

            if "login" in page.url:
                raise Exception("Login failed, incorrect credentials or blocked.")

            print("Saving cookies...")
            cookies = context.cookies()
            with open(session_file, "w") as file:
                json.dump(cookies, file)
            
            # user_agent = page.evaluate("navigator.userAgent")

            # save_data = UserSession(username=username,cookies=cookies,user_agent=user_agent)
            # save_data.save()
            browser.close()
            return {"status": "success", "message": "Login successfull."}
    except Exception as e:
        print(f"Login process failed: {str(e)}")
        raise
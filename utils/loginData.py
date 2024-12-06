# from playwright.sync_api import sync_playwright
# import json
# import os, sys, asyncio
# from config.settings import settings

# # def install_playwright_browsers():
# #     """Install Playwright browsers via API."""
# #     with sync_playwright() as p:
# #         print("Playwright is ready. Browsers will be installed automatically.")

# # if sys.platform == "win32":
# #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
# def login_data(username, password):
#     with sync_playwright() as p:
#         print("------ In sync func of login -------")
#         browser = p.chromium.launch(headless=False, slow_mo=100)
#         context = browser.new_context()
#         page = context.new_page()

#         page.goto("https://www.instagram.com/accounts/login/")
#         page.wait_for_load_state("networkidle")

#         page.fill("input[name='username']", username)
#         page.fill("input[name='password']", password)
#         page.click("button[type='submit']")
#         page.wait_for_timeout(15000)  # Wait for login redirection
#         try:
#             page.click("button:has-text('Not Now')")
#         except:
#             pass
        
#         try:
#             cookies = context.cookies()
#             user_agent = page.evaluate("navigator.userAgent")
#             with open(f"{settings.SESSION_DIR}/instagram_cookies_{username}.json", "w") as file:
#                 json.dump(cookies, file)
#         except Exception as e:
#             print("--error--", e)
        
#         session_file = os.path.join(settings.SESSION_DIR, f"session-{username}.txt")
#         with open(session_file, "w") as file:
#             for cookie in cookies:
#                 file.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\tFALSE\t{cookie['expires']}\t{cookie['name']}\t{cookie['value']}\n")

#         browser.close()
#         print(f"Login successful. Session saved at.")
# from playwright.sync_api import sync_playwright
# import json
# import os
# from config.settings import settings

# def login_data(username, password):
#     with sync_playwright() as p:
#         try:
#             print("------ Starting Playwright login -------")
#             browser = p.chromium.launch(headless=False, slow_mo=50)
#             context = browser.new_context(
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#             )
#             page = context.new_page()

#             # Navigate to Instagram login page
#             page.goto("https://www.instagram.com/accounts/login/")
#             page.wait_for_selector("input[name='username']", timeout=30000)

#             # Fill in login credentials
#             page.fill("input[name='username']", username)
#             page.fill("input[name='password']", password)
#             page.click("button[type='submit']")

#             # Wait for successful login
#             page.wait_for_selector("button:has-text('Not Now')", timeout=30000)
#             try:
#                 page.click("button:has-text('Not Now')")
#             except:
#                 print("No 'Not Now' button to dismiss.")

#             # Save session cookies
#             cookies = context.cookies()
#             user_agent = page.evaluate("navigator.userAgent")

#             if not os.path.exists(settings.SESSION_DIR):
#                 os.makedirs(settings.SESSION_DIR)

#             cookie_file = os.path.join(settings.SESSION_DIR, f"instagram_cookies_{username}.json")
#             with open(cookie_file, "w") as file:
#                 json.dump({"cookies": cookies, "user_agent": user_agent}, file)
#                 print(f"Cookies saved to {cookie_file}")

#             # Save session for future use
#             session_file = os.path.join(settings.SESSION_DIR, f"session-{username}.txt")
#             with open(session_file, "w") as file:
#                 for cookie in cookies:
#                     file.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\tFALSE\t{cookie['expires']}\t{cookie['name']}\t{cookie['value']}\n")
#                 print(f"Session saved to {session_file}")

#             browser.close()
#             return {"status": "success", "message": "Login successful"}
#         except Exception as e:
#             print("-- Error during login --", e)
#             raise e

# ------------------------ Last updated code ------------------------

from fastapi import HTTPException
from playwright.async_api import async_playwright
import json
import os
from config.settings import settings

async def login_data(username, password):
    try:
        async with async_playwright() as p:
            print("Initializing browser...", username)
            browser = await p.chromium.launch(headless=True,args=['--no-sandbox', '--disable-setuid-sandbox'])
            context = await browser.new_context()
            page = await context.new_page()

            print("Navigating to Instagram login page...")
            await page.goto("https://www.instagram.com/accounts/login/")
            await page.wait_for_selector("input[name='username']")

            print("Filling login details...")
            await page.fill("input[name='username']", username)
            await page.fill("input[name='password']", password)
            await page.click("button[type='submit']")

            print("Waiting for redirection...")
            await page.wait_for_timeout(15000)

            # Additional checks
            if page.url == "https://www.instagram.com/accounts/login/":
                raise Exception("Login failed, incorrect credentials or blocked.")

            print("Saving cookies...")
            cookies = await context.cookies()
            user_agent = await page.evaluate("navigator.userAgent")
            with open(f"{settings.SESSION_DIR}/instagram_cookies_{username}.json", "w") as file:
                json.dump(cookies, file)
            session_file = os.path.join(settings.SESSION_DIR, f"session-{username}.txt")
            with open(session_file, "w") as file:
                for cookie in cookies:
                    file.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\tFALSE\t{cookie['expires']}\t{cookie['name']}\t{cookie['value']}\n")
            await browser.close()
            return {"status": "success", "cookies": cookies}

    except Exception as e:
        print(f"Login process failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Login process failed: {str(e)}")
from playwright.async_api import async_playwright

async def test_playwright():
    async with async_playwright() as p:
            print("Initializing browser...")
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            print("Navigating to Instagram login page...")
            await page.goto("https://www.instagram.com/accounts/login/")
            await page.wait_for_selector("input[name='username']")

            print("Filling login details...")
            # await page.fill("input[name='username']", username)
            # await page.fill("input[name='password']", password)
            # await page.click("button[type='submit']")

            print("Waiting for redirection...")
            await page.wait_for_timeout(15000)

            # Additional checks
            if page.url == "https://www.instagram.com/accounts/login/":
                raise Exception("Login failed, incorrect credentials or blocked.")

            print("Saving cookies...")
            cookies = await context.cookies()
            await browser.close()
            return {"status": "success", "cookies": cookies}

# import asyncio
# asyncio.run(test_playwright())
import time, requests, json
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from django.conf import settings
from rest_framework.views import APIView
from selenium.webdriver.common.by import By
from rest_framework.response import Response
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login_to_facebook(email, password):
    """
    Log in to Facebook using Selenium and store session data.

    Args:
        email (str): The Facebook email address.
        password (str): The Facebook password.

    Returns:
        None: The driver is not returned directly. Session data is stored.
    """
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in PATH
    driver.get('https://www.facebook.com')

    try:
        time.sleep(5)
        email_elem = driver.find_element(By.ID, "email")
        password_elem = driver.find_element(By.ID, "pass")

        email_elem.send_keys(email)
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)

        # Wait for login to complete (adjust as needed)
        time.sleep(10)
        driver_data = driver
        driver.quit() 
        return driver_data
    
    except Exception as e:
        driver.quit()
        raise Exception(f"Failed to log in: {str(e)}")

class FacebookLoginAPIView(APIView):

    def post(self, request):
        """Handle the POST request for logging in."""
        fb_email = request.data.get('email')
        print("Email address from Json -->", fb_email)
        fb_password = request.data.get('password')
        print("Password from Json -->", fb_password)
        try:
            # Log in to Facebook
            driver = login_to_facebook(fb_email, fb_password)
            cookie = driver.get_cookies()
            print("Cookies from browser --->", cookie)
            print("Driver in login Proxy URL func -->", driver)
            print("Driver in login URL func -->", driver.command_executor.browser_name)
            # Save driver in session
            session_data = {
                "webdriver" : driver.session_id,
                "webdriver_url" : driver.command_executor.browser_name
            }
            request.session['webdrive_session'] = session_data
            driver.quit()
            return Response({'message': 'Login successful. You can now download posts.'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

def get_driver_from_session(request):
    """Retrieve the Selenium WebDriver instance from the session."""
    session = request.session.get('webdrive_session')
    print("Session data 123 ----->", session)
    if not session:
        raise Exception("No WebDriver session found in the request.")

    session_id = session.get('webdriver')
    print("Session Id from session --->", session_id)
    command_executor_url = session.get('webdriver_url')
    print("Command Executor URL from Session -->", command_executor_url)

    if not session_id or not command_executor_url:
        raise Exception("No active WebDriver session details available. Please log in first.")

    try:
        # Initialize the WebDriver with command_executor
        options = Options()
        print("POSTS FROM CLASS ---->", options)
        driver = WebDriver(command_executor=command_executor_url, options=options)

        # Reassign the existing session ID
        driver.session_id = session_id

        # Test if the session is still alive
        _ = driver.title  # This will raise an exception if the session is invalid

        print("Successfully reconnected to WebDriver session.")
        return driver

    except Exception as e:
        print(f"Failed to reconnect to WebDriver session: {str(e)}")
        raise Exception("WebDriver session is no longer active or accessible.")

def download_post(driver, post_url):
    """Navigate to the Facebook post and download its media."""
    try:
        driver.get(post_url)

        # Wait for the post to load
        time.sleep(15)

        # Extract media URLs
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        media_urls = []

        # Look for images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                media_urls.append(src)

        # Look for videos
        for video in soup.find_all('video'):
            src = video.get('src')
            if src:
                media_urls.append(src)

        # Download the media
        download_links = []
        for index, url in enumerate(media_urls):
            response = requests.get(url)
            file_name = f'media_{index}.jpg'  # Change to .mp4 if it's a video
            file_path = Path(settings.MEDIA_ROOT) / 'downloads' / 'facebook' / file_name

            # Ensure the directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'wb') as file:
                file.write(response.content)

            # Add to response links
            download_links.append(str(file_path))

        return {
            'media_urls': media_urls,
            'download_links': download_links
        }

    except Exception as e:
        raise Exception(f"Failed to download post: {str(e)}")

class FacebookPostDownloaderAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """Handle the GET request to download a Facebook post."""
        post_url = request.query_params.get('post_url')
        print("URL THAT I PASTE --->", post_url)
        if not post_url:
            return Response({'error': 'Post URL is required.'}, status=400)

        try:
            # Retrieve driver from session
            driver = get_driver_from_session(request)
            print("Driver --->", driver)

            # Download the post
            result = download_post(driver, post_url)

            return Response({
                'message': 'Media downloaded successfully.',
                'media_urls': result['media_urls'],
                'download_links': result['download_links']
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

def connect_to_url_with_selenium(target_url):
    
    result = None
    
    # Setup Chrome options with anti-detection measures
    options = Options()
    
    # Option 1: Run in windowed mode (more like a real user)
    # Comment this out if you need truly headless operation
    # Nothing here - browser will open with UI
    
    # Option 2: Run headless but with anti-detection measures
    options.add_argument("--headless=new")  # New headless mode in Chrome
    
    # Common anti-detection measures
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Set a realistic window size
    options.add_argument("--window-size=1920,1080")
    
    # Use a common user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    
    # Disable automation flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Additional stealth settings
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        # Create a new instance of Chrome driver
        driver = webdriver.Chrome(options=options)
        
        # Execute CDP commands to modify navigator properties
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Overwrite the plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                // Overwrite the languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'es']
                });
            """
        })
        
        # Navigate to the URL
        driver.get(target_url)
        
        # Add a random delay to simulate human behavior (1-3 seconds)
        time.sleep(1 + random.random() * 2)
        
        
        # Set our result 
        result = driver.page_source
        
                
        # Properly close the driver
        driver.quit()

        return result
    
    
    except Exception as e:
        print(f"Error: {e}")
        # Make sure to quit even if there's an exception
        try:
            if 'driver' in locals():
                driver.quit()
        except:
            pass
        return None
    
    
    
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import json
from typing import Dict, List, Any

class AsyncSeleniumWrapper:
    """
    A wrapper class that enables asynchronous use of Selenium WebDriver.
    """
    
    def __init__(self, headless=True, user_agent=None):
        """
        Initialize the AsyncSeleniumWrapper with options.
        
        Args:
            headless: Whether to run Chrome in headless mode
            user_agent: Custom user agent string to use
        """
        self.options = Options()
        
        if headless:
            self.options.add_argument("--headless=new")
        
        # Common settings to improve reliability
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        
        # Set user agent if provided
        if user_agent:
            self.options.add_argument(f"--user-agent={user_agent}")
        
        # Anti-detection settings
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        
        # The driver instance will be set when connect is called
        self.driver = None
    
    async def connect(self):
        """
        Connect to a new Chrome instance asynchronously.
        
        Returns:
            The WebDriver instance
        """
        # Create the driver in a separate thread to avoid blocking the main thread
        loop = asyncio.get_event_loop()
        self.driver = await loop.run_in_executor(
            None, 
            lambda: webdriver.Chrome(options=self.options)
        )
        
        # Apply anti-detection measures
        await loop.run_in_executor(
            None,
            lambda: self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument", 
                {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                }
            )
        )
        
        return self.driver
    
    async def disconnect(self):
        """
        Properly close the WebDriver connection.
        """
        if self.driver:
            await asyncio.get_event_loop().run_in_executor(None, self.driver.quit)
            self.driver = None
    
    async def get_page(self, url):
        """
        Navigate to the specified URL.
        
        Args:
            url: The URL to navigate to
            
        Returns:
            The page_source
        """
        if not self.driver:
            await self.connect()
        
        await asyncio.get_event_loop().run_in_executor(None, self.driver.get, url)
        return self.driver.page_source
    
    async def get_server_response_headers(self, url):
        """
        Get the response headers from the server for the specified URL.
        
        Args:
            url: The URL to connect to
            
        Returns:
            Dictionary of response headers
        """
        if not self.driver:
            await self.connect()
        
        # Enable Network monitoring
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.driver.execute_cdp_cmd('Network.enable', {})
        )
        
        # Set up a container for the response headers
        response_headers = {}
        
        # Navigate to the URL
        page_title = await self.get_page(url)
        
        # Get response headers using CDP
        responses = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.driver.execute_cdp_cmd('Network.getAllCookies', {})
        )
        
        # We would normally get headers here, but this is just a placeholder
        # In a real implementation, you'd need to intercept the actual response
        # which is more complex with CDP
        
        # Disable Network monitoring
        await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.driver.execute_cdp_cmd('Network.disable', {})
        )
        
        return {"title": page_title, "cookies": responses.get("cookies", [])}
    
    async def execute_async_script(self, script, *args):
        """
        Execute asynchronous JavaScript in the browser.
        
        Args:
            script: The JavaScript to execute
            *args: Arguments to pass to the script
            
        Returns:
            The result of the script execution
        """
        if not self.driver:
            await self.connect()
        
        # Execute the script in a separate thread
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: self.driver.execute_async_script(script, *args)
        )
        
        return result
    
    
    
async def async_connect_to_url_with_selenium(url,headless = True):
    async_selenium = AsyncSeleniumWrapper(headless=headless)
    await async_selenium.connect()
    return await async_selenium.get_page(url)

async def main():
    # Example usage
    async_selenium = AsyncSeleniumWrapper(headless=True)
    
    try:
        # Connect and navigate to a URL
        await async_selenium.connect()
        url = "https://www.monergism.com/topics"
        
        print(f"Connecting to {url}...")
        title = await async_selenium.get_page(url)
        print(f"Page title: {title}")
        
        # Get response headers
        response_data = await async_selenium.get_server_response_headers(url)
        print("\nResponse data:")
        print(json.dumps(response_data, indent=2))
        
        # Execute some JavaScript
        script_result = await async_selenium.execute_async_script(
            "arguments[0](document.title);", 
            # The first argument is the callback function
        )
        print(f"\nScript result: {script_result}")
        
    finally:
        # Always disconnect properly
        await async_selenium.disconnect()


if __name__ == "__main__":
    result = connect_to_url_with_selenium("https://www.monergism.com/topics")
    print(result)
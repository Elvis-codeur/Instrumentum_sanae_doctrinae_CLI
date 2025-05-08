from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import random

def get_server_response_headers(driver, url):
    """
    Uses Chrome DevTools Protocol to capture HTTP response headers from the server.
    Returns them as a dictionary.
    """
    # Enable Network domain to capture responses
    driver.execute_cdp_cmd('Network.enable', {})
    
    # Set up a container for the response headers
    response_headers = {}
    response_received = False
    
    def response_received_handler(response_data):
        nonlocal response_headers, response_received
        if response_data['response']['url'] == url:
            response_headers = response_data['response']['headers']
            response_received = True
    
    # Add event listener for response events
    driver.add_cdp_listener('Network.responseReceived', response_received_handler)
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the response to be received
    wait_time = 0
    while not response_received and wait_time < 10:
        time.sleep(0.5)
        wait_time += 0.5
    
    # Disable network monitoring
    driver.execute_cdp_cmd('Network.disable', {})
    
    return response_headers

def connect_to_url_and_get_server_headers(target_url):
    """
    Connect to a URL using Selenium and capture the server's response headers.
    """
    # Setup Chrome options with anti-detection measures
    options = Options()
    
    # Headless mode
    options.add_argument("--headless=new")
    
    # Common settings
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        # Create a new instance of Chrome driver
        driver = webdriver.Chrome(options=options)
        
        # Apply stealth settings
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        # Get server response headers
        server_headers = get_server_response_headers(driver, target_url)
        
        # Get page title for verification
        page_title = driver.title
        
        # Properly close the driver
        driver.quit()
        
        return {
            "url": target_url,
            "title": page_title,
            "server_headers": server_headers,
            "success": True
        }
    except Exception as e:
        print(f"Error: {e}")
        # Make sure to quit the driver even if there's an exception
        try:
            if 'driver' in locals():
                driver.quit()
        except:
            pass
        return {
            "url": target_url,
            "server_headers": None,
            "success": False,
            "error": str(e)
        }

def format_headers_dict(headers_dict):
    """
    Pretty print the headers dictionary in a readable format
    """
    formatted = ""
    for key, value in headers_dict.items():
        formatted += f"{key}: {value}\n"
    return formatted

def save_headers_to_file(result, filename="server_headers.json"):
    """
    Save the captured headers to a JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Server headers saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving headers: {e}")
        return False
        
def test_for_headless_detection(server_headers):
    """
    Analyze server headers for potential signs of headless browser detection
    """
    detection_signs = []
    
    # Check for common security headers that might vary for headless browsers
    if 'X-Frame-Options' in server_headers:
        print(f"Server uses X-Frame-Options: {server_headers['X-Frame-Options']}")
    
    # Check for server-side bot detection hints
    bot_related_headers = [h for h in server_headers.keys() if 'bot' in h.lower() or 'security' in h.lower()]
    if bot_related_headers:
        detection_signs.extend(bot_related_headers)
        
    # Check for cloud security services that might detect bots
    security_services = [
        ('cloudflare', 'CF-'),
        ('akamai', 'Akamai'),
        ('imperva', 'X-Imperva'),
        ('fastly', 'Fastly')
    ]
    
    for service, prefix in security_services:
        matches = [h for h in server_headers.keys() if prefix in h]
        if matches:
            detection_signs.append(f"Found {service} security headers: {', '.join(matches)}")
            
    return detection_signs

if __name__ == "__main__":
    url = "https://www.monergism.com/topics"
    print(f"Connecting to {url} and capturing server response headers...")
    
    result = connect_to_url_and_get_server_headers(url)
    
    if result["success"]:
        print(f"\nSuccessfully connected to {result['url']}")
        print(f"Page title: {result['title']}")
        print("\nServer response headers:")
        print("=" * 50)
        
        if result["server_headers"]:
            formatted_headers = format_headers_dict(result["server_headers"])
            print(formatted_headers)
            
            # Check for potential bot detection
            detection_signs = test_for_headless_detection(result["server_headers"])
            if detection_signs:
                print("\nPotential headless browser detection indicators:")
                for sign in detection_signs:
                    print(f"- {sign}")
            else:
                print("\nNo obvious headless browser detection indicators found in headers.")
                
            # Save headers to file
            save_headers_to_file(result)
        else:
            print("No headers were captured.")
    else:
        print(f"Failed to connect to {result['url']}")
        print(f"Error: {result.get('error', 'Unknown error')}")
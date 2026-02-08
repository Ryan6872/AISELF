import os
import time
from playwright.sync_api import sync_playwright

SWAGGER_PATH = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\swagger.json"
USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"
SCREENSHOT_PATH = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\error_screenshot.png"

def run():
    print("Starting RapidAPI Automation (Persistent Session v3)...")
    os.environ["HOME"] = r"C:\Users\Administrator"
    
    with sync_playwright() as p:
        # Launch persistent context
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        try:
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            print("Navigating to RapidAPI Dashboard...")
            page.goto("https://rapidapi.com/provider/dashboard")
            time.sleep(5)
            
            # Check login
            if "auth/login" in page.url:
                print("Login required! Please login manually.")
                page.wait_for_selector("text=Add New API", timeout=300000)
            
            print("Checking if API exists...")
            api_name = "Prometheus Text & Code Toolkit"
            # Refresh to be sure
            page.reload()
            time.sleep(3)
            
            if page.get_by_text(api_name).count() > 0:
                print(f"Found existing API: {api_name}")
                page.click(f"text={api_name}")
            else:
                print("API not found, creating new...")
                try:
                    page.click("text=Add New API", timeout=5000)
                except:
                    print("Button click failed, forcing navigation...")
                    page.goto("https://rapidapi.com/provider/new")
                
                # Helper to fill form
                page.wait_for_selector("input[name='name']", timeout=10000)
                page.fill("input[name='name']", api_name)
                page.fill("textarea[name='description']", "Ultra-fast Python AST analysis and text processing toolkit.")
                try:
                    page.click("div[class*='category']", timeout=2000)
                    page.click("text=Tools", timeout=2000)
                except:
                    pass
                page.click("button[type='submit']")
                print("API Created.")
                page.wait_for_url("**/definition/overview", timeout=15000)

            # Go to Endpoints
            print("Navigating to Endpoints...")
            time.sleep(3)
            
            # Navigate to Endpoints tab
            # We might be on Overview
            found_endpoints = False
            
            # Strategy: Click "API Specs" -> "V1" -> "Endpoints"
            # Or assume directly visible
            try:
                 print("Looking for Endpoints tab...")
                 if page.get_by_text("Endpoints").is_visible():
                     page.click("text=Endpoints")
                     found_endpoints = True
                 else:
                     # Try dropdown
                     if page.get_by_text("API Specs").is_visible():
                         page.click("text=API Specs")
                         time.sleep(1)
                         # Try searching "endpoints"
                         if page.get_by_text("Endpoints").is_visible():
                             page.click("text=Endpoints")
                             found_endpoints = True
            except:
                pass
                
            if not found_endpoints:
                print("Could not find Endpoints tab automatically.")
                print("Attemping to find 'Add Endpoint' directly...")

            time.sleep(2)
            
            # Create Endpoint
            print("Checking/Creating Endpoint...")
            if page.get_by_text("Create Endpoint").is_visible():
                print("Clicking Create Endpoint...")
                page.click("text=Create Endpoint")
                time.sleep(1)
                
                # Fill Form
                print("Filling Form...")
                # Name
                try:
                    page.locator("input").first.fill("Analyze Code")
                except:
                    pass
                    
                # Path
                try:
                     # Identify via placeholder if possible
                     page.fill("[placeholder*='/']", "/explain")
                except:
                     pass

                # Save
                try:
                    page.click("button:has-text('Save')")
                    print("Endpoint saved.")
                except:
                    print("Could not click Save.")
                    
            print("\n" + "="*50)
            print("Automation Complete! Browser will stay open.")
            print("="*50 + "\n")
            
            while True:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error detected: {e}")
            try:
                page.screenshot(path=SCREENSHOT_PATH)
                print(f"Screenshot saved to {SCREENSHOT_PATH}")
            except:
                pass
            print("Browser staying open for debugging.")
            while True:
                time.sleep(1)

if __name__ == "__main__":
    run()

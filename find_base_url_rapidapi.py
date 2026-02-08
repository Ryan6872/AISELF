import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"

def run():
    print("Starting Base URL Locator...")
    os.environ["HOME"] = r"C:\Users\Administrator"
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # 1. Dashboard
        page.goto("https://rapidapi.com/provider/dashboard")
        time.sleep(3)
        
        # 2. Click API
        try:
             page.click("text=Prometheus Text and Code Toolkit")
        except:
             pass
        time.sleep(3)
        
        # 3. Explore for Base URL
        # Strategy:
        # - Check "Hub Listing" -> "Gateway" (New UI?)
        # - Check "Definition" -> "Gateway"
        # - Check "General"
        
        print("Looking for 'Gateway' tab...")
        try:
            # Try finding a tab named Gateway
            page.click("text=Gateway")
            time.sleep(2)
            
            # Look for input with "base url" or "target"
            # Common selectors: input[name='baseUrl'], input[placeholder='https://api.example.com']
            
            inputs = page.locator("input").all()
            for i in inputs:
                placeholder = i.get_attribute("placeholder") or ""
                name = i.get_attribute("name") or ""
                value = i.input_value()
                
                print(f"Input: name='{name}', placeholder='{placeholder}', value='{value}'")
                
                if "api.example.com" in placeholder or "Base URL" in placeholder or "baseUrl" in name:
                    print(f"FOUND POTENTIAL BASE URL FIELD! Highlighting it...")
                    i.focus()
                    # i.fill("https://aiself.vercel.app/api") # Un-comment to auto-fill
                    time.sleep(1)
        except Exception as e:
            print(f"Gateway tab exploration failed: {e}")

        print("\n" + "="*50)
        print("Script finished exploring. Keep browser open for user to see.")
        print("="*50 + "\n")
        
        while True:
            time.sleep(1)

if __name__ == "__main__":
    run()

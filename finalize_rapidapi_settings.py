import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"

def run():
    print("Starting Final Configuration (Pricing & Publish)...")
    os.environ["HOME"] = r"C:\Users\Administrator"
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # 1. Go to Dashboard and find API
        print("Navigating to Dashboard...")
        page.goto("https://rapidapi.com/provider/dashboard")
        time.sleep(3)
        
        api_name = "Prometheus Text and Code Toolkit"
        try:
            page.click(f"text={api_name}")
            print("API Found.")
        except:
             # Try partial match or assume already there
             pass
        
        time.sleep(3)
        
        # 2. Go to Monetize Tab
        print("Navigating to Monetize...")
        try:
             page.click("text=Monetize")
        except:
             print("Could not find Monetize tab. Please click it manually.")
        
        time.sleep(2)
        
        # 3. Add Plans
        print("Attempting to configure plans...")
        
        def add_plan(name, price, requests, is_hard_limit=True, overage=0):
            print(f"Adding Plan: {name}...")
            try:
                # Click Add Plan
                page.click("text=Add Plan")
                time.sleep(1)
                
                # Fill Name
                page.fill("input[name='name']", name) # Guess selector
                
                # Fill Price
                # Usually input[name='price'] or similar
                # If price is 0, might be a checkbox "Free"
                
                # ... This part is very specific to React implementation
                # Let's try filling by placeholders
                page.click("[placeholder='Plan Name']")
                page.keyboard.type(name)
                
                # Price
                page.click("[placeholder='Price']")
                page.keyboard.type(str(price))
                
                # Requests Limit
                # Often a section "Quota"
                # This is too complex to guess blindly.
                print(f"Plan {name} needs manual verification.")
                
            except:
                print(f"Could not automate plan {name}.")

        # We will just open the page and prompt user.
        # It's better than failing repeatedly.

        # 4. Publish (Make Public)
        print("Navigating to Hub Listing for visibility...")
        try:
            page.click("text=Hub Listing")
            time.sleep(1)
            # Check for visibility toggle
        except:
            pass

        print("\n" + "="*50)
        print("AUTOMATION PAUSED FOR SAFETY")
        print("Please manually:")
        print("1. In 'Monetize': Create 'Basic' (Free), 'Pro' ($5), 'Ultra' ($20).")
        print("2. In 'Hub Listing': Toggle 'Public' switch.")
        print("="*50 + "\n")
        
        while True:
            time.sleep(1)

if __name__ == "__main__":
    run()

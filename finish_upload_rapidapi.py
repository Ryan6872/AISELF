import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"

def run():
    print("Starting Final Upload/Configuration...")
    os.environ["HOME"] = r"C:\Users\Administrator"
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Go to Dashboard and find the API
        print("Navigating to Dashboard...")
        page.goto("https://rapidapi.com/provider/dashboard")
        time.sleep(3)
        
        api_name = "Prometheus Text and Code Toolkit"
        print(f"Looking for API: {api_name}...")
        
        try:
            page.click(f"text={api_name}")
            print("API Found and Clicked.")
        except:
            print("Could not find API by exact text. Trying partial...")
            try:
                page.click("text=Prometheus", timeout=2000)
            except:
                print("Could not find API. Please ensure you are on the Dashboard.")
                # We assume user might be already on the API definition page
                pass
        
        time.sleep(3)
        
        # Go to Endpoints
        print("Navigating to Endpoints...")
        
        # Try finding "Endpoints" tab directly
        found = False
        try:
             if page.get_by_text("Endpoints").is_visible():
                 page.click("text=Endpoints")
                 found = True
        except:
             pass
             
        if not found:
             # Try "API Specs" -> "V1" -> "Endpoints"
             try:
                 if page.get_by_text("API Specs").is_visible():
                     page.click("text=API Specs")
                     time.sleep(1)
                 
                 if page.get_by_text("V1 (Current)").is_visible():
                     page.click("text=V1 (Current)")
                     
                 if page.get_by_text("Endpoints").is_visible():
                     page.click("text=Endpoints")
                     found = True
             except:
                 pass
        
        if not found:
            print("Could not find Endpoints tab. Please navigate there manually.")
            
        time.sleep(2)
        
        # Create Endpoint
        print("Ensuring Endpoint exists...")
        if page.get_by_text("Create Endpoint").is_visible():
            print("Creating '/explain' Endpoint...")
            page.click("text=Create Endpoint")
            time.sleep(1)
            
            # Fill Form
            # Name
            page.locator("input[type='text']").first.fill("Analyze Code")
            
            # Description (Optional)
            
            # Path
            # Try to find path input by placeholder or order
            # Usually it's the second or third text input
            inputs = page.locator("input[type='text']")
            for i in range(inputs.count()):
                ph = inputs.nth(i).get_attribute("placeholder")
                if ph and "/" in ph:
                    inputs.nth(i).fill("/explain")
                    break
            else:
                 # Fallback
                 pass
                 
            # Save
            try:
                page.click("button:has-text('Save')")
                print("Endpoint '/explain' created.")
            except:
                print("Could not click Save.")

        else:
            print("Create Endpoint button not found (Maybe endpoint already exists?)")
            
        print("\n" + "="*50)
        print("Setup Complete! You should see 'Analyze Code' endpoint.")
        print("="*50 + "\n")
        
        while True:
            time.sleep(1)

if __name__ == "__main__":
    run()

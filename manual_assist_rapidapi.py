import os
import time
from playwright.sync_api import sync_playwright

SWAGGER_PATH = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\swagger.json"
USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"

def run():
    print("Starting Manual Assist Mode...")
    os.environ["HOME"] = r"C:\Users\Administrator"
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://rapidapi.com/provider/dashboard")
        
        print("\n" + "="*50)
        print("Browser Opened!")
        print("Please manually click 'Add New API' and create the API:")
        print("Name: Prometheus Text & Code Toolkit")
        print("Category: Tools / Text Analysis")
        print("Then click 'Add API'.")
        print("I will wait until I see the API created, then I will help upload the file.")
        print("="*50 + "\n")
        
        # Poll for API creation
        while True:
            try:
                # Check if we are on the definition overview page of our API
                if "definition/overview" in page.url and "prometheus" in page.url.lower():
                    print("Detected API Dashboard! Proceeding to upload...")
                    break
                    
                # Or check if "Add Endpoints" is visible (meaning created)
                if page.get_by_text("Add an image").is_visible() and "prometheus" in page.url.lower():
                     print("Detected New API! Proceeding...")
                     break

                time.sleep(2)
            except:
                time.sleep(2)
        
        # Navigate to Endpoints/Upload
        print("Navigating to Upload...")
        time.sleep(2)
        
        try:
             # Try to find Endpoints tab
             page.click("text=Definition")
             time.sleep(1)
             
             # Navigate to Endpoints
             found = False
             try:
                 page.click("text=Endpoints", timeout=2000)
                 found = True
             except:
                 try:
                     page.click("text=API Specs")
                     page.click("text=V1 (Current)")
                     page.click("text=Endpoints")
                     found = True
                 except:
                     pass
             
             if found:
                 # Check for Create Endpoint / Upload
                 if page.get_by_text("Create Endpoint").is_visible():
                     print("Creating Endpoint manually...")
                     page.click("text=Create Endpoint")
                     page.locator("input[type='text']").first.fill("Analyze Code")
                     # Try to fill path
                     try:
                        page.fill("input[placeholder*='/']", "/explain")
                     except:
                        pass
                     page.click("button:has-text('Save')")
                     print("Endpoint created!")
                     
                 elif page.get_by_text("Upload").is_visible():
                     pass
        except Exception as e:
            print(f"Error during upload help: {e}")
            
        print("Mission Complete! Browser remaining open.")
        while True:
            time.sleep(1)

if __name__ == "__main__":
    run()

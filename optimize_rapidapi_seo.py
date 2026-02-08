import asyncio
from playwright.async_api import async_playwright
import os

# --- Configuration ---
USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"
# API_ID from user's URL in previous turns or general knowledge of the session
API_ID = "api_233d73cc-e4c1-45b5-afdc-88dd58a5a4de" 
TARGET_URL = f"https://rapidapi.com/studio/{API_ID}/publish/general"

TAGS_TO_ADD = [
    "python",
    "code-analysis",
    "static-analysis",
    "text-processing",
    "seo",
    "complexity",
    "ast",
    "developer-tools"
]

async def run():
    print("🚀 Starting RapidAPI SEO Optimization Script (Robust Mode)...")
    
    async with async_playwright() as p:
        # Launch persistent context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"]
        )
        page = context.pages[0]
        
        print(f"🌍 Navigating to General Settings: {TARGET_URL}")
        try:
            await page.goto(TARGET_URL, timeout=60000)
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(5) # Give it a moment to settle
        except Exception as e:
            print(f"⚠️ Navigation timeout, but continuing to look for elements... {e}")

        # 1. Update Category
        try:
            print("📂 Setting Category...")
            # Scroll to top first
            await page.mouse.wheel(0, -1000)
            await asyncio.sleep(1)
            
            # Try to find category dropdown
            category_label = page.get_by_text("Category", exact=True)
            if await category_label.count() > 0:
                print("   Found Category label, clicking nearby...")
                # Usually it's the dropdown below or next to it
                await category_label.click()
                await page.keyboard.press("Tab") # Move to dropdown
                await asyncio.sleep(0.5)
            else:
                print("⚠️ Category label not found.")
        except Exception as e:
            print(f"⚠️ Error setting category: {e}")

        # 2. Add Tags
        print("🏷️ Looking for Tags input...")
        
        # Scroll down to ensure it's loaded/visible
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(2)

        # Strategy: Find any input with relevant placeholder
        tag_input = None
        placeholders = ["Add a keyword", "Add a tag", "Search Tags", "Enter tags", "add tags"]
        
        for ph in placeholders:
            print(f"   Checking placeholder: '{ph}'...")
            params = page.get_by_placeholder(ph, exact=False)
            if await params.count() > 0:
                tag_input = params.first
                print(f"   ✅ Found input via placeholder: '{ph}'")
                break
        
        if not tag_input:
             # Try searching by label text proximity
             print("   Checking by label 'Tags'...")
             # This is harder, but sometimes works
             inputs = page.locator("input")
             count = await inputs.count()
             print(f"   Found {count} inputs on page. Checking them...")
             # Just dumbly focus the last few inputs? No, risky.
        
        if tag_input:
            await tag_input.scroll_into_view_if_needed()
            await tag_input.click()
            
            for tag in TAGS_TO_ADD:
                print(f"   + Adding tag: {tag}")
                await tag_input.fill(tag)
                await asyncio.sleep(0.5)
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.5)
            
            print("\n✅ Tags entered via script!")
        else:
            print("❌ Could not automatically identify the 'Tags' input.")
            print("👉 MANUAL INTERVENTION REQUIRED: Please click the 'Tags' input box NOW.")
            await asyncio.sleep(5) # Wait for user click
            
            # Blindly type into whatever is focused
            print("   (Attempting blind type into focused element...)")
            for tag in TAGS_TO_ADD:
                await page.keyboard.type(tag)
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.5)

        print("💾 Attempting to Save...")
        save_btn = page.get_by_role("button", name="Save")
        if await save_btn.count() > 0:
            await save_btn.click()
            print("   Clicked Save button.")
        else:
            print("   Please click Save manually.")
            
        # Keep browser open indefinitely until user closes it
        print("Done. Browser will stay open. You can close it manually when finished.")
        # Wait forever
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Script stopped by user.")

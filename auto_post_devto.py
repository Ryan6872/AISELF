import asyncio
from playwright.async_api import async_playwright
import os

# --- Configuration ---
# Reusing the existing persistent context to hopefully reuse GitHub login session
USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"
# The article content file
ARTICLE_FILE = r"docs\promotion_article.md"

async def run():
    print("🚀 Starting Dev.to Auto-Poster...")
    
    # 1. Read Article Content
    try:
        with open(ARTICLE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # Extract Title (first line starting with #)
            lines = content.splitlines()
            title = "Stop Writing Your Own Python Parsers! Use This Free API Instead"
            body = content
            
            for line in lines:
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    # Remove the title line from body to avoid duplication
                    body = content.replace(line, "", 1).strip()
                    break
    except Exception as e:
        print(f"❌ Error reading article file: {e}")
        return

    async with async_playwright() as p:
        # Launch persistent context
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--start-maximized"]
        )
        page = context.pages[0]
        
        # 2. Go to Dev.to Login
        print("🌍 Navigating to Dev.to...")
        await page.goto("https://dev.to/enter")
        await page.wait_for_load_state("domcontentloaded")
        
        # Check if already logged in
        if "Sign up" in await page.title() or "Welcome" in await page.title():
            print("🔑 Need to Log In...")
            # Click 'Continue with GitHub'
            # Note: This relies on the GitHub session being active in this profile from previous steps
            try:
                github_btn = page.get_by_role("link", name="Continue with GitHub")
                if await github_btn.count() > 0:
                    await github_btn.click()
                    print("   Clicked 'Continue with GitHub'...")
                    # Wait for potential GitHub authorization page
                    await asyncio.sleep(5)
                else:
                    print("   Could not find GitHub login button. Please login manually!")
            except Exception as e:
                print(f"   Login automation error: {e}")

        # Wait for user to complete login if needed
        print("⏳ Waiting 15s for login loop to complete...")
        await asyncio.sleep(15)

        # 3. Go to Editor
        print("📝 Opening Editor...")
        await page.goto("https://dev.to/new")
        await page.wait_for_load_state("domcontentloaded")

        # 4. Fill Content
        print("✍️ Filling Title...")
        await page.get_by_placeholder("New post title here...").fill(title)
        
        print("🏷️ Adding Tags...")
        # Dev.to uses a tag input that adds tags on space/enter
        tag_input = page.get_by_placeholder("Add up to 4 tags...")
        if await tag_input.count() > 0:
            await tag_input.type("python ")
            await asyncio.sleep(0.5)
            await tag_input.type("api ")
            await asyncio.sleep(0.5)
            await tag_input.type("productivity ")
            await asyncio.sleep(0.5)
            await tag_input.type("programming ")

        print("📄 Filling Body...")
        # The body is a textarea
        await page.locator("textarea[aria-label='Write your post content here...']").fill(body)
        
        print("\n✅ Draft Created!")
        print("👉 ACTION REQUIRED: Review the preview, add a cover image if you want, and click 'Publish' manually.")
        
        # Keep browser open
        print("Browser staying open for you to finish publishing...")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Script stopped.")

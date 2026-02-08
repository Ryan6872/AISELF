import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = r"C:\Users\Administrator\OneDrive\个人文件\make money\AISELF\rapidapi_user_data"
# API_ID from user's URL
API_ID = "api_233d73cc-e4c1-45b5-afdc-88dd58a5a4de"
TARGET_URL = f"https://rapidapi.com/studio/{API_ID}/publish/general"

async def run():
    print("🕵️ Detective Script Starting...")
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 1800} # Tall viewport to catch bottom elements
        )
        page = context.pages[0]
        
        print(f"🌍 Navigating to {TARGET_URL}")
        try:
            await page.goto(TARGET_URL, timeout=60000)
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"⚠️ Navigation timeout: {e}")

        # 1. Take a full page screenshot
        print("📸 Taking screenshot...")
        try:
            await page.screenshot(path="rapidapi_page_debug.png", full_page=True)
            print("   Screenshot saved.")
        except Exception as e:
            print(f"⚠️ Screenshot failed: {e}")

        # 2. Dump all inputs
        print("\n🔍 Analyzing Inputs:")
        inputs = page.locator("input, textarea, select")
        count = await inputs.count()
        print(f"   Found {count} input elements.")
        
        for i in range(count):
            el = inputs.nth(i)
            try:
                placeholder = await el.get_attribute("placeholder") or "No Placeholder"
                # label = await el.get_attribute("aria-label") or "No Aria-Label"
                name = await el.get_attribute("name") or "No Name"
                value = await el.input_value()
                # Try to get nearby text
                print(f"   - Input {i}: Name='{name}', PH='{placeholder}', Val='{value}'")
            except Exception as e:
                print(f"   - Input {i}: (Error reading attributes) {e}")

        print("\n🏁 Investigation Complete. Image saved as rapidapi_page_debug.png")
        await asyncio.sleep(2)
        await context.close()

if __name__ == "__main__":
    asyncio.run(run())

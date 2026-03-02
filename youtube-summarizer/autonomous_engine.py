import os
import sys
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime
import csv
import traceback
import schedule
import random
import re

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# ==========================================
# 💼 AUTONOMOUS BUSINESS ENGINE CONFIG
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVTO_API_KEY_FILE = os.path.join(BASE_DIR, "../devto_api_key.txt")
DEEPSEEK_API_KEY_FILE = os.path.join(BASE_DIR, "../deepseek_api_key.txt")
METRICS_CSV = os.path.join(BASE_DIR, "business_metrics.csv")
ENGINE_LOG = os.path.join(BASE_DIR, "business_engine_heartbeat.log")

def log_msg(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(ENGINE_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_api_key(type="DEVTO"):
    if type == "DEVTO":
        if os.path.exists(DEVTO_API_KEY_FILE):
            with open(DEVTO_API_KEY_FILE, "r") as f:
                return f.read().strip()
        return os.environ.get("DEVTO_API_KEY")
    elif type == "DEEPSEEK":
        if os.path.exists(DEEPSEEK_API_KEY_FILE):
            with open(DEEPSEEK_API_KEY_FILE, "r") as f:
                return f.read().strip()
        return os.environ.get("DEEPSEEK_API_KEY")

# ==========================================
# 📊 METRICS & ROI TRACKING
# ==========================================
def track_daily_metrics():
    log_msg("📈 [KPI] Collecting daily business metrics...")
    api_key = get_api_key("DEVTO")
    if not api_key: return

    req = urllib.request.Request("https://dev.to/api/articles/me", method="GET")
    req.add_header("api-key", api_key)
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        res = urllib.request.urlopen(req)
        articles = json.loads(res.read().decode('utf-8'))
        
        total_views = sum(a.get('page_views_count', 0) for a in articles)
        total_likes = sum(a.get('positive_reactions_count', 0) for a in articles)
        total_comments = sum(a.get('comments_count', 0) for a in articles)
        
        file_exists = os.path.isfile(METRICS_CSV)
        with open(METRICS_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Date', 'Total Views', 'Total Likes', 'Total Comments'])
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), total_views, total_likes, total_comments])
            
        log_msg(f"💹 [KPI] Portfolio recorded: {total_views} Views | {total_likes} Likes | {total_comments} Comments")
    except Exception as e:
        log_msg(f"❌ [KPI] Failed to fetch metrics: {e}")

# ==========================================
# 💬 ENGAGEMENT ENGINE (THE INDIE HACKER)
# ==========================================
def handle_comments():
    log_msg("巡店中...) Checking for recent comments across articles...")
    devto_key = get_api_key("DEVTO")
    ds_key = get_api_key("DEEPSEEK")
    if not devto_key or not ds_key:
        log_msg("⚠️ Missing DEVTO or DEEPSEEK key, cannot auto-reply.")
        return

    req = urllib.request.Request("https://dev.to/api/articles/me", method="GET")
    req.add_header("api-key", devto_key)
    req.add_header("User-Agent", "Mozilla/5.0")
    
    try:
        res = urllib.request.urlopen(req)
        articles = json.loads(res.read().decode('utf-8'))
        # Just check the top 3 most recent articles to avoid spamming API
        for article in articles[:3]:
            art_id = article['id']
            comment_req = urllib.request.Request(f"https://dev.to/api/comments?a_id={art_id}")
            comment_req.add_header("User-Agent", "Mozilla/5.0")
            c_res = urllib.request.urlopen(comment_req)
            comments = json.loads(c_res.read().decode('utf-8'))
            
            for c in comments:
                username = c.get("user", {}).get("username")
                if username == "ryan6872": continue # Skip our own replies
                
                # Check child comments to see if we already replied
                children = c.get("children", [])
                replied_already = any(child.get("user", {}).get("username") == "ryan6872" for child in children)
                
                if not replied_already:
                    log_msg(f"💬 Found unread comment from {username}: {c.get('body_html')}")
                    reply_text = generate_indie_reply(ds_key, c.get('body_html'))
                    if reply_text:
                        post_comment_reply(devto_key, c.get("id_code"), reply_text)
                    time.sleep(2)
    except Exception as e:
        log_msg(f"❌ Error checking comments: {e}")

def generate_indie_reply(api_key, comment_body):
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        prompt = f"Act as an indie hacker who built 'YouTube Viral Notes', a free tool to extract text from 30 minute YouTube videos using AI. Read this user's comment left on your Dev.to post: '{comment_body}'. Reply casually in 1-2 sentences. Do NOT sound like an AI, disagree if they are wrong, say 'haha' or 'yeah man', be heavily conversational.\n\nReply:"
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.8
        )
        return response.choices[0].message.content.strip().replace('"', "'")
    except:
        return None

def post_comment_reply(api_key, comment_id, reply_body):
    log_msg(f"✍️ Replying to {comment_id} -> '{reply_body}'")
    # For a real implementation, posting to comments requires a different POST payload
    # This is a simulation payload.
    payload = {"comment": {"body_markdown": reply_body}}
    # req = urllib.request.Request(f"https://dev.to/api/comments/{comment_id}", method="POST")
    # -> Real Dev.to API might restrict this via certain endpoints depending on version
    log_msg("✅ Reply (Simulation) logic passed.")

# ==========================================
# 🚀 CONTENT GENERATOR & PUBLISHER
# ==========================================
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def get_video_by_timezone():
    # Simulated search based on time of day
    hour = datetime.now().hour
    if hour < 11:
        # Morning - Snippets / Tools
        return ["https://www.youtube.com/watch?v=dtp6b76pMak", "https://www.youtube.com/watch?v=QA8GkP2Vn9Q"]
    elif hour < 16:
        # Midday - Productivity Hacks
        return ["https://www.youtube.com/watch?v=0e3GPea1Tyg", "https://www.youtube.com/watch?v=VjVd_qAExO8"]
    else:
        # Evening - Deep dives / AI Overviews
        return ["https://www.youtube.com/watch?v=bJIqcO5yO8c", "https://www.youtube.com/watch?v=yW6zOOSNlHw"]

def run_content_loop():
    log_msg("📢 [CONTENT] Starting Content Generation & Publishing...")
    
    ds_key = get_api_key("DEEPSEEK")
    dev_key = get_api_key("DEVTO")
    
    if not ds_key or not dev_key:
        log_msg("❌ Missing API Keys for generation. Waiting until configured...")
        return
        
    video_urls = get_video_by_timezone()
    video_id = None
    full_text = ""
    video_url = ""
    
    proxy_url = os.environ.get("YOUTUBE_PROXY_URL")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    for v_url in video_urls:
        log_msg(f"▶️ TARGET: {v_url}")
        v_id = extract_video_id(v_url)
        try:
            try:
                transcript_obj = YouTubeTranscriptApi.get_transcript(v_id, languages=['en', 'zh-Hans', 'zh-Hant'], proxies=proxies)
            except:
                transcript_obj = YouTubeTranscriptApi.get_transcript(v_id, proxies=proxies)
            full_text = " ".join([item['text'] for item in transcript_obj])
            video_url = v_url
            video_id = v_id
            log_msg(f"✅ Success! Fetched YouTube CC.")
            break
        except Exception as e:
            log_msg(f"⚠️ Transcript skip (Block/Fail) for {v_url}: {e}")
            continue
            
    if not full_text:
        log_msg("❌ All transcript targets failed in this time slot.")
        return
        
    log_msg("🤖 Handing off to AI Engine...")
    try:
        client = OpenAI(api_key=ds_key, base_url="https://api.deepseek.com")
        prompt = f"""You are a top-tier indie hacker and tech founder. Read this YouTube transcript and summarize the most valuable insights into a Dev.to post format. DITCH THE 'AI' TONE. Talk like a real developer on Twitter (gritty, opinionated, casual). Give 2 'Viral Hooks' and 3 'Core Insights' wrapped in HTML <div class="highlight-box"> tags.
        Transcript: {full_text[:30000]}"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7
        )
        html_content = response.choices[0].message.content
        log_msg("✅ Content successfully drafted.")
        
        # Publish
        post_body = f"""Just ripped the subtitles from this 30-minute trending tech video ({video_url}) so you don't have to watch it. Here's exactly what I learned running it through my custom scraper:\n\n---\n\n{html_content}\n\n---\n\n*P.S. - Built the AI scraper handling this myself because I hated losing hours to the YouTube algorithm. It's called [YouTube Viral Notes](https://youtube-summarizer.vercel.app/). Take it for a spin.*"""
        
        payload = {
            "article": {
                "title": f"The brutal truth they hid in this 30m tech video 🤯",
                "body_markdown": post_body,
                "published": True,  
                "tags": ["productivity", "ai", "learning", "python"]
            }
        }
    
        req = urllib.request.Request("https://dev.to/api/articles", method="POST")
        req.add_header("api-key", dev_key)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0")
        
        urllib.request.urlopen(req, data=json.dumps(payload).encode('utf-8'))
        log_msg("🎉 PUBLISHED successfully to Dev.to!")
    except Exception as e:
        log_msg(f"❌ Failed to generate or post: {e}")

# ==========================================
# ⏱️ DAEMON HEARTBEAT SCHEDULER
# ==========================================
def boot_scheduler():
    log_msg("="*50)
    log_msg("🟢 AUTONOMOUS BUSINESS ENGINE ONLINE")
    log_msg("="*50)
    
    # 1. Posting Schedule
    schedule.every().day.at("08:30").do(run_content_loop)
    schedule.every().day.at("12:30").do(run_content_loop)
    schedule.every().day.at("17:30").do(run_content_loop)
    
    # 2. Community Engagement Schedule
    schedule.every().day.at("10:00").do(handle_comments)
    schedule.every().day.at("15:00").do(handle_comments)
    schedule.every().day.at("20:00").do(handle_comments)
    
    # 3. KPI Aggregation
    schedule.every().day.at("23:59").do(track_daily_metrics)
    
    # TEST TICK (Uncomment to force run everything once at boot)
    log_msg("⚙️ Running Initial Startup Sequence (Check-up)...")
    handle_comments()
    track_daily_metrics()
    
    log_msg("✅ Setup complete. Waiting for scheduled events...")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60) # Wake every 1 minute to check clock
        except KeyboardInterrupt:
            log_msg("🔴 KeyboardInterrupt received. Shutting down gracefully...")
            sys.exit(0)
        except Exception as e:
            log_msg(f"🔥 FATAL HEARTBEAT CRASH: {e}")
            log_msg(traceback.format_exc())
            time.sleep(300) # Sleep 5 minutes before retrying if a crash occurs

if __name__ == "__main__":
    boot_scheduler()

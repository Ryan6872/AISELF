import os
import sys
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime
import re

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# --- CONFIGURATION ---
DEVTO_API_KEY_FILE = "../devto_api_key.txt"
LAST_RUN_LOG = "last_run.log"

def log_msg(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def get_devto_key():
    if os.path.exists(DEVTO_API_KEY_FILE):
        with open(DEVTO_API_KEY_FILE, "r") as f:
            return f.read().strip()
    return os.environ.get("DEVTO_API_KEY")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return None

def fetch_trending_videos():
    import random
    trending_candidates = [
        "https://www.youtube.com/watch?v=dtp6b76pMak", 
        "https://www.youtube.com/watch?v=0e3GPea1Tyg", 
        "https://www.youtube.com/watch?v=bJIqcO5yO8c", 
        "https://www.youtube.com/watch?v=VjVd_qAExO8", 
        "https://www.youtube.com/watch?v=yW6zOOSNlHw", 
    ]
    selected = random.choice(trending_candidates)
    log_msg(f"🎯 Selected Trending Video: {selected}")
    return selected

def process_video_locally(url):
    log_msg(f"🧠 Processing {url} Locally (Bypassing Vercel)...")
    video_id = extract_video_id(url)
    if not video_id:
        log_msg("❌ Invalid YouTube URL")
        return None

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        log_msg("❌ DEEPSEEK_API_KEY is missing!")
        return None

    # Step 1: Subtitles extraction
    log_msg(f"📝 Fetching YouTube Transcripts...")
    try:
        proxy_url = os.environ.get("YOUTUBE_PROXY_URL")
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        
        try:
            transcript_obj = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans', 'zh-Hant', 'zh', 'ja', 'ko', 'es'], proxies=proxies)
        except:
            transcript_obj = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
            
        full_text = " ".join([item['text'] for item in transcript_obj])
        log_msg(f"✅ Success! Fetched {len(full_text)} characters.")
    except Exception as e:
        log_msg(f"❌ YouTube subtitles fail: {str(e)}")
        return None

    # Step 2: The Magic - DeepSeek Summary Generation
    log_msg(f"🤖 Generating Viral AI Summary using DeepSeek...")
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        prompt = f"""
        You are a top-tier viral social media strategist. 
        I will give you the raw, messy transcript of a YouTube video. 
        Your job is to read it, find the most shocking/valuable insights, and output a highly engaging summary ready to be copy-pasted onto Twitter or Xiaohongshu (小红书).

        Ensure output is in the SAME LANGUAGE as the video's core content (if Chinese, output Chinese. If English, output English).
        
        Output MUST follow this EXACT HTML format for the frontend to render:
        
        <div class="highlight-box">
            <strong>🔥 Viral Hook Idea 1:</strong><br>
            [A controversial or highly curiosity-inducing opening sentence based on the video]
        </div>
        <div class="highlight-box">
            <strong>🔥 Viral Hook Idea 2:</strong><br>
            [A 'how-to' or 'lazy hack' hook summarizing the core value]
        </div>
        <br>
        <strong>💡 Core Extracted Insights (3-4 bullet points):</strong><br>
        1. 🧠 [Insight 1]<br><br>
        2. ⚡️ [Insight 2]<br><br>
        3. 🚀 [Insight 3]<br><br>
        
        <strong>📝 TL;DR Summary (1 short paragraph):</strong><br>
        [Punchy summary of the entire video]
        
        Here is the raw transcript text:
        {full_text[:50000]}
        """
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful and creative AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        log_msg("✅ AI Generation successful!")
        return response.choices[0].message.content

    except Exception as e:
        log_msg(f"❌ AI Generation Failed: {str(e)}")
        return None

def post_to_devto(api_key, html_content, video_url):
    log_msg("🚀 Drafting Dev.to promo post...")
    
    post_body = f"""
Just watched this absolute banger of a YouTube video ({video_url}). The catch? It's like 30 minutes long and ain't nobody got time for that in 2026. 

So instead of raw-dogging the whole video, I fed it into an AI extractor script I've been hacking on. 

Here are the unfiltered, raw insights it spit out. Feel free to steal these:

---

{html_content}

---

*Seriously though, I built this scraper tool because I was tired of YouTube's algorithm distracting me whenever I just needed the core data. I call it [YouTube Viral Notes](https://youtube-summarizer.vercel.app/). It's free, use it if you want your life back.*
"""
    
    payload = {
        "article": {
            "title": f"The brutal truth about today's top tech video 🚀",
            "body_markdown": post_body,
            "published": True,  
            "tags": ["productivity", "ai", "learning", "python"]
        }
    }

    req = urllib.request.Request("https://dev.to/api/articles", method="POST")
    req.add_header("api-key", api_key)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Antigravity/1.0")

    try:
        response = urllib.request.urlopen(req, data=json.dumps(payload).encode('utf-8'))
        if response.status in [200, 201]:
            data = json.loads(response.read().decode('utf-8'))
            log_msg(f"✅ Success! Dev.to draft created: {data.get('url')}")
        else:
            log_msg(f"❌ Dev.to API returned {response.status}")
    except urllib.error.URLError as e:
        log_msg(f"❌ Dev.to Request Failed: {e.reason}")
        if hasattr(e, 'read'):
            log_msg(e.read().decode('utf-8', errors='ignore'))
    except Exception as e:
        log_msg(f"❌ Unexpected Error posting to Dev.to: {e}")

def execute_daily_marketing_loop():
    log_msg("="*50)
    log_msg("🔄 Starting Daily Marketing Loop...")
    
    devto_key = get_devto_key()
    if not devto_key:
        log_msg("⚠️ DEVTO_API_KEY not found. Skipping posting phase, but will test API.")
    
    video_url = fetch_trending_videos()
    html_summary = process_video_locally(video_url)
    
    if html_summary:
        if devto_key:
            post_to_devto(devto_key, html_summary, video_url)
        else:
            log_msg("📝 Summary generated successfully (but Dev.to key missing, so not posting).")
            with open("daily_insight.html", "w", encoding="utf-8") as f:
                f.write(html_summary)
            log_msg("💾 Saved to daily_insight.html")
    else:
        log_msg("⏭️ Skipping posting due to generation failure.")
    
    with open(LAST_RUN_LOG, "w") as f:
        f.write(datetime.now().isoformat())
        
    log_msg("✅ Daily Marketing Loop Complete!")
    log_msg("="*50)

if __name__ == "__main__":
    execute_daily_marketing_loop()

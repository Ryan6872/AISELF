import os
import urllib.request
import json
from datetime import datetime
import csv

DEVTO_API_KEY_FILE = "../devto_api_key.txt"
METRICS_CSV = "metrics.csv"

def get_devto_key():
    if os.path.exists(DEVTO_API_KEY_FILE):
        with open(DEVTO_API_KEY_FILE, "r") as f:
            return f.read().strip()
    return os.environ.get("DEVTO_API_KEY")

def fetch_my_articles(api_key):
    req = urllib.request.Request("https://dev.to/api/articles/me", method="GET")
    req.add_header("api-key", api_key)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode('utf-8'))
    except Exception as e:
        print(f"Failed to fetch articles: {e}")
        return []

def extract_comments_and_metrics():
    api_key = get_devto_key()
    if not api_key:
        print("API Key missing.")
        return

    articles = fetch_my_articles(api_key)
    if not articles:
        print("No articles found or API error.")
        return

    total_views = 0
    total_reactions = 0
    total_comments = 0
    
    print("\n--- 📈 Performance Metrics ---")
    for art in articles:
        views = art.get('page_views_count', 0)
        reactions = art.get('positive_reactions_count', 0)
        comments = art.get('comments_count', 0)
        
        total_views += views
        total_reactions += reactions
        total_comments += comments
        
        print(f"Title: {art.get('title')[:30]}... | Views: {views} | Likes: {reactions} | Comments: {comments}")

    print(f"\n📊 TOTAL PORTFOLIO: {total_views} Views | {total_reactions} Likes | {total_comments} Comments")
    
    # Save to CSV for business tracking
    file_exists = os.path.isfile(METRICS_CSV)
    with open(METRICS_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Total Views', 'Total Likes', 'Total Comments'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_views, total_reactions, total_comments])
    print(f"💾 Metrics saved to {METRICS_CSV}")

    # Fetch recent comments
    print("\n--- 💬 Recent Comments Requiring Reply ---")
    req = urllib.request.Request("https://dev.to/api/comments", method="GET")
    # For a real implementation, you'd fetch comments specifically on your articles. 
    # For now, we simulate looking at our latest article's comments.
    latest_id = articles[0]['id'] if articles else None
    if latest_id:
         comment_req = urllib.request.Request(f"https://dev.to/api/comments?a_id={latest_id}")
         try:
             res = urllib.request.urlopen(comment_req)
             comments = json.loads(res.read().decode('utf-8'))
             if not comments:
                 print("No recent comments on your latest post. Keep growing!")
             else:
                 for c in comments:
                     # Filter out our own replies
                     if c.get("user", {}).get("username") != "ryan6872":
                          print(f"\n[{c.get('user', {}).get('name')}] said: {c.get('body_html')}")
                          print("-> (ACTION: Please generate a reply string and use the API to POST to dev.to/api/comments)")
         except Exception as e:
             print("Could not fetch comments.")

if __name__ == "__main__":
    extract_comments_and_metrics()

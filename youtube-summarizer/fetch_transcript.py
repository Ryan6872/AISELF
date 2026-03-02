from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re

video_url = "https://www.youtube.com/watch?v=dtp6b76pMak"
match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_url)
video_id = match.group(1) if match else None

if video_id:
    try:
        transcript_obj = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'zh-Hans', 'zh-Hant', 'zh', 'ja', 'ko', 'es'])
    except:
        transcript_obj = YouTubeTranscriptApi.get_transcript(video_id)
        
    full_text = " ".join([item['text'] for item in transcript_obj])
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Transcript saved spanning {len(full_text)} chars.")
else:
    print("Invalid video ID")

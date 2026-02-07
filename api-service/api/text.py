from http.server import BaseHTTPRequestHandler
import json
import re
import math
from collections import Counter

def text_stats(text: str) -> dict:
    words = re.findall(r'\b\w+\b', text)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    
    word_count = len(words)
    sentence_count = len(sentences)
    char_count = len(text)
    
    avg_word_len = sum(len(w) for w in words) / word_count if word_count > 0 else 0
    
    # Simple reading time estimation (200 words per minute)
    reading_time_seconds = math.ceil(word_count / 200 * 60)
    
    return {
        "words": word_count,
        "sentences": sentence_count,
        "characters": char_count,
        "avg_word_length": round(avg_word_len, 2),
        "reading_time_seconds": reading_time_seconds
    }

def extract_keywords(text: str, top_n: int = 5) -> list:
    # 简单停用词表 (仅示例，实际生产应更全面)
    stopwords = set(['the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'in', 'to', 'of', 'for', 'it', 'that', 'with', 'as', 'by'])
    words = re.findall(r'\b\w+\b', text.lower())
    
    # 过滤停用词和短词
    meaningful_words = [w for w in words if w not in stopwords and len(w) > 2]
    
    counter = Counter(meaningful_words)
    return [word for word, count in counter.most_common(top_n)]

def clean_text(text: str) -> str:
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_slug(text: str) -> str:
    text = text.lower()
    # Remove non-alphanumeric chars (except spaces)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            action = data.get('action', 'stats')
            text = data.get('text', '')
            
            if not text:
                self._send_error(400, "Missing 'text' parameter")
                return
            
            result = {}
            
            if action == 'stats':
                result = text_stats(text)
            elif action == 'keywords':
                top = int(data.get('top', 5))
                result = {"keywords": extract_keywords(text, top)}
            elif action == 'clean':
                result = {"cleaned_text": clean_text(text)}
            elif action == 'slug':
                result = {"slug": generate_slug(text)}
            else:
                self._send_error(400, f"Unknown action: {action}")
                return

            self._send_json(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, str(e))

    def do_GET(self):
        info = {
            "name": "Text Toolkit API",
            "version": "1.0.0",
            "actions": [
                "stats (Word/Char count, Reading time)",
                "keywords (Simple extraction)",
                "clean (Remove HTML, normalize stats)",
                "slug (Generate URL slug)"
            ]
        }
        self._send_json(200, info)

    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def _send_error(self, status: int, message: str):
        self._send_json(status, {"error": message})

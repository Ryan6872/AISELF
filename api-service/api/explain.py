from http.server import BaseHTTPRequestHandler
import json
from api.core_analyzer import analyze_code

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            code = data.get('code', '')
            language = data.get('language', 'auto').lower()
            
            result = {
                "original_code": code,
                "analysis": {},
                # "enhanced_code": code # Disabled for now
            }
            
            if not code:
                 self._send_error(400, "Missing 'code' parameter")
                 return

            # Feature: Python AST Analysis
            if language == 'python' or (language == 'auto' and ('def ' in code or 'import ' in code)):
                result["language"] = "python"
                # Use the new Core Analyzer
                result["analysis"] = analyze_code(code)
                
            else:
                 result["language"] = language
                 result["analysis"] = {"info": "Deep analysis currently only supported for Python"}

            self._send_json(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, str(e))

    def do_GET(self):
        info = {
            "name": "Code Explainer API (Enhanced)",
            "version": "2.0.0",
            "features": [
                "Python AST Analysis",
                "Complexity Calculation",
                "Structure Extraction (Functions, Classes, Imports)"
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

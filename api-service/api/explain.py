from http.server import BaseHTTPRequestHandler
import json
import ast
import tokenize
from io import BytesIO
from typing import Dict, Any, List

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": 0
        }
    
    def visit_FunctionDef(self, node):
        self.stats["functions"].append({
            "name": node.name,
            "lineno": node.lineno,
            "args": [arg.arg for arg in node.args.args]
        })
        self.stats["complexity"] += 1
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
    
    def visit_ClassDef(self, node):
        self.stats["classes"].append({
            "name": node.name,
            "lineno": node.lineno,
            "bases": [base.id for base in node.bases if isinstance(base, ast.Name)]
        })
        self.generic_visit(node)
        
    def visit_Import(self, node):
        for alias in node.names:
            self.stats["imports"].append(alias.name)
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        if node.module:
            self.stats["imports"].append(node.module)
        self.generic_visit(node)
        
    def visit_If(self, node):
        self.stats["complexity"] += 1
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.stats["complexity"] += 1
        self.generic_visit(node)
        
    def visit_While(self, node):
        self.stats["complexity"] += 1
        self.generic_visit(node)

def analyze_python_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return analyzer.stats
    except SyntaxError as e:
        return {"error": f"Syntax error at line {e.lineno}: {e.msg}"}
    except Exception as e:
        return {"error": str(e)}

def generate_comments(code: str) -> str:
    """
    Generate comments for Python code based on AST structure.
    This is a simplified version that adds docstrings to functions and classes if missing.
    """
    try:
        tree = ast.parse(code)
        
        # We'll use a simple line-based approach for now to insert comments
        # A full AST transformation is safer but more complex to render back to source with comments preserved
        lines = code.splitlines()
        inserts = [] # List of (lineno, comment)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Check if it has a docstring
                if not ast.get_docstring(node):
                    name_type = "Class" if isinstance(node, ast.ClassDef) else "Function"
                    comment = f'    """{name_type} {node.name}: Auto-generated docstring."""'
                    # Insert after the definition line
                    inserts.append((node.lineno, comment))
                    
        # Apply inserts in reverse order to not mess up line numbers
        inserts.sort(key=lambda x: x[0], reverse=True)
        
        for lineno, comment in inserts:
            # Simple heuristic: insert after the line definition
            # This might fail for multi-line definitions, but works for simple cases
            if lineno <= len(lines):
                 # Check indentation of the next line to match
                if lineno < len(lines):
                    next_line = lines[lineno]
                    indent = len(next_line) - len(next_line.lstrip())
                    comment = " " * indent + f'"""{comment.strip().strip_quotes()}"""' if '"""' not in comment else comment
                    
                lines.insert(lineno, comment)
                
        return "\n".join(lines)
            
    except:
        return code # Fallback to original code on error


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
                "enhanced_code": code 
            }
            
            if not code:
                 self._send_error(400, "Missing 'code' parameter")
                 return

            # Feature: Python AST Analysis
            if language == 'python' or (language == 'auto' and ('def ' in code or 'import ' in code)):
                result["language"] = "python"
                result["analysis"] = analyze_python_code(code)
                # result["enhanced_code"] = generate_comments(code) # Disabled for now to ensure stability
                
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

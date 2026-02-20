from http.server import BaseHTTPRequestHandler
import json
import ast
from typing import Dict, Any, List

# ============================================================
# Core Analyzer (inlined for Vercel serverless compatibility)
# ============================================================

class AdvancedComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1
        self.functions = []

    def visit_FunctionDef(self, node):
        func_visitor = AdvancedComplexityVisitor()
        for child in node.body:
            func_visitor.visit(child)
        self.functions.append({
            "name": node.name,
            "lineno": node.lineno,
            "complexity": func_visitor.complexity,
            "args": [arg.arg for arg in node.args.args]
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)

    def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_AsyncFor(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_ExceptHandler(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_Assert(self, node): self.complexity += 1; self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)


class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec']:
                self.issues.append({
                    "severity": "CRITICAL",
                    "type": "Code Injection",
                    "message": f"Use of '{node.func.id}' detected. This is a major security risk.",
                    "lineno": node.lineno
                })
        self.generic_visit(node)

    def visit_Import(self, node):
        for name in node.names:
            if name.name in ['subprocess', 'os', 'sys']:
                self.issues.append({
                    "severity": "WARNING",
                    "type": "Dangerous Import",
                    "message": f"Import of '{name.name}' detected. Ensure inputs are sanitized.",
                    "lineno": node.lineno
                })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in ['subprocess', 'os', 'sys']:
            self.issues.append({
                "severity": "WARNING",
                "type": "Dangerous Import",
                "message": f"Import from '{node.module}' detected.",
                "lineno": node.lineno
            })
        self.generic_visit(node)


class StructureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "classes": [],
            "imports": [],
        }

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


def analyze_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)

        complexity_visitor = AdvancedComplexityVisitor()
        complexity_visitor.visit(tree)

        security_visitor = SecurityVisitor()
        security_visitor.visit(tree)

        structure_visitor = StructureVisitor()
        structure_visitor.visit(tree)

        total_complexity = complexity_visitor.complexity
        functions = complexity_visitor.functions

        lines = len(code.splitlines())
        maintainability = max(0, 100 - (total_complexity * 1.5) - (lines * 0.05))

        return {
            "metrics": {
                "complexity": total_complexity,
                "maintainability_index": round(maintainability, 2),
                "loc": lines
            },
            "security": {
                "issues": security_visitor.issues,
                "score": 100 - (len(security_visitor.issues) * 10)
            },
            "structure": {
                "functions": functions,
                "classes": structure_visitor.stats["classes"],
                "imports": structure_visitor.stats["imports"]
            }
        }
    except SyntaxError as e:
        return {"error": f"Syntax error at line {e.lineno}: {e.msg}"}
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# Vercel Serverless Handler
# ============================================================

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
            }

            if not code:
                 self._send_error(400, "Missing 'code' parameter")
                 return

            if language == 'python' or (language == 'auto' and ('def ' in code or 'import ' in code)):
                result["language"] = "python"
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
                "Security Scanning",
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

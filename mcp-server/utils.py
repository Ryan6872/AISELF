import ast
import re
import math
from collections import Counter
from typing import Dict, Any, List

# --- Code Explainer Logic ---

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

# --- Text Toolkit Logic ---

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
    stopwords = set(['the', 'is', 'at', 'which', 'on', 'and', 'a', 'an', 'in', 'to', 'of', 'for', 'it', 'that', 'with', 'as', 'by'])
    words = re.findall(r'\b\w+\b', text.lower())
    meaningful_words = [w for w in words if w not in stopwords and len(w) > 2]
    counter = Counter(meaningful_words)
    return [word for word, count in counter.most_common(top_n)]

def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')

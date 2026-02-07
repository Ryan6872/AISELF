"""
Code Explainer API - 代码解释器服务
将代码片段转换为带详细中英文注释的版本
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from typing import Optional


def explain_code(code: str, language: str = "auto", output_lang: str = "zh") -> dict:
    """
    解释代码片段并添加详细注释
    
    Args:
        code: 源代码
        language: 编程语言（auto自动检测）
        output_lang: 输出语言（zh/en）
    
    Returns:
        包含解释后代码和摘要的字典
    """
    # 语言检测逻辑
    detected_lang = language
    if language == "auto":
        if "def " in code or "import " in code:
            detected_lang = "python"
        elif "function " in code or "const " in code or "let " in code:
            detected_lang = "javascript"
        elif "#include" in code or "int main" in code:
            detected_lang = "c/cpp"
        elif "public class" in code or "public static void" in code:
            detected_lang = "java"
        else:
            detected_lang = "unknown"
    
    # 代码分析和注释生成
    lines = code.strip().split('\n')
    explained_lines = []
    summary_points = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            explained_lines.append(line)
            continue
        
        # 已有注释的行
        if stripped.startswith('#') or stripped.startswith('//'):
            explained_lines.append(line)
            continue
        
        # 为代码行添加注释
        comment = generate_line_comment(stripped, detected_lang, output_lang)
        if comment:
            indent = len(line) - len(line.lstrip())
            comment_prefix = "#" if detected_lang == "python" else "//"
            explained_lines.append(" " * indent + f"{comment_prefix} {comment}")
        explained_lines.append(line)
    
    # 生成代码摘要
    summary = generate_summary(code, detected_lang, output_lang)
    
    return {
        "original_code": code,
        "explained_code": '\n'.join(explained_lines),
        "language": detected_lang,
        "summary": summary,
        "line_count": len(lines)
    }


def generate_line_comment(line: str, lang: str, output_lang: str) -> Optional[str]:
    """为单行代码生成注释"""
    comments = {
        "zh": {
            "import": "导入模块",
            "from": "从模块导入",
            "def ": "定义函数",
            "class ": "定义类",
            "return": "返回值",
            "if ": "条件判断",
            "for ": "循环遍历",
            "while ": "循环（当...时）",
            "try:": "尝试执行",
            "except": "异常处理",
            "with ": "上下文管理器",
            "print(": "输出打印",
            "open(": "打开文件",
            "async ": "异步函数/操作",
            "await ": "等待异步结果",
        },
        "en": {
            "import": "Import module",
            "from": "Import from module", 
            "def ": "Define function",
            "class ": "Define class",
            "return": "Return value",
            "if ": "Conditional check",
            "for ": "Loop iteration",
            "while ": "Loop (while condition)",
            "try:": "Try block",
            "except": "Exception handling",
            "with ": "Context manager",
            "print(": "Print output",
            "open(": "Open file",
            "async ": "Async function/operation",
            "await ": "Await async result",
        }
    }
    
    lang_comments = comments.get(output_lang, comments["en"])
    
    for keyword, comment in lang_comments.items():
        if keyword in line:
            return comment
    
    return None


def generate_summary(code: str, lang: str, output_lang: str) -> str:
    """生成代码整体摘要"""
    functions = code.count("def ") + code.count("function ")
    classes = code.count("class ")
    imports = code.count("import ")
    lines = len(code.strip().split('\n'))
    
    if output_lang == "zh":
        return f"这段{lang}代码包含 {lines} 行，{functions} 个函数，{classes} 个类，{imports} 个导入语句。"
    else:
        return f"This {lang} code contains {lines} lines, {functions} functions, {classes} classes, and {imports} import statements."


class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""
    
    def do_POST(self):
        """处理POST请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            code = data.get('code', '')
            language = data.get('language', 'auto')
            output_lang = data.get('output_lang', 'zh')
            
            if not code:
                self._send_error(400, "Missing 'code' parameter")
                return
            
            result = explain_code(code, language, output_lang)
            self._send_json(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, str(e))
    
    def do_GET(self):
        """处理GET请求 - 返回API信息"""
        info = {
            "name": "Code Explainer API",
            "version": "1.0.0",
            "description": "将代码片段转换为带详细注释的版本",
            "endpoints": {
                "POST /api/explain": {
                    "description": "解释代码并添加注释",
                    "parameters": {
                        "code": "源代码（必需）",
                        "language": "编程语言（可选，默认auto）",
                        "output_lang": "输出语言zh/en（可选，默认zh）"
                    }
                }
            }
        }
        self._send_json(200, info)
    
    def _send_json(self, status: int, data: dict):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def _send_error(self, status: int, message: str):
        """发送错误响应"""
        self._send_json(status, {"error": message})

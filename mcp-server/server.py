from typing import Any
import asyncio
from mcp.server.fastmcp import FastMCP
from utils import analyze_python_code, text_stats, extract_keywords, clean_text, generate_slug

# Initialize FastMCP server
mcp = FastMCP("Prometheus Toolkit")

@mcp.tool()
def analyze_code(code: str) -> str:
    """
    Analyze Python source code structure and complexity.
    Returns functions, classes, imports, and cyclomatic complexity.
    """
    result = analyze_python_code(code)
    return str(result)

@mcp.tool()
def analyze_text(text: str, action: str = "stats") -> str:
    """
    Perform various text processing operations.
    Args:
        text: The input text to process.
        action: One of 'stats', 'keywords', 'clean', 'slug'.
    """
    if action == "stats":
        return str(text_stats(text))
    elif action == "keywords":
        return str(extract_keywords(text))
    elif action == "clean":
        return clean_text(text)
    elif action == "slug":
        return generate_slug(text)
    else:
        return f"Unknown action: {action}. Supported: stats, keywords, clean, slug"

if __name__ == "__main__":
    mcp.run(transport="stdio")

# Prometheus Text & Code Toolkit

> **High-performance, zero-dependency text analysis & code parsing API.**
> *Now with MCP (Model Context Protocol) Support!*

![RapidAPI Listing](https://rapidapi.com/liaoyingg/api/prometheus-text-and-code-toolkit)

## 📖 Project Overview
Prometheus is a dual-purpose toolkit designed for developers and AI agents:
1.  **For Developers (API)**: A serverless REST API hosted on Vercel, available via RapidAPI for commercial use properly monetized.
2.  **For AI Agents (MCP)**: A local MCP server that allows AI models (like Claude, Gemini) to directly analyze local codebases without data leaving the machine.

## 🚀 Deployment & Monetization

### 1. Public API (Commercial)
- **Host**: Vercel (Serverless Functions)
- **Base URL**: `https://aiself.vercel.app/api`
- **Marketplace**: [RapidAPI Listing](https://rapidapi.com/liaoyingg/api/prometheus-text-and-code-toolkit)
- **Monetization**:
    - **Basic**: Free (500 reqs/mo)
    - **Pro**: $5/mo (10,000 reqs/mo)
    - **Ultra**: $20/mo (100,000 reqs/mo)

### 2. Local MCP Server (Private/Free)
- **Location**: `/mcp-server`
- **Usage**: Personal use for code analysis.
- **Cost**: Free (Runs locally).

## 🛠️ Installation & Usage

### Method A: Use via RapidAPI (For App Developers)
```python
import requests
url = "https://prometheus-text-and-code-toolkit.p.rapidapi.com/api/explain"
payload = { "code": "def hello(): pass" }
headers = {
    "x-rapidapi-key": "YOUR_API_KEY",
    "x-rapidapi-host": "prometheus-text-and-code-toolkit.p.rapidapi.com"
}
response = requests.post(url, json=payload, headers=headers)
```

### Method B: Use via MCP (For Claude/AI)
1.  Install dependencies: `pip install mcp`
2.  Add to `claude_desktop_config.json`:
    ```json
    {
      "mcpServers": {
        "prometheus": {
          "command": "python",
          "args": ["/absolute/path/to/mcp-server/server.py"]
        }
      }
    }
    ```
3.  Ask Claude: *"Analyze the complexity of this file."*

## 📂 Project Structure
```
/
├── api-service/          # Vercel Serverless Functions (The Product)
│   ├── api/explain.py    # Code Analysis Logic
│   ├── api/text.py       # Text Processing Logic
│   └── vercel.json       # Deployment Config
│
├── mcp-server/           # Local Agent Server (The Tool)
│   ├── server.py         # MCP Entry Point
│   └── utils.py          # Shared Core Algorithms
│
└── demo_antigravity.py   # Test Script for Dogfooding
```

## 📝 Maintenance
- **To Update API**: Edit `api-service/api/*.py`, then `git push`. Vercel auto-deploys.
- **To Check Revenue**: Go to [RapidAPI Provider Dashboard](https://rapidapi.com/provider/dashboard).

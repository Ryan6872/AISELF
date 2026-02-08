# Prometheus 文本与代码工具箱 (Prometheus Text & Code Toolkit)

> **高性能、零依赖的文本分析与代码解析 API**
> *现已支持 MCP (模型上下文协议)！*

![RapidAPI 上架截图](https://rapidapi.com/liaoyingg/api/prometheus-text-and-code-toolkit)

## 📖 项目概述
Prometheus 是一个为开发者和 AI 智能体设计的双用途工具箱：
1.  **面向开发者 (API)**：部署在 Vercel 上的无服务器 REST API，通过 RapidAPI 平台进行商业化销售。
2.  **面向 AI 智能体 (MCP)**：一个本地 MCP 服务器，允许 AI 模型（如 Claude, Gemini）直接分析本地代码库，无需上传数据。

## 🚀 部署与变现

### 1. 公开 API (商业版)
- **托管平台**: Vercel (Serverless Functions)
- **基础地址 (Base URL)**: `https://aiself.vercel.app/api`
- **市场链接**: [RapidAPI Listing](https://rapidapi.com/liaoyingg/api/prometheus-text-and-code-toolkit)
- **收费模式**:
    - **基础版 (Basic)**: 免费 (500 次请求/月)
    - **专业版 (Pro)**: $5/月 (10,000 次请求/月)
    - **至尊版 (Ultra)**: $20/月 (100,000 次请求/月)

### 2. 本地 MCP 服务器 (自用/免费)
- **位置**: `/mcp-server`
- **用途**: 个人代码分析
- **成本**: 免费 (本地运行)

## 🛠️ 安装与使用指南

### 方法 A: 通过 RapidAPI 使用 (适用于应用开发)
```python
import requests
url = "https://prometheus-text-and-code-toolkit.p.rapidapi.com/api/explain"
payload = { "code": "def hello(): pass" }
headers = {
    "x-rapidapi-key": "您的_API_KEY",
    "x-rapidapi-host": "prometheus-text-and-code-toolkit.p.rapidapi.com"
}
response = requests.post(url, json=payload, headers=headers)
```

### 方法 B: 通过 MCP 使用 (适用于 Claude/AI)
1.  安装依赖库: `pip install mcp`
2.  添加到 `claude_desktop_config.json` 配置文件:
    ```json
    {
      "mcpServers": {
        "prometheus": {
          "command": "python",
          "args": ["C:\\完整路径\\到\\mcp-server\\server.py"]
        }
      }
    }
    ```
3.  直接问 Claude: *"分析一下这个文件的代码复杂度。"*

## 📂 项目结构
```
/
├── api-service/          # Vercel 无服务器函数 (产品核心)
│   ├── api/explain.py    # 代码分析逻辑
│   ├── api/text.py       # 文本处理逻辑
│   └── vercel.json       # 部署配置
│
├── mcp-server/           # 本地智能体服务 (自用工具)
│   ├── server.py         # MCP 入口程序
│   └── utils.py          # 共享的核心算法
│
└── demo_antigravity.py   # 自测脚本 (Dogfooding)
```

## 📝 维护指南
- **更新 API**: 修改 `api-service/api/*.py`，然后执行 `git push`。Vercel 会自动部署。
- **查看收入**: 访问 [RapidAPI 提供者仪表盘](https://rapidapi.com/provider/dashboard)。

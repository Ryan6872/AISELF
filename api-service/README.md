# Prometheus AI Services

Project Prometheus 下的微服务集合，提供高效、零成本的文本和代码处理 API。

## 🚀 Deployed Endpoint
- Base URL: `https://aiself.vercel.app/api`

## 📦 Available APIs

### 1. Code Explainer (Enhanced)
- **Endpoint**: `/explain`
- **Method**: `POST`
- **Description**: 基于 AST (Abstract Syntax Tree) 对代码进行深度结构分析和复杂度评估。目前深度分析仅支持 Python。
- **Payload**:
  ```json
  {
    "code": "def hello(): print('world')",
    "language": "python" 
  }
  ```
- **Response**:
  ```json
  {
    "analysis": {
      "functions": [{"name": "hello", "lineno": 1, "args": []}],
      "complexity": 1
    }
  }
  ```

### 2. Text Toolkit
- **Endpoint**: `/text`
- **Method**: `POST` 
- **Description**: 多功能文本处理工具集。
- **Actions**:
  - `stats`: 统计字数、词数、阅读时间
  - `keywords`: 提取关键词 (Top N)
  - `clean`: 去除 HTML 标签、多余空格
  - `slug`: 生成 URL 友好的 slug
- **Payload**:
  ```json
  {
    "action": "stats",
    "text": "Hello world! This is a test."
  }
  ```

## 🛠️ Development

所有 API 均为 Serverless Function，部署在 Vercel 上。

### Local Test
```bash
# 需安装 Vercel CLI
vercel dev
```

### Deploy
推送到 `main` 分支自动部署。

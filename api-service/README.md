# Code Explainer API

一个将代码片段转换为带详细注释版本的API服务。

## 功能

- 自动检测编程语言
- 为每行代码添加中文/英文注释  
- 生成代码整体摘要
- 支持 Python, JavaScript, Java, C/C++ 等

## API 端点

### GET /api/explain
返回API信息和使用说明。

### POST /api/explain
解释代码并添加注释。

**请求体**:
```json
{
  "code": "def hello():\n    print('Hello World')",
  "language": "auto",
  "output_lang": "zh"
}
```

**响应**:
```json
{
  "original_code": "...",
  "explained_code": "# 定义函数\ndef hello():\n    # 输出打印\n    print('Hello World')",
  "language": "python",
  "summary": "这段python代码包含 2 行，1 个函数...",
  "line_count": 2
}
```

## 部署

### Vercel
```bash
cd api-service
vercel --prod
```

## 定价（RapidAPI）

- **Free**: 100 次/月
- **Basic** ($9.99/月): 1,000 次/月
- **Pro** ($29.99/月): 10,000 次/月

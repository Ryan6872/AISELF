# Vercel 部署指南

## 方式一：GitHub 自动部署（推荐）

### 步骤 1: 将代码推送到 GitHub
```bash
cd c:\Users\admin\.gemini\antigravity\playground\fiery-cassini\api-service
git init
git add .
git commit -m "Initial commit: Code Explainer API"
git remote add origin https://github.com/YOUR_USERNAME/code-explainer-api.git
git push -u origin main
```

### 步骤 2: 连接 Vercel
1. 访问 https://vercel.com/new
2. 选择 "Import Git Repository"
3. 选择刚才创建的仓库
4. 点击 "Deploy"

---

## 方式二：Vercel CLI 部署

### 步骤 1: 安装 Vercel CLI
```bash
npm install -g vercel
```

### 步骤 2: 登录并部署
```bash
cd c:\Users\admin\.gemini\antigravity\playground\fiery-cassini\api-service
vercel login
vercel --prod
```

---

## 部署后获取 API URL
部署成功后，您将获得类似这样的URL：
```
https://code-explainer-api-xxx.vercel.app/api/explain
```

保存此URL，用于后续在RapidAPI上架。

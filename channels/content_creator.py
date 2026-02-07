"""
Project Prometheus - 内容创作渠道模块
负责生成技术文章并管理发布流程
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# 路径配置
CHANNELS_DIR = Path(__file__).parent
CONTENT_DIR = CHANNELS_DIR / "content"
DRAFTS_DIR = CONTENT_DIR / "drafts"
PUBLISHED_DIR = CONTENT_DIR / "published"

# 确保目录存在
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)


# 文章主题策略 - 聚焦AI+开发者工具领域
TOPIC_STRATEGIES = {
    "ai_tools": {
        "name": "AI工具实战",
        "description": "介绍AI工具的实际应用场景和使用技巧",
        "platforms": ["juejin", "zhihu"],
        "examples": [
            "如何用Claude自动化你的开发工作流",
            "AI辅助代码审查：从入门到精通",
            "用AI生成单元测试的最佳实践"
        ]
    },
    "automation": {
        "name": "自动化脚本",
        "description": "分享实用的自动化脚本和工作流",
        "platforms": ["juejin", "dev.to"],
        "examples": [
            "Python自动化办公：批量处理Excel的10个技巧",
            "用Playwright实现Web自动化测试",
            "构建你的第一个GitHub Action"
        ]
    },
    "tutorials": {
        "name": "技术教程",
        "description": "深入浅出的技术教程",
        "platforms": ["juejin", "zhihu", "dev.to"],
        "examples": [
            "从零搭建现代化前端开发环境",
            "FastAPI入门：构建高性能API",
            "Docker容器化部署实战指南"
        ]
    }
}


class ArticleDraft:
    """文章草稿管理"""
    
    def __init__(
        self,
        title: str,
        topic_category: str,
        target_platforms: list[str],
        outline: Optional[list[str]] = None
    ):
        self.id = f"ART-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.title = title
        self.topic_category = topic_category
        self.target_platforms = target_platforms
        self.outline = outline or []
        self.content = ""
        self.status = "draft"
        self.created_at = datetime.now().isoformat()
        self.published_at = None
        self.metrics = {
            "views": 0,
            "likes": 0,
            "comments": 0,
            "earnings": 0
        }
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "topic_category": self.topic_category,
            "target_platforms": self.target_platforms,
            "outline": self.outline,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "published_at": self.published_at,
            "metrics": self.metrics
        }
    
    def save(self) -> Path:
        """保存草稿到文件"""
        filepath = DRAFTS_DIR / f"{self.id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return filepath
    
    @classmethod
    def load(cls, article_id: str) -> "ArticleDraft":
        """从文件加载草稿"""
        filepath = DRAFTS_DIR / f"{article_id}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        draft = cls(
            title=data["title"],
            topic_category=data["topic_category"],
            target_platforms=data["target_platforms"],
            outline=data["outline"]
        )
        draft.id = data["id"]
        draft.content = data["content"]
        draft.status = data["status"]
        draft.created_at = data["created_at"]
        draft.published_at = data.get("published_at")
        draft.metrics = data.get("metrics", draft.metrics)
        return draft


def get_topic_suggestions() -> list[dict]:
    """
    获取文章主题建议
    基于当前策略和市场趋势推荐主题
    """
    suggestions = []
    for category, strategy in TOPIC_STRATEGIES.items():
        for example in strategy["examples"]:
            suggestions.append({
                "title": example,
                "category": category,
                "platforms": strategy["platforms"],
                "priority": "medium"
            })
    return suggestions


def create_article_plan(
    title: str,
    category: str,
    platforms: list[str]
) -> ArticleDraft:
    """
    创建文章计划
    
    Args:
        title: 文章标题
        category: 主题分类
        platforms: 目标发布平台
    
    Returns:
        ArticleDraft 实例
    """
    draft = ArticleDraft(
        title=title,
        topic_category=category,
        target_platforms=platforms
    )
    draft.save()
    return draft


def list_drafts() -> list[dict]:
    """列出所有草稿"""
    drafts = []
    for filepath in DRAFTS_DIR.glob("*.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            drafts.append({
                "id": data["id"],
                "title": data["title"],
                "status": data["status"],
                "created_at": data["created_at"]
            })
    return drafts


if __name__ == "__main__":
    # 测试：显示主题建议
    import pprint
    print("=== 文章主题建议 ===")
    pprint.pprint(get_topic_suggestions())

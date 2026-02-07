"""
Project Prometheus - 账本管理模块
管理收支记录、计算ROI、追踪Token成本
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

# 路径配置
CORE_DIR = Path(__file__).parent.parent / "core"
LEDGER_PATH = CORE_DIR / "ledger.json"
CONFIG_PATH = CORE_DIR / "config.json"


def load_ledger() -> dict:
    """加载账本数据"""
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(ledger: dict) -> None:
    """保存账本数据"""
    ledger["meta"]["last_updated"] = datetime.now().isoformat()
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)


def add_transaction(
    amount: float,
    tx_type: Literal["income", "expense"],
    category: str,
    description: str,
    channel: str = "system"
) -> dict:
    """
    添加一笔交易记录
    
    Args:
        amount: 金额（正数）
        tx_type: 类型 - "income" 或 "expense"
        category: 分类（如 token_cost, platform_reward, sale 等）
        description: 描述
        channel: 来源渠道
    
    Returns:
        新创建的交易记录
    """
    ledger = load_ledger()
    
    # 生成交易ID
    tx_count = len(ledger["transactions"]) + 1
    tx_id = f"TXN-{tx_count:03d}"
    
    # 计算余额
    current_balance = ledger["summary"]["net_profit"]
    if tx_type == "income":
        new_balance = current_balance + amount
        ledger["summary"]["total_income"] += amount
    else:
        new_balance = current_balance - amount
        ledger["summary"]["total_expense"] += amount
        if category == "token_cost":
            ledger["summary"]["total_token_cost"] += amount
    
    ledger["summary"]["net_profit"] = new_balance
    
    # 创建交易记录
    transaction = {
        "id": tx_id,
        "timestamp": datetime.now().isoformat(),
        "type": tx_type,
        "category": category,
        "amount": amount,
        "description": description,
        "channel": channel,
        "balance_after": new_balance
    }
    
    ledger["transactions"].append(transaction)
    
    # 更新渠道统计
    if channel in ledger["channel_performance"]:
        perf = ledger["channel_performance"][channel]
        if tx_type == "income":
            perf["total_income"] += amount
        else:
            perf["total_expense"] += amount
        
        # 计算ROI
        if perf["total_expense"] > 0:
            perf["roi"] = (perf["total_income"] - perf["total_expense"]) / perf["total_expense"] * 100
    
    save_ledger(ledger)
    return transaction


def get_summary() -> dict:
    """获取账本摘要"""
    ledger = load_ledger()
    return {
        "summary": ledger["summary"],
        "channel_performance": ledger["channel_performance"],
        "recent_transactions": ledger["transactions"][-5:]  # 最近5笔
    }


def record_token_cost(tokens_used: int, description: str = "AI对话消耗") -> dict:
    """
    记录Token消耗成本
    
    Args:
        tokens_used: 使用的token数量
        description: 描述
    
    Returns:
        交易记录
    """
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    cost_per_1k = config["token_cost"]["estimated_per_1k_tokens_cny"]
    cost = (tokens_used / 1000) * cost_per_1k
    
    return add_transaction(
        amount=round(cost, 4),
        tx_type="expense",
        category="token_cost",
        description=f"{description} (~{tokens_used} tokens)",
        channel="system"
    )


if __name__ == "__main__":
    # 测试：显示当前摘要
    import pprint
    pprint.pprint(get_summary())

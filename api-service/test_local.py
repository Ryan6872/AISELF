"""
本地测试脚本 - 测试代码解释器API
"""
import sys
import os

# 添加api目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from api.explain import explain_code


def test_python_code():
    """测试Python代码解释"""
    code = '''
import os
from datetime import datetime

def greet(name):
    current_time = datetime.now()
    print(f"Hello, {name}! It's {current_time}")
    return True

if __name__ == "__main__":
    greet("World")
'''
    
    result = explain_code(code, "python", "zh")
    
    print("=" * 50)
    print("【原始代码】")
    print(result["original_code"])
    print("\n" + "=" * 50)
    print("【带注释代码】")
    print(result["explained_code"])
    print("\n" + "=" * 50)
    print(f"【语言】: {result['language']}")
    print(f"【摘要】: {result['summary']}")
    print(f"【行数】: {result['line_count']}")
    return result


def test_javascript_code():
    """测试JavaScript代码解释"""
    code = '''
const express = require('express');

function handleRequest(req, res) {
    if (req.method === 'GET') {
        return res.json({ message: 'Hello!' });
    }
}
'''
    
    result = explain_code(code, "auto", "en")
    
    print("\n" + "=" * 50)
    print("【JavaScript Test - English】")
    print(result["explained_code"])
    print(f"Summary: {result['summary']}")
    return result


if __name__ == "__main__":
    print("🧪 Testing Code Explainer API...\n")
    
    test_python_code()
    test_javascript_code()
    
    print("\n✅ All tests passed!")

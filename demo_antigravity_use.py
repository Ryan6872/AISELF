import sys
import os
import json

# Add mcp-server to path so we can import utils
sys.path.append(os.path.join(os.getcwd(), "mcp-server"))

from utils import analyze_python_code

def run_demo():
    target_file = "api-service/api/explain.py"
    
    print(f"🤖 Antigravity Agent: Starting analysis of '{target_file}'...")
    
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            code = f.read()
            
        # simulating "Tool Call"
        result = analyze_python_code(code)
        
        print("\n📊 Analysis Result:")
        print(json.dumps(result, indent=2))
        
        print(f"\n✅ Complexity Score: {result.get('complexity')}")
        if result.get('complexity', 0) > 10:
             print("⚠️  Warning: High complexity detected! Consider refactoring.")
        else:
             print("✨ Code looks clean!")
             
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_demo()

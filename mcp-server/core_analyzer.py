import ast
import re
from typing import Dict, Any, List

class AdvancedComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # Base complexity is 1
        self.functions = []

    def visit_FunctionDef(self, node):
        func_visitor = AdvancedComplexityVisitor()
        for child in node.body:
            func_visitor.visit(child)
        
        self.functions.append({
            "name": node.name,
            "lineno": node.lineno,
            "complexity": func_visitor.complexity,
            "args": [arg.arg for arg in node.args.args]
        })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)

    # Complexity increasers
    def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_AsyncFor(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_ExceptHandler(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_Assert(self, node): self.complexity += 1; self.generic_visit(node)
    
    # Boolean operators (and/or) increase complexity
    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec']:
                self.issues.append({
                    "severity": "CRITICAL",
                    "type": "Code Injection",
                    "message": f"Use of '{node.func.id}' detected. This is a major security risk.",
                    "lineno": node.lineno
                })
        self.generic_visit(node)

    def visit_Import(self, node):
        for name in node.names:
            if name.name in ['subprocess', 'os', 'sys']:
                self.issues.append({
                    "severity": "WARNING",
                    "type": "Dangerous Import",
                    "message": f"Import of '{name.name}' detected. Ensure inputs are sanitized.",
                    "lineno": node.lineno
                })
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module in ['subprocess', 'os', 'sys']:
             self.issues.append({
                    "severity": "WARNING",
                    "type": "Dangerous Import",
                    "message": f"Import from '{node.module}' detected.",
                    "lineno": node.lineno
                })
        self.generic_visit(node)

class StructureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "classes": [],
            "imports": [],
        }

    def visit_ClassDef(self, node):
        self.stats["classes"].append({
            "name": node.name,
            "lineno": node.lineno,
            "bases": [base.id for base in node.bases if isinstance(base, ast.Name)]
        })
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.stats["imports"].append(node.module)
        self.generic_visit(node)

def analyze_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
        
        # 1. Complexity Analysis
        complexity_visitor = AdvancedComplexityVisitor()
        complexity_visitor.visit(tree)
        
        # 2. Security Analysis
        security_visitor = SecurityVisitor()
        security_visitor.visit(tree)
        
        # 3. Structure Analysis
        structure_visitor = StructureVisitor()
        structure_visitor.visit(tree)
        
        # 4. Global Stats
        total_complexity = complexity_visitor.complexity
        functions = complexity_visitor.functions
        
        # Calculate Maintainability (Simple Heuristic for now)
        # 100 base, minus complexity * 2, len * 0.1
        lines = len(code.splitlines())
        maintainability = max(0, 100 - (total_complexity * 1.5) - (lines * 0.05))

        return {
            "metrics": {
                "complexity": total_complexity,
                "maintainability_index": round(maintainability, 2),
                "loc": lines
            },
            "security": {
                "issues": security_visitor.issues,
                "score": 100 - (len(security_visitor.issues) * 10)
            },
            "structure": {
                "functions": functions,
                "classes": structure_visitor.stats["classes"],
                "imports": structure_visitor.stats["imports"]
            }
        }
    except SyntaxError as e:
        return {"error": f"Syntax error at line {e.lineno}: {e.msg}"}
    except Exception as e:
        return {"error": str(e)}

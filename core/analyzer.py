import ast
import re

class CodeAnalyzer:
    def __init__(self, code):
        self.code = code
        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def calculate_halstead_metrics(self):
        """
        Estimates the 'Mental Effort' required to write the code.
        High effort in AI code suggests 'over-engineering'.
        """
        if not self.tree: return "Syntax Error"
        
        operators = set()
        operands = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.And, ast.Or)):
                operators.add(type(node))
            elif isinstance(node, (ast.Name, ast.Constant)):
                operands.add(str(node))
        
        # Simple version of Halstead Volume
        n1, n2 = len(operators), len(operands)
        volume = (n1 + n2) * (n1 + n2).bit_length() # Approximate
        return {"vocabulary": n1 + n2, "volume": round(volume, 2)}

    def detect_bad_practices(self):
        """
        Finds patterns often missed by standard linters but common in LLM outputs.
        """
        findings = []
        
        # 1. Check for Hardcoded Secrets (Basic Regex)
        if re.search(r'(api_key|password|secret|token)\s*=\s*["\'][a-zA-Z0-9]{8,}["\']', self.code):
            findings.append("Potential hardcoded credential detected.")

        # 2. Check for 'Ghost' Comments
        # LLMs often leave placeholders like '# Add logic here'
        if re.search(r'#.*(TODO|FIXME|logic here|insert here)', self.code, re.I):
            findings.append("Unfinished placeholder/TODO found.")

        # 3. Import Efficiency
        imports = [node.names[0].name for node in ast.walk(self.tree) if isinstance(node, ast.Import)]
        if len(set(imports)) != len(imports):
            findings.append("Duplicate imports detected.")

        return findings

    def get_docstring_coverage(self):
        """
        Measures if the code is actually explained. 
        AI code is often verbose but lacks meaningful documentation.
        """
        if not self.tree: return 0
        
        functions = [n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        if not functions: return 100.0
        
        documented = sum(1 for n in functions if ast.get_docstring(n))
        return round((documented / len(functions)) * 100, 2)

# --- Integration Example ---
if __name__ == "__main__":
    sample_code = """
import os
import os # Duplicate!

def solve():
    # TODO: Add logic here
    api_key = "AIZA_fake_key_123"
    return "Hello World"
    """
    analyzer = CodeAnalyzer(sample_code)
    print("--- Analysis Results ---")
    print(f"Halstead Metrics: {analyzer.calculate_halstead_metrics()}")
    print(f"Bad Practices: {analyzer.detect_bad_practices()}")
    print(f"Docstring Coverage: {analyzer.get_docstring_coverage()}%")
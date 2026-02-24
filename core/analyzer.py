import ast
import re

class CodeAnalyzer:
    """
    A static analysis tool that parses Python code into an Abstract Syntax Tree (AST)
    to calculate complexity metrics and detect non-standard coding patterns.
    """

    def __init__(self, code):
        """
        Initializes the analyzer by parsing source code into an AST.

        Args:
            code (str): The Python source code to be analyzed.
        """
        self.code = code
        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def calculate_halstead_metrics(self):
        """
        Estimates the 'Mental Effort' and 'Volume' required to write the code.
        High volume in AI-generated code often suggests over-engineering.

        Returns:
            dict: A dictionary containing 'vocabulary' and 'volume', or a string error.
        """
        if not self.tree: return "Syntax Error"
        
        operators = set()
        operands = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.And, ast.Or)):
                operators.add(type(node))
            elif isinstance(node, (ast.Name, ast.Constant)):
                operands.add(str(node))
        
        n1, n2 = len(operators), len(operands)
        volume = (n1 + n2) * (n1 + n2).bit_length()
        return {"vocabulary": n1 + n2, "volume": round(volume, 2)}

    def detect_bad_practices(self):
        """
        Identifies patterns common in LLM outputs, such as hardcoded secrets,
        placeholder comments, and duplicate imports.

        Returns:
            list: A list of strings describing detected issues.
        """
        findings = []
        
        # 1. Check for Hardcoded Secrets
        if re.search(r'(api_key|password|secret|token)\s*=\s*["\'][a-zA-Z0-9]{8,}["\']', self.code):
            findings.append("Potential hardcoded credential detected.")

        # 2. Check for Placeholder Comments
        if re.search(r'#.*(TODO|FIXME|logic here|insert here)', self.code, re.I):
            findings.append("Unfinished placeholder/TODO found.")

        # 3. Import Efficiency
        if self.tree:
            imports = [node.names[0].name for node in ast.walk(self.tree) if isinstance(node, ast.Import)]
            if len(set(imports)) != len(imports):
                findings.append("Duplicate imports detected.")

        return findings

    def get_docstring_coverage(self):
        """
        Calculates the percentage of functions and classes that contain docstrings.

        Returns:
            float: Coverage percentage (0.0 to 100.0).
        """
        if not self.tree: return 0.0
        
        functions = [n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        if not functions: return 100.0
        
        documented = sum(1 for n in functions if ast.get_docstring(n))
        return round((documented / len(functions)) * 100, 2)
import ast
import re
import math
from collections import Counter


class CodeAnalyzer:
    """
    A static analysis tool that parses Python code into an Abstract Syntax Tree (AST)
    to calculate complexity metrics and detect non-standard coding patterns.
    """

    OPERATOR_NODES = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
        ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift, ast.Invert,
        ast.And, ast.Or, ast.Not,
        ast.UAdd, ast.USub,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn
    )

    def __init__(self, code):
        self.code = code
        try:
            self.tree = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def calculate_halstead_metrics(self):
        if not self.tree:
            return "Syntax Error"

        operator_counts = Counter()
        operand_counts = Counter()

        for node in ast.walk(self.tree):
            if isinstance(node, self.OPERATOR_NODES):
                operator_counts[type(node).__name__] += 1
            elif isinstance(node, ast.Name):
                operand_counts[node.id] += 1
            elif isinstance(node, ast.Constant):
                operand_counts[repr(node.value)] += 1

        n1 = len(operator_counts)
        n2 = len(operand_counts)
        N1 = sum(operator_counts.values())
        N2 = sum(operand_counts.values())

        vocabulary = n1 + n2
        length = N1 + N2
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0

        return {
            "n1": n1,
            "n2": n2,
            "N1": N1,
            "N2": N2,
            "vocabulary": vocabulary,
            "volume": round(volume, 2)
        }

    def detect_bad_practices(self):
        findings = []

        if re.search(
            r'(api_key|password|secret|token)\s*=\s*["\'][\w]{8,}["\']',
            self.code
        ):
            findings.append("Potential hardcoded credential detected.")

        if re.search(r'#.*(TODO|FIXME|logic here|insert here)', self.code, re.I):
            findings.append("Unfinished placeholder/TODO found.")

        if re.search(r'^\s*#\s*$', self.code, re.MULTILINE):
            findings.append("Ghost comment (empty # symbol) detected.")

        if self.tree:
            imports = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.extend(alias.name for alias in node.names)
            if len(set(imports)) != len(imports):
                findings.append("Duplicate imports detected.")

        return findings

    def get_docstring_coverage(self):
        if not self.tree:
            return 0.0

        functions = [
            n for n in ast.walk(self.tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]

        if not functions:
            return None

        documented = sum(1 for n in functions if ast.get_docstring(n))
        return round((documented / len(functions)) * 100, 2)
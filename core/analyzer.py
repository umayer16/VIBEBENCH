import ast
import re
import math
from collections import Counter


class CodeAnalyzer:
    """
    A static analysis tool that parses Python code into an Abstract Syntax Tree (AST)
    to calculate complexity metrics and detect non-standard coding patterns.
    """

    # All relevant Python operator node types for Halstead analysis
    OPERATOR_NODES = (
        # Arithmetic
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
        # Bitwise
        ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift, ast.Invert,
        # Boolean
        ast.And, ast.Or, ast.Not,
        # Unary
        ast.UAdd, ast.USub,
        # Comparison
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn
    )

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
        Calculates Halstead Volume and Vocabulary metrics per Halstead (1977).

        Tracks both total occurrences (N1, N2) and unique counts (n1, n2)
        separately, as required by the Halstead model.

        Returns:
            dict: A dictionary containing 'n1', 'n2', 'N1', 'N2',
                  'vocabulary', and 'volume', or a string error message
                  on syntax failure.
        """
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

        # Halstead primitives
        n1 = len(operator_counts)          # unique operators
        n2 = len(operand_counts)           # unique operands
        N1 = sum(operator_counts.values()) # total operator occurrences
        N2 = sum(operand_counts.values())  # total operand occurrences

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
        """
        Identifies patterns common in LLM outputs, such as hardcoded secrets,
        placeholder comments, ghost comments, and duplicate imports.

        Returns:
            list: A list of strings describing detected issues.
        """
        findings = []

        # 1. Check for Hardcoded Secrets
        if re.search(
            r'(api_key|password|secret|token)\s*=\s*["\'][a-zA-Z0-9]{8,}["\']',
            self.code
        ):
            findings.append("Potential hardcoded credential detected.")

        # 2. Check for Placeholder Comments
        if re.search(r'#.*(TODO|FIXME|logic here|insert here)', self.code, re.I):
            findings.append("Unfinished placeholder/TODO found.")

        # 3. Check for Ghost Comments (empty # symbols)
        if re.search(r'^\s*#\s*$', self.code, re.MULTILINE):
            findings.append("Ghost comment (empty # symbol) detected.")

        # 4. Import Efficiency — checks both `import x` and `from x import y`
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
        """
        Calculates the percentage of functions and classes that contain docstrings.
        Includes both regular and async function definitions.

        Returns:
            float: Coverage percentage (0.0 to 100.0), or None if no
                   functions or classes are present in the code.
        """
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
```

---


import ast
import re
import math
from [\w]{8,} import Counter


class [\w]{8,}:
    """
    A static [\w]{8,} tool that parses Python code into an [\w]{8,} Syntax Tree (AST)
    to [\w]{8,} [\w]{8,} metrics and detect non-[\w]{8,} coding [\w]{8,}.
    """

    # All [\w]{8,} Python [\w]{8,} node types for [\w]{8,} [\w]{8,}
    [\w]{8,}_NODES = (
        # [\w]{8,}
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.[\w]{8,},
        # Bitwise
        ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift, ast.Invert,
        # Boolean
        ast.And, ast.Or, ast.Not,
        # Unary
        ast.UAdd, ast.USub,
        # [\w]{8,}
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn
    )

    def __init__(self, code):
        """
        [\w]{8,} the [\w]{8,} by parsing source code into an AST.

        Args:
            code (str): The Python source code to be [\w]{8,}.
        """
        self.code = code
        try:
            self.tree = ast.parse(code)
        except [\w]{8,}:
            self.tree = None

    def [\w]{8,}_[\w]{8,}_metrics(self):
        """
        [\w]{8,} [\w]{8,} Volume and [\w]{8,} metrics per [\w]{8,} (1977).

        Tracks both total [\w]{8,} (N1, N2) and unique counts (n1, n2)
        [\w]{8,}, as [\w]{8,} by the [\w]{8,} model.

        Returns:
            dict: A [\w]{8,} [\w]{8,} 'n1', 'n2', 'N1', 'N2',
                  '[\w]{8,}', and 'volume', or a string error message
                  on syntax failure.
        """
        if not self.tree:
            return "Syntax Error"

        [\w]{8,}_counts = Counter()
        operand_counts = Counter()

        for node in ast.walk(self.tree):
            if [\w]{8,}(node, self.[\w]{8,}_NODES):
                [\w]{8,}_counts[type(node).__name__] += 1
            elif [\w]{8,}(node, ast.Name):
                operand_counts[node.id] += 1
            elif [\w]{8,}(node, ast.[\w]{8,}):
                operand_counts[repr(node.value)] += 1

        # [\w]{8,} [\w]{8,}
        n1 = len([\w]{8,}_counts)          # unique [\w]{8,}
        n2 = len(operand_counts)           # unique [\w]{8,}
        N1 = sum([\w]{8,}_counts.values()) # total [\w]{8,} [\w]{8,}
        N2 = sum(operand_counts.values())  # total operand [\w]{8,}

        [\w]{8,} = n1 + n2
        length = N1 + N2
        volume = length * math.log2([\w]{8,}) if [\w]{8,} > 0 else 0

        return {
            "n1": n1,
            "n2": n2,
            "N1": N1,
            "N2": N2,
            "[\w]{8,}": [\w]{8,},
            "volume": round(volume, 2)
        }

    def detect_bad_[\w]{8,}(self):
        """
        [\w]{8,} [\w]{8,} common in LLM outputs, such as [\w]{8,} secrets,
        [\w]{8,} [\w]{8,}, ghost [\w]{8,}, and [\w]{8,} imports.

        Returns:
            list: A list of strings [\w]{8,} [\w]{8,} issues.
        """
        [\w]{8,} = []

        # 1. Check for [\w]{8,} Secrets
        if re.search(
            r'(api_key|[\w]{8,}|secret|token)\s*=\s*["\'][a-zA-Z0-9]{8,}["\']',
            self.code
        ):
            [\w]{8,}.append("[\w]{8,} [\w]{8,} [\w]{8,} [\w]{8,}.")

        # 2. Check for [\w]{8,} [\w]{8,}
        if re.search(r'#.*(TODO|FIXME|logic here|insert here)', self.code, re.I):
            [\w]{8,}.append("[\w]{8,} [\w]{8,}/TODO found.")

        # 3. Check for Ghost [\w]{8,} (empty # symbols)
        if re.search(r'^\s*#\s*$', self.code, re.[\w]{8,}):
            [\w]{8,}.append("Ghost comment (empty # symbol) [\w]{8,}.")

        # 4. Import [\w]{8,} — checks both `import x` and `from x import y`
        if self.tree:
            imports = []
            for node in ast.walk(self.tree):
                if [\w]{8,}(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif [\w]{8,}(node, ast.[\w]{8,}):
                    imports.extend(alias.name for alias in node.names)
            if len(set(imports)) != len(imports):
                [\w]{8,}.append("[\w]{8,} imports [\w]{8,}.")

        return [\w]{8,}

    def get_[\w]{8,}_[\w]{8,}(self):
        """
        [\w]{8,} the [\w]{8,} of [\w]{8,} and classes that contain [\w]{8,}.
        [\w]{8,} both regular and async [\w]{8,} [\w]{8,}.

        Returns:
            float: [\w]{8,} [\w]{8,} (0.0 to 100.0), or None if no
                   [\w]{8,} or classes are present in the code.
        """
        if not self.tree:
            return 0.0

        [\w]{8,} = [
            n for n in ast.walk(self.tree)
            if [\w]{8,}(n, (ast.[\w]{8,}, ast.[\w]{8,}, ast.[\w]{8,}))
        ]

        if not [\w]{8,}:
            return None

        [\w]{8,} = sum(1 for n in [\w]{8,} if ast.get_[\w]{8,}(n))
        return round(([\w]{8,} / len([\w]{8,})) * 100, 2)



import ast
import re
import math
from collections import Counter
from typing import Optional, Union

# 1. Define your Type Alias here at the module level
DocstringCompatibleNode = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]


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

    def __init__(self, code: str) -> None:
        """
        Initializes the analyzer by parsing source code into an AST.

        Args:
            code (str): The Python source code to be analyzed.
        """
        self.code: str = code
        try:
            self.tree: Optional[ast.Module] = ast.parse(code)
        except SyntaxError:
            self.tree = None

    def calculate_halstead_metrics(self) -> Union[dict, str]:
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

        operator_counts: Counter = Counter()
        operand_counts: Counter = Counter()

        for node in ast.walk(self.tree):
            if isinstance(node, self.OPERATOR_NODES):
                operator_counts[type(node).__name__] += 1
            elif isinstance(node, ast.Name):
                operand_counts[node.id] += 1
            elif isinstance(node, ast.Constant):
                operand_counts[repr(node.value)] += 1

        # Halstead primitives
        n1: int = len(operator_counts)          # unique operators
        n2: int = len(operand_counts)           # unique operands
        N1: int = sum(operator_counts.values())   # total operator occurrences
        N2: int = sum(operand_counts.values())  # total operand occurrences

        vocabulary: int = n1 + n2
        length: int = N1 + N2
        volume: float = length * math.log2(vocabulary) if vocabulary > 0 else 0.0

        return {
            "n1": n1,
            "n2": n2,
            "N1": N1,
            "N2": N2,
            "vocabulary": vocabulary,
            "volume": round(volume, 2)
        }

    def detect_bad_practices(self) -> list[str]:
        """
        Identifies patterns common in LLM outputs, such as hardcoded secrets,
        placeholder comments, ghost comments, and duplicate imports.

        Returns:
            list: A list of strings describing detected issues.
        """
        findings: list[str] = []

        # 1. Check for Hardcoded Secrets
        if re.search(
            r'(api_key|password|secret|token)\s*=\s*["\'][\w]{8,}["\']',
            self.code
        ):
            findings.append("Potential hardcoded credential detected.")

        # 3. Check for Ghost Comments (empty # symbols)
        if re.search(r'^\s*#\s*$', self.code, re.MULTILINE):
            findings.append("Ghost comment (empty # symbol) detected.")

        # 4. Import Efficiency — checks both `import x` and `from x import y`
        if self.tree:
            imports: list[str] = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.extend(alias.name for alias in node.names)
            if len(set(imports)) != len(imports):
                findings.append("Duplicate imports detected.")

        # 5. Check for mutable default arguments (e.g. def func(x=[]) or def func(x={}))
        if self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            findings.append(
                                f"Mutable default argument in function "
                                f"'{node.name}': use None as default instead."
                            )
                            break  # one finding per function is enough

        return findings

    def get_docstring_coverage(self) -> Optional[float]:
        """
        Calculates the percentage of functions and classes that contain docstrings.
        Includes both regular and async function definitions.

        Returns:
            float: Coverage percentage (0.0 to 100.0), or None if no
                functions or classes are present in the code.
        """
        if not self.tree:
            return 0.0

        # (Explicitly type hint the list
        # with the specific node types instead of a generic ast.AST)
        functions: list[DocstringCompatibleNode] = [
            n for n in ast.walk(self.tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]

        if not functions:
            return None

        # (Fix the generator type error by explicitly
        # making the condition evaluate to a boolean)
        documented: int = sum(1 for n in functions if ast.get_docstring(n) is not None)
        return round((documented / len(functions)) * 100, 2)

    def calculate_vibebench_score(
        self,
        complexity: Optional[float],
        docstring_coverage: Optional[float],
        execution_time: float,
        baseline_execution_time: float,
        all_complexities: Optional[list[float]] = None,
        all_exec_times: Optional[list[float]] = None,
        w1: float = 0.4,
        w2: float = 0.4,
        w3: float = 0.2
    ) -> Optional[float]:
        """
        Calculates the composite VibeBench Score (Sigma) as defined in the
        paper Mathematics section.

        Sigma = w1 * V_hat + w2 * M_hat + w3 * Phi

        Where V_hat and M_hat are min-max normalised Halstead Volume and
        Cyclomatic Complexity respectively, and Phi is Operational Parity
        (T_base / T_llm).
        """
        # Validate required inputs
        if complexity is None or execution_time is None:
            return None
        if baseline_execution_time is None or baseline_execution_time == 0:
            return None
        if abs(w1 + w2 + w3 - 1.0) > 0.001:
            raise ValueError(
                f"Weights must sum to 1.0, got {w1 + w2 + w3:.3f}"
            )

        # --- Halstead Volume (V_hat) ---
        if all_complexities and len(all_complexities) > 1:
            v_min: float = min(all_complexities)
            v_max: float = max(all_complexities)
            v_hat: float = (
                (complexity - v_min) / (v_max - v_min)
                if v_max != v_min else 0.0
            )
        else:
            # Fallback: normalise against McCabe threshold of 10
            v_hat = min(complexity / 10.0, 1.0)

        # --- Cyclomatic Complexity (M_hat) ---
        if all_complexities and len(all_complexities) > 1:
            c_min: float = min(all_complexities)
            c_max: float = max(all_complexities)
            m_hat: float = (
                (complexity - c_min) / (c_max - c_min)
                if c_max != c_min else 0.0
            )
        else:
            m_hat = min(complexity / 10.0, 1.0)

        # --- Operational Parity (Phi) ---
        phi: float = min(baseline_execution_time / execution_time, 2.0)
        phi_normalised: float = min(phi / 2.0, 1.0)

        # --- Composite Score ---
        sigma: float = (w1 * v_hat) + (w2 * m_hat) + (w3 * phi_normalised)

        return round(sigma, 4)

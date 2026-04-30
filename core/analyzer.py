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
            r'(api_key|password|secret|token)\s*=\s*["\'][\w]{8,}["\']',
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

    def calculate_vibebench_score(
        self,
        complexity,
        docstring_coverage,
        execution_time,
        baseline_execution_time,
        all_complexities=None,
        all_exec_times=None,
        w1=0.4,
        w2=0.4,
        w3=0.2
    ):
        """
        Calculates the composite VibeBench Score (Sigma) as defined in the
        paper Mathematics section.

        Sigma = w1 * V_hat + w2 * M_hat + w3 * Phi

        Where V_hat and M_hat are min-max normalised Halstead Volume and
        Cyclomatic Complexity respectively, and Phi is Operational Parity
        (T_base / T_llm).

        Args:
            complexity (float): Cyclomatic complexity of the file (M).
            docstring_coverage (float): Docstring coverage 0-100.
            execution_time (float): Execution time of this file in seconds.
            baseline_execution_time (float): Execution time of human 
                baseline in seconds.
            all_complexities (list): All complexity values in the benchmark
                run, used for min-max normalisation. If None, normalisation
                is skipped and raw value used.
            all_exec_times (list): All execution times in the benchmark run,
                used for min-max normalisation. If None, skipped.
            w1 (float): Weight for Halstead Volume component (default 0.4).
            w2 (float): Weight for Cyclomatic Complexity component 
                (default 0.4).
            w3 (float): Weight for Operational Parity component 
                (default 0.2).

        Returns:
            float: VibeBench Score between 0.0 and 1.0, or None if
                inputs are insufficient to calculate.
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
        # Use Halstead volume from the AST if available, else use 0
        halstead = self.calculate_halstead_metrics()
        if isinstance(halstead, dict):
            volume = halstead.get("volume", 0)
        else:
            volume = 0

        # Min-max normalise volume
        if all_complexities and len(all_complexities) > 1:

            v_min = min(all_complexities)
            v_max = max(all_complexities)
            v_hat = ((complexity - v_min) / (v_max - v_min)
                    if v_max != v_min else 0.0)
        else:
            # Fallback: normalise against McCabe threshold of 10
            v_hat = min(complexity / 10.0, 1.0)

        # --- Cyclomatic Complexity (M_hat) ---
        if all_complexities and len(all_complexities) > 1:
            c_min = min(all_complexities)
            c_max = max(all_complexities)
            m_hat = ((complexity - c_min) / (c_max - c_min)
                    if c_max != c_min else 0.0)
        else:
            m_hat = min(complexity / 10.0, 1.0)

        # --- Operational Parity (Phi) ---
        # Phi = T_base / T_llm
        # Phi close to 1 = good parity. Phi > 1 = LLM is slower.
        # Cap at 2.0 to prevent outliers dominating the score.
        phi = min(baseline_execution_time / execution_time, 2.0)
        # Normalise Phi to 0-1 range (1.0 = perfect parity or faster)
        phi_normalised = min(phi / 2.0, 1.0)

        # --- Composite Score ---
        sigma = (w1 * v_hat) + (w2 * m_hat) + (w3 * phi_normalised)

        return round(sigma, 4)

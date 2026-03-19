import os
import json
from datetime import datetime
from core.executor import CodeExecutor
from core.analyzer import CodeAnalyzer
from core.reporter import VibeReporter  # FIX #22: import at top level
from radon.complexity import cc_visit

SCHEMA_VERSION = "1.1"


class VibeBench:
    """
    The main orchestration framework for VibeBench.

    This class manages the lifecycle of code analysis, from walking through
    model-generated datasets to executing code in a sandboxed environment
    and generating consolidated performance reports.
    """

    def __init__(self, root_dir, verbose=False):
        """
        Initializes the benchmarking suite with a root directory for datasets.

        Args:
            root_dir (str): Path to the directory containing model subfolders
                            (e.g., 'datasets/').
            verbose (bool): If True, print per-file metric details during the run.
        """
        self.root_dir = root_dir
        self.verbose = verbose
        self.results = []
        self.executor = CodeExecutor(timeout=5)

    def get_complexity(self, code):
        """
        Calculates cyclomatic complexity using the radon library.

        Args:
            code (str): The Python source code to analyze.

        Returns:
            float: The average complexity of all code blocks, rounded to two
                   decimal places. Returns None on error.
        """
        try:
            blocks = cc_visit(code)
            return round(sum(b.complexity for b in blocks) / len(blocks), 2) if blocks else 0
        except Exception:
            return None

    def _print_verbose(self, record):
        """
        Prints per-file metric details to stdout in verbose mode.

        Args:
            record (dict): A single benchmark result record.
        """
        exec_time = record["execution_time_sec"]
        exec_time_str = f"{exec_time:.3f}s" if isinstance(exec_time, (int, float)) else "N/A"

        doc_cov = record["docstring_coverage"]
        doc_cov_str = f"{doc_cov:.1f}%" if isinstance(doc_cov, (int, float)) else "N/A"

        complexity = record["complexity"]
        complexity_str = str(complexity) if complexity is not None else "N/A"

        print(f"  Complexity      : {complexity_str}")
        print(f"  Docstring Cover : {doc_cov_str}")
        print(f"  Bad Practices   : {record['bad_practices_count']}")
        print(f"  Execution Time  : {exec_time_str}")
        print(f"  Status          : {record['status']}")
        print()

    def run_benchmark(self):
        """
        Executes the multi-model analysis by iterating through the dataset directory.

        Specifically identifies 'human_samples' as the Benchmark Reference Data
        (Gold Standard) to ensure comparative integrity against LLM outputs.
        """
        print(f"🚀 Starting Multi-Model Analysis on: {self.root_dir}\n")

        for root, dirs, files in os.walk(self.root_dir):
            folder_name = os.path.basename(root)

            # Skip the root folder itself
            if root == self.root_dir:
                continue

            # Formalizing the Human Baseline label
            is_baseline = folder_name == "human_samples"
            model_label = "HUMAN_BASELINE (Reference)" if is_baseline else folder_name.upper()

            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)
                    print(f"[{model_label}] Analyzing {filename}...")

                    with open(path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    # Dynamic Execution in sandboxed environment
                    exec_metrics = self.executor.run(path)

                    # Static Analysis using the core Analyzer
                    analyzer = CodeAnalyzer(code)

                    # Use None instead of "Error" for missing numeric fields (#24)
                    raw_exec_time = exec_metrics.get("execution_time")
                    execution_time_sec = raw_exec_time if isinstance(raw_exec_time, (int, float)) else None

                    doc_coverage = analyzer.get_docstring_coverage()

                    record = {
                        "schema_version": SCHEMA_VERSION,
                        "model": folder_name,
                        "category": "Benchmark Reference" if is_baseline else "AI Synthesis",
                        "file": filename,
                        "complexity": self.get_complexity(code),
                        "docstring_coverage": doc_coverage,
                        "bad_practices_count": len(analyzer.detect_bad_practices()),
                        "execution_time_sec": execution_time_sec,
                        "status": exec_metrics.get("status"),
                        "timestamp": datetime.now().isoformat()
                    }

                    # Print per-file details if --verbose is set (#23)
                    if self.verbose:
                        self._print_verbose(record)

                    self.results.append(record)

        self.save_report()

    def save_report(self):
        """
        Serializes the benchmark results into a timestamped JSON report and
        automatically generates the leaderboard markdown via VibeReporter.

        Fixes #22: previously the leaderboard had to be generated manually
        by running core/reporter.py as a separate step.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_name = f"vibebench_multimodel_{timestamp}.json"

        with open(report_name, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)

        print(f"\n✅ Benchmark Complete. Report saved: {report_name}")

        # FIX #22: auto-generate the leaderboard immediately after saving
        try:
            reporter = VibeReporter(report_name)
            reporter.generate_markdown()
        except Exception as e:
            print(f"⚠️  Leaderboard generation failed: {e}")
            print(f"   You can generate it manually: python core/reporter.py")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="vibebench",
        description="VibeBench: Holistic evaluation of LLM-generated code."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- analyze command ---
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Run static analysis on a single Python file."
    )
    analyze_parser.add_argument(
        "--input",
        required=True,
        metavar="FILE",
        help="Path to the Python file to analyze."
    )
    analyze_parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Path to save JSON results (optional, prints to stdout if omitted)."
    )

    # --- benchmark command ---
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Run the full multi-model benchmark suite."
    )
    benchmark_parser.add_argument(
        "--tasks",
        required=True,
        metavar="FILE",
        help="Path to the tasks JSON file (e.g. datasets/prompts.json)."
    )
    benchmark_parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Path to save benchmark results JSON (optional)."
    )
    benchmark_parser.add_argument(
        "--models",
        nargs="+",
        metavar="MODEL",
        default=None,
        help="Space-separated list of models to benchmark (e.g. gpt-4o gemini-1.5-pro)."
    )
    benchmark_parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print per-file metric details (complexity, docstring coverage, "
             "bad practices, execution time, status) during the benchmark run."
    )

    args = parser.parse_args()

    if args.command == "analyze":
        with open(args.input, "r") as f:
            code = f.read()

        analyzer = CodeAnalyzer(code)
        results = {
            "schema_version": SCHEMA_VERSION,
            "file": args.input,
            "halstead_metrics": analyzer.calculate_halstead_metrics(),
            "docstring_coverage": analyzer.get_docstring_coverage(),
            "bad_practices": analyzer.detect_bad_practices()
        }

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2))

    elif args.command == "benchmark":
        datasets_dir = os.path.dirname(args.tasks)
        bench = VibeBench(root_dir=datasets_dir, verbose=args.verbose)
        bench.run_benchmark()


if __name__ == "__main__":
    main()

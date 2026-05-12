import os
import json
from datetime import datetime
from core.executor import CodeExecutor
from core.analyzer import CodeAnalyzer
from core.reporter import VibeReporter
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
            verbose (bool): If True,
            print per-file metric details during the run.
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
            return round(
                sum(b.complexity for b in blocks) / len(blocks), 2
            ) if blocks else 0
        except Exception:
            return None

    def _print_verbose(self, record):
        """
        Prints per-file metric details to stdout in verbose mode.

        Args:
            record(dict): A single 
            benchmark result record.
        """
        exec_time = record["execution_time_sec"]
        exec_time_str = (
            f"{exec_time:.3f}s" if isinstance(exec_time, (int, float)) else "N/A"
        )

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

    def run_benchmark(self, export_csv=False):
        """
        Executes the multi-model analysis by iterating through the dataset directory.

        Specifically identifies 'human_samples' as the Benchmark Reference Data
        (Gold Standard) to ensure comparative integrity against LLM outputs.

        Args:
            export_csv (bool): If True, also export results as a CSV file.
        """
        print(f"🚀 Starting Multi-Model Analysis on: {self.root_dir}\n")

        # Pre-scan baseline directory to collect execution times per task.
        # These are used later to calculate the VibeBench Score (Phi component).
        baseline_times = {}
        baseline_dir = os.path.join(self.root_dir, "human_samples")
        if os.path.exists(baseline_dir):
            for fname in os.listdir(baseline_dir):
                if fname.endswith(".py"):
                    fpath = os.path.join(baseline_dir, fname)
                    baseline_metrics = self.executor.run(fpath)
                    bt = baseline_metrics.get("execution_time")
                    if isinstance(bt, (int, float)):
                        # Key by task ID: e.g. "TASK-001" from "TASK-001_manual.py"
                        task_id = fname.split("_")[0].upper()
                        baseline_times[task_id] = bt

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

                    # Use None instead of "Error" for missing numeric fields
                    raw_exec_time = exec_metrics.get("execution_time")
                    is_valid_time = isinstance(raw_exec_time, (int, float))
                    execution_time_sec = raw_exec_time if is_valid_time else None
                    doc_coverage = analyzer.get_docstring_coverage()

                    # Extract task ID from filename for baseline lookup
                    # e.g. "TASK-001" from "TASK-001_chatgpt.py"
                    task_id = filename.split("_")[0].upper()
                    baseline_time = baseline_times.get(task_id)

                    # Calculate composite VibeBench Score (Sigma)
                    vibebench_score = None
                    if execution_time_sec is not None and baseline_time is not None:
                        vibebench_score = analyzer.calculate_vibebench_score(
                            complexity=self.get_complexity(code),
                            docstring_coverage=doc_coverage,
                            execution_time=execution_time_sec,
                            baseline_execution_time=baseline_time
                        )

                    record = {
                        "schema_version": SCHEMA_VERSION,
                        "model": folder_name,
                        "category": "Benchmark Reference" if is_baseline else "AI Synthesis",
                        "file": filename,
                        "complexity": self.get_complexity(code),
                        "docstring_coverage": doc_coverage,
                        "bad_practices_count": len(analyzer.detect_bad_practices()),
                        "execution_time_sec": execution_time_sec,
                        "vibebench_score": vibebench_score,
                        "status": exec_metrics.get("status"),
                        "timestamp": datetime.now().isoformat()
                    }

                    # Print per-file details if --verbose is set
                    if self.verbose:
                        self._print_verbose(record)

                    self.results.append(record)

        self.save_report(export_csv=export_csv)

    def save_report(self, export_csv=False):
        """
        Serializes benchmark results to a timestamped JSON report and
        optionally exports a CSV file for analysis in external tools.

        Args:
            export_csv (bool): If True, also write results to a .csv file.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_name = f"vibebench_multimodel_{timestamp}.json"

        with open(report_name, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)

        print(f"\n✅ Benchmark Complete. Report saved: {report_name}")

        # Optional CSV export
        if export_csv:
            try:
                import pandas as pd
                csv_name = report_name.replace('.json', '.csv')
                df = pd.DataFrame(self.results)
                df.to_csv(csv_name, index=False, encoding='utf-8')
                print(f"📊 CSV export saved: {csv_name}")
            except ImportError:
                print("⚠️  pandas not installed. Run: pip install pandas")
            except Exception as e:
                print(f"⚠️  CSV export failed: {e}")

        # Auto-generate leaderboard immediately after saving
        try:
            reporter = VibeReporter(report_name)
            reporter.generate_markdown()
        except Exception as e:
            print(f"⚠️  Leaderboard generation failed: {e}")
            print("   You can generate it manually: python core/reporter.py")


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

    # --- report command ---
    report_parser = subparsers.add_parser(
        "report",
        help="Generate reports from an existing benchmark JSON file."
    )
    report_parser.add_argument(
        "--input",
        required=True,
        metavar="FILE",
        help="Path to a benchmark JSON file."
    )
    report_parser.add_argument(
        "--leaderboard",
        action="store_true",
        default=False,
        help="Generate the markdown leaderboard."
    )
    report_parser.add_argument(
        "--significance",
        action="store_true",
        default=False,
        help="Generate pairwise statistical significance report."
    )
    report_parser.add_argument(
        "--output-dir",
        metavar="DIR",
        default=".",
        help="Directory to write report files (default: current directory)."
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
        "--export-csv",
        action="store_true",
        default=False,
        help="Also export benchmark results as a CSV file alongside the JSON output."
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
        bench.run_benchmark(export_csv=args.export_csv)
    elif args.command == "report":
        reporter = VibeReporter(args.input)
        if args.leaderboard:
            output_path = os.path.join(
                args.output_dir, "VibeBench_Leaderboard.md"
            )
            reporter.generate_markdown(output_file=output_path)
        if args.significance:
            output_path = os.path.join(
                args.output_dir, "VibeBench_Significance_Report.md"
            )
            reporter.generate_significance_report(output_file=output_path)


if __name__ == "__main__":
    main()

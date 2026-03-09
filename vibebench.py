import os
import json
from datetime import datetime
from core.executor import CodeExecutor
from core.analyzer import CodeAnalyzer
from radon.complexity import cc_visit

class VibeBench:
    """
    The main orchestration framework for VibeBench. 
    
    This class manages the lifecycle of code analysis, from walking through 
    model-generated datasets to executing code in a sandboxed environment 
    and generating consolidated performance reports[cite: 70, 128].
    """

    def __init__(self, root_dir):
        """
        Initializes the benchmarking suite with a root directory for datasets.

        Args:
            root_dir (str): Path to the directory containing model subfolders 
                            (e.g., 'datasets/').
        """
        self.root_dir = root_dir
        self.results = []
        self.executor = CodeExecutor(timeout=5)

    def get_complexity(self, code):
        """
        Calculates cyclomatic complexity using the radon library.

        Args:
            code (str): The Python source code to analyze.

        Returns:
            float: The average complexity of all code blocks, rounded to two decimal places[cite: 133].
        """
        try:
            blocks = cc_visit(code)
            return round(sum(b.complexity for b in blocks) / len(blocks), 2) if blocks else 0
        except Exception:
            return "Error"

    def run_benchmark(self):
        """
        Executes the multi-model analysis by iterating through the dataset directory.
        
        Specifically identifies 'human_samples' as the Benchmark Reference Data 
        (Gold Standard) to ensure comparative integrity against LLM outputs[cite: 73, 175].
        """
        print(f"🚀 Starting Multi-Model Analysis on: {self.root_dir}\n")
        
        for root, dirs, files in os.walk(self.root_dir):
            folder_name = os.path.basename(root)
            
            # Skip the root folder itself
            if root == self.root_dir:
                continue

            # Formalizing the Human Baseline label for JOSS compliance
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

                    self.results.append({
                        "model": folder_name,
                        "category": "Benchmark Reference" if is_baseline else "AI Synthesis",
                        "file": filename,
                        "complexity": self.get_complexity(code),
                        "docstring_coverage": analyzer.get_docstring_coverage(),
                        "bad_practices_count": len(analyzer.detect_bad_practices()),
                        "execution_time_sec": exec_metrics.get("execution_time", "Error"),
                        "status": exec_metrics.get("status"),
                        "timestamp": datetime.now().isoformat()
                    })
        self.save_report()

    def save_report(self):
        """
        Serializes the benchmark results into a timestamped JSON report for 
        further analysis or leaderboard generation[cite: 147].
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_name = f"vibebench_multimodel_{timestamp}.json"
        
        with open(report_name, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)
        
        print(f"\n✅ Benchmark Complete. Report saved: {report_name}")

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
        help="Path to the tasks JSON file (e.g. datasets/tasks.json)."
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

    args = parser.parse_args()

    if args.command == "analyze":
        import json
        from core.analyzer import CodeAnalyzer

        with open(args.input, "r") as f:
            code = f.read()

        analyzer = CodeAnalyzer(code)
        results = {
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
        print("Benchmark mode: running full suite...")
        # Full benchmark pipeline hook — extend here
        print("Tasks file:", args.tasks)
        if args.models:
            print("Models:", ", ".join(args.models))


if __name__ == "__main__":
    main()

import os
import time
import subprocess
import json
from datetime import datetime

# Import analysis tools
from radon.complexity import cc_visit
from radon.metrics import mi_visit

class VibeBench:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.results = []

    def get_complexity(self, code):
        """Calculates Cyclomatic Complexity (Lower is better)."""
        try:
            blocks = cc_visit(code)
            avg_cc = sum(b.complexity for b in blocks) / len(blocks) if blocks else 0
            return round(avg_cc, 2)
        except Exception:
            return "Error"

    def get_security_score(self, file_path):
        """Runs Bandit to find security vulnerabilities."""
        try:
            # Runs bandit and captures JSON output
            cmd = f"bandit -f json -q {file_path}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Count issues by severity
            issues = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for issue in data.get('results', []):
                severity = issue.get('issue_severity')
                if severity in issues:
                    issues[severity] += 1
            return issues
        except Exception:
            return "Error"

    def measure_performance(self, file_path):
        """Measures execution time. Warning: Runs the code!"""
        start_time = time.perf_counter()
        try:
            # We use a timeout to prevent infinite loops from 'bad' AI code
            subprocess.run(["python", file_path], timeout=5, capture_output=True)
            end_time = time.perf_counter()
            return round(end_time - start_time, 4)
        except subprocess.TimeoutExpired:
            return "Timeout (Infinite Loop?)"
        except Exception:
            return "Execution Error"

    def run_benchmark(self):
        print(f"🚀 Starting VibeBench Analysis on: {self.target_dir}\n")
        
        for filename in os.listdir(self.target_dir):
            if filename.endswith(".py"):
                path = os.path.join(self.target_dir, filename)
                
                with open(path, 'r') as f:
                    code = f.read()

                print(f"Analyzing {filename}...")
                
                analysis = {
                    "file": filename,
                    "complexity": self.get_complexity(code),
                    "security": self.get_security_score(path),
                    "execution_time_sec": self.measure_performance(path),
                    "timestamp": datetime.now().isoformat()
                }
                self.results.append(analysis)

        self.save_report()

    def save_report(self):
        report_name = f"vibebench_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_name, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\n✅ Benchmark Complete. Report saved to: {report_name}")

if __name__ == "__main__":
    # Point this to the folder containing the code you want to test
    # Example: 'samples/ai_generated/'
    folder_to_test = input("Enter the directory path to analyze: ")
    if os.path.exists(folder_to_test):
        bench = VibeBench(folder_to_test)
        bench.run_benchmark()
    else:
        print("Directory not found.")
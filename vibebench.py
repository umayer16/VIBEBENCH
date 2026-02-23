import os
import json
from datetime import datetime
from core.executor import CodeExecutor
from radon.complexity import cc_visit

class VibeBench:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.results = []
        self.executor = CodeExecutor(timeout=5)

    def get_complexity(self, code):
        try:
            blocks = cc_visit(code)
            return round(sum(b.complexity for b in blocks) / len(blocks), 2) if blocks else 0
        except: return "Error"

    def run_benchmark(self):
        print(f"🚀 Starting Multi-Model Analysis on: {self.root_dir}\n")
        
        # Walk through subdirectories (gemini, chatgpt, etc.)
        for root, dirs, files in os.walk(self.root_dir):
            model_name = os.path.basename(root)
            
            # Skip the root folder itself to only process subdirectories
            if root == self.root_dir:
                continue

            for filename in files:
                if filename.endswith(".py"):
                    path = os.path.join(root, filename)
                    print(f"[{model_name.upper()}] Analyzing {filename}...")
                    
                    with open(path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    exec_metrics = self.executor.run(path)

                    self.results.append({
                        "model": model_name,
                        "file": filename,
                        "complexity": self.get_complexity(code),
                        "execution_time_sec": exec_metrics.get("execution_time", "Error"),
                        "status": exec_metrics.get("status"),
                        "timestamp": datetime.now().isoformat()
                    })
        self.save_report()

    def save_report(self):
        report_name = f"vibebench_multimodel_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_name, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\n✅ Benchmark Complete. Report saved: {report_name}")

if __name__ == "__main__":
    folder_to_test = input("Enter the directory path to analyze (e.g., datasets): ")
    if os.path.exists(folder_to_test):
        bench = VibeBench(folder_to_test)
        bench.run_benchmark()
    else:
        print(f"Directory not found: {folder_to_test}")
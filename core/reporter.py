import json
import os
import glob
from datetime import datetime  # FIXED: Moved from __main__ to top level for global access

class VibeReporter:
    def __init__(self, json_file):
        """Loads the raw benchmark data from the JSON report."""
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"Report file not found: {json_file}")
            
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def generate_markdown(self, output_file="VibeBench_Leaderboard.md"):
        """Creates a high-level leaderboard and a detailed comparison table."""
        if not self.data:
            print("⚠️ No data found in the report.")
            return

        md_content = "# 🏆 AI Code Quality Leaderboard\n"
        # Accessing datetime here now works regardless of how the script is run
        md_content += f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # 1. Aggregate stats per model
        models = {}
        for entry in self.data:
            m = entry.get('model', 'Unknown')
            if m not in models:
                models[m] = {"comp": [], "time": [], "docs": [], "bugs": 0}
            
            # Handle potential 'Error' strings in numeric fields
            comp = entry.get('complexity')
            if isinstance(comp, (int, float)):
                models[m]["comp"].append(comp)
                
            exec_time = entry.get('execution_time_sec')
            if isinstance(exec_time, (int, float)):
                models[m]["time"].append(exec_time)
            
            doc_cov = entry.get('docstring_coverage', 0)
            if isinstance(doc_cov, (int, float)):
                models[m]["docs"].append(doc_cov)
                
            models[m]["bugs"] += entry.get('bad_practices_count', 0)

        # 2. Summary Leaderboard Table
        md_content += "## 📈 Model Comparison Summary\n"
        md_content += "| Model | Avg Complexity | Avg Exec Time | Doc Coverage | Total Bad Practices |\n"
        md_content += "| :--- | :---: | :---: | :---: | :---: |\n"

        # Sort models by success rate descending, then by avg complexity ascending
        sorted_models = sorted(
            models.items(),
            key=lambda x: (
                
                -(x[1]["success"] / x[1]["total"] if x[1]["total"] > 0 else 0),
                sum(x[1]["comp"]) / len(x[1]["comp"]) if x[1]["comp"] else 0
            )
        )

        for m, stats in sorted_models:
            avg_c = sum(stats["comp"]) / len(stats["comp"]) if stats["comp"] else 0
            avg_t = sum(stats["time"]) / len(stats["time"]) if stats["time"] else 0
            avg_d = sum(stats["docs"]) / len(stats["docs"]) if stats["docs"] else 0

            if m not in models:
              
              models[m] = {"comp": [], "time": [], "docs": [], "bugs": 0, "success": 0, "total": 0}
            models[m]["total"] += 1
            if entry.get('status') == 'Success':
                models[m]["success"] += 1

            success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
            md_content += f"| {m.upper()} | {avg_c:.2f} | {avg_t:.4f}s | {avg_d:.1f}% | {stats['bugs']} | {success_rate:.1f}% |\n"


        # 3. Detailed Data Table
        md_content += "\n## 🔍 Detailed File Analysis\n"
        md_content += "| Model | Avg Complexity | Avg Exec Time | Doc Coverage | Total Bad Practices | Success Rate |\n"
        md_content += "| :--- | :---: | :---: | :---: | :---: | :---: |\n"

        for entry in self.data:
            md_content += (f"| {entry.get('model', 'N/A').upper()} | {entry['file']} | "
                          f"{entry['complexity']} | {entry['execution_time_sec']}s | {entry['status']} |\n")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Professional Leaderboard generated: {output_file}")

if __name__ == "__main__":
    # Automatically find the latest multi-model report
    json_files = glob.glob("vibebench_multimodel_*.json")
    
    if json_files:
        # Sorts by creation time to find the newest one
        latest_report = max(json_files, key=os.path.getctime)
        print(f"📄 Processing latest report: {latest_report}")
        
        reporter = VibeReporter(latest_report)
        reporter.generate_markdown()
    else:
        print("❌ No report files found. Please run 'python vibebench.py' first.")
import json
import os

class VibeReporter:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.data = json.load(f)

    def generate_markdown(self, output_file="VibeBench_Report.md"):
        """Creates a high-level summary and a detailed comparison table."""
        
        md_content = "# 📊 VibeBench Analysis Report\n"
        md_content += f"**Date:** {os.path.basename(output_file).split('_')[-1].replace('.md', '')}\n\n"
        
        # 1. Summary Statistics
        md_content += "## 📈 Executive Summary\n"
        total_files = len(self.data)
        avg_complexity = sum(d['complexity'] for d in self.data) / total_files
        avg_time = sum(d['execution_time_sec'] for d in self.data if isinstance(d['execution_time_sec'], float)) / total_files
        
        md_content += f"- **Total Scripts Analyzed:** {total_files}\n"
        md_content += f"- **Average Cyclomatic Complexity:** {avg_complexity:.2f}\n"
        md_content += f"- **Average Execution Time:** {avg_time:.4f}s\n\n"

        # 2. Detailed Data Table
        md_content += "## 🔍 Detailed File Analysis\n"
        md_content += "| File Name | Complexity | Security (High/Med/Low) | Exec Time |\n"
        md_content += "| :--- | :---: | :---: | :---: |\n"

        for entry in self.data:
            sec = entry['security']
            sec_str = f"{sec['HIGH']}/{sec['MEDIUM']}/{sec['LOW']}" if isinstance(sec, dict) else "N/A"
            
            md_content += f"| {entry['file']} | {entry['complexity']} | {sec_str} | {entry['execution_time_sec']}s |\n"

        # 3. Research Insights (Automated)
        md_content += "\n## 💡 Key Research Insights\n"
        high_risk = [d['file'] for d in self.data if isinstance(d['security'], dict) and d['security']['HIGH'] > 0]
        
        if high_risk:
            md_content += f"- ⚠️ **Security Alert:** {len(high_risk)} files contain high-severity vulnerabilities.\n"
        else:
            md_content += "- ✅ No high-severity security vulnerabilities detected.\n"
            
        md_content += "- *Recommendation:* Compare these results against the Human-Baseline folder to calculate the 'Vibe Efficiency Gap'.\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Professional Markdown report generated: {output_file}")

# --- Quick Test ---
if __name__ == "__main__":
    # Note: This assumes you have already run vibebench.py and have a JSON file.
    import glob
    json_files = glob.glob("vibebench_report_*.json")
    
    if json_files:
        latest_report = max(json_files, key=os.path.getctime)
        reporter = VibeReporter(latest_report)
        reporter.generate_markdown()
    else:
        print("No report files found. Run vibebench.py first!")
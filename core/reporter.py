import json
import os
import glob
from datetime import datetime


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
        md_content += (
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        )

        # 1. Aggregate stats per model
        models = {}
        for entry in self.data:
            m = entry.get('model', 'Unknown')
            if m not in models:
                models[m] = {
                    "comp": [], "time": [], "docs": [],
                    "bugs": 0, "success": 0, "total": 0
                }

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
            models[m]["total"] += 1
            if entry.get('status') == 'Success':
                models[m]["success"] += 1

        # 2. Summary Leaderboard Table — sorted by success rate descending
        md_content += "## 📈 Model Comparison Summary\n\n"
        md_content += (
            "| Rank | Model | Avg Complexity | Avg Exec Time | "
            "Avg Doc Coverage | Bad Practices | Success Rate |\n"
        )
        md_content += (
            "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n"
        )

        sorted_models = sorted(
            models.items(),
            key=lambda x: (
                -(x[1]["success"] / x[1]["total"] if x[1]["total"] > 0 else 0),
                sum(x[1]["comp"]) / len(x[1]["comp"]) if x[1]["comp"] else 0
            )
        )

        rank = 1
        for m, stats in sorted_models:
            avg_c = (
                round(sum(stats["comp"]) / len(stats["comp"]), 2)
                if stats["comp"] else 0
            )
            avg_t = (
                round(sum(stats["time"]) / len(stats["time"]), 4)
                if stats["time"] else 0
            )
            avg_d = (
                round(sum(stats["docs"]) / len(stats["docs"]), 1)
                if stats["docs"] else 0
            )
            success_rate = (
                f"{stats['success']}/{stats['total']}"
                if stats["total"] > 0 else "0/0"
            )

            rank_str = "—" if m == "human_samples" else str(rank)
            if m != "human_samples":
                rank += 1

            md_content += (
                f"| {rank_str} | {m.upper()} | {avg_c} | {avg_t}s | "
                f"{avg_d}% | {stats['bugs']} | {success_rate} |\n"
            )

        # 3. Detailed File Analysis Table
        md_content += "\n## 🔍 Detailed File Analysis\n\n"
        md_content += (
            "| Model | File | Complexity | Exec Time | "
            "Doc Coverage | Bad Practices | Status |\n"
        )
        md_content += (
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
        )

        for entry in self.data:
            model = entry.get('model', 'N/A').upper()
            fname = entry.get('file', 'N/A')
            comp = entry.get('complexity', 'N/A')
            exec_t = entry.get('execution_time_sec')
            exec_t_str = (
                f"{exec_t:.4f}s" if isinstance(exec_t, (int, float)) else "N/A"
            )
            doc_cov = entry.get('docstring_coverage')
            doc_cov_str = (
                f"{doc_cov:.1f}%"
                if isinstance(doc_cov, (int, float)) else "N/A"
            )
            bad = entry.get('bad_practices_count', 0)
            status = entry.get('status', 'N/A')

            md_content += (
                f"| {model} | {fname} | {comp} | {exec_t_str} | "
                f"{doc_cov_str} | {bad} | {status} |\n"
            )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ Professional Leaderboard generated: {output_file}")


if __name__ == "__main__":
    json_files = glob.glob("vibebench_multimodel_*.json")

    if json_files:
        latest_report = max(json_files, key=os.path.getctime)
        print(f"📄 Processing latest report: {latest_report}")

        reporter = VibeReporter(latest_report)
        reporter.generate_markdown()
    else:
        print("❌ No report files found. Please run 'python vibebench.py' first.")
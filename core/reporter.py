import json
import os
import glob
from datetime import datetime
from scipy import stats


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

        # 1. Aggregate stat per model
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
        for m, stat in sorted_models:
            avg_c = (
                round(sum(stat["comp"]) / len(stat["comp"]), 2)
                if stat["comp"] else 0
            )
            avg_t = (
                round(sum(stat["time"]) / len(stat["time"]), 4)
                if stat["time"] else 0
            )
            avg_d = (
                round(sum(stat["docs"]) / len(stat["docs"]), 1)
                if stat["docs"] else 0
            )
            success_rate = (
                f"{stat['success']}/{stat['total']}"
                if stat["total"] > 0 else "0/0"
            )

            rank_str = "—" if m == "human_samples" else str(rank)
            if m != "human_samples":
                rank += 1

            md_content += (
                f"| {rank_str} | {m.upper()} | {avg_c} | {avg_t}s | "
                f"{avg_d}% | {stat['bugs']} | {success_rate} |\n"
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

    def compare_models_statistically(self, metric='execution_time_sec'):
        """
        Performs pairwise Mann-Whitney U tests between all model pairs
        for a given metric and returns a significance report.

        The Mann-Whitney U test is used because execution times and
        complexity scores are not normally distributed.

        Args:
            metric (str): The metric to compare. Must be a numeric field
            in the benchmark JSON records. Default: execution_time_sec.

        Returns:
            dict: Nested dict of {model_a: {model_b: result_dict}} where
                result_dict contains 'u_statistic', 'p_value', and
                'significant' (bool, p < 0.05).
        """
        # Group metric values by model
        model_data = {}
        for entry in self.data:
            m = entry.get('model', 'Unknown')
            val = entry.get(metric)
            if isinstance(val, (int, float)):
                if m not in model_data:
                    model_data[m] = []
                model_data[m].append(val)
        models = sorted(model_data.keys())
        results = {}
        for i, model_a in enumerate(models):
            results[model_a] = {}
            for model_b in models[i + 1:]:
                data_a = model_data[model_a]
                data_b = model_data[model_b]

                # Need at least 3 data points per group for meaningful test
                if len(data_a) < 3 or len(data_b) < 3:
                    results[model_a][model_b] = {
                        'u_statistic': None,
                        'p_value': None,
                        'significant': None,
                        'note': 'Insufficient data'
                    }
                    continue
                u_stat, p_val = stats.mannwhitneyu(
                    data_a, data_b, alternative='two-sided'
                )
                results[model_a][model_b] = {
                    'u_statistic': round(float(u_stat), 4),
                    'p_value': round(float(p_val), 4),
                    'significant': bool(p_val < 0.05)
                }
        return results

    def generate_significance_report(
        self,
        output_file="VibeBench_Significance_Report.md"
    ):
        """
        Generates a Markdown report of pairwise statistical significance
        tests between all models for execution time and complexity.

        Args:
            output_file (str): Path to write the Markdown report.
        """
        md = "# VibeBench Statistical Significance Report\n\n"
        md += (
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        )
        md += (
            "Statistical comparisons use two-sided Mann-Whitney U tests. "
            "Differences are considered significant at p < 0.05.\n\n"
        )

        for metric, label in [
            ('execution_time_sec', 'Execution Time'),
            ('complexity', 'Cyclomatic Complexity')
        ]:
            md += f"## {label} Comparisons\n\n"
            md += "| Model A | Model B | U Statistic | p-value | Significant |\n"
            md += "| :--- | :--- | :---: | :---: | :---: |\n"

            results = self.compare_models_statistically(metric)

            any_results = False
            for model_a, comparisons in results.items():
                for model_b, res in comparisons.items():
                    any_results = True
                    if res['p_value'] is None:
                        md += (
                            f"| {model_a.upper()} | {model_b.upper()} | "
                            f"— | — | Insufficient data |\n"
                        )
                    else:
                        sig = "✅ Yes" if res['significant'] else "❌ No"
                        md += (
                            f"| {model_a.upper()} | {model_b.upper()} | "
                            f"{res['u_statistic']} | {res['p_value']} | "
                            f"{sig} |\n"
                        )
            if not any_results:
                md += "| No comparable model pairs found | | | | |\n"
            md += "\n"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"✅ Significance report generated: {output_file}")


if __name__ == "__main__":
    json_files = glob.glob("vibebench_multimodel_*.json")

    if json_files:
        latest_report = max(json_files, key=os.path.getctime)
        print(f"📄 Processing latest report: {latest_report}")

        reporter = VibeReporter(latest_report)
        reporter.generate_markdown()
    else:
        print("❌ No report files found. Please run 'python vibebench.py' first.")

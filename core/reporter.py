import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from scipy import stats


class VibeReporter:
    def __init__(self, json_file: str) -> None:
        """Loads the raw benchmark data from the JSON report."""
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"Report file not found: {json_file}")

        with open(json_file, 'r', encoding='utf-8') as f:
            self.data: List[Dict[str, Any]] = json.load(f)

    def _aggregate_model_stats(self) -> Dict[str, Dict[str, Any]]:
        """Aggregates per-file benchmark records into model summary stats."""
        models: Dict[str, Dict[str, Any]] = {}
        for entry in self.data:
            m: str = entry.get('model', 'Unknown')
            if m not in models:
                models[m] = {
                    "comp": [], "time": [], "docs": [],
                    "bugs": 0, "success": 0, "total": 0,
                    "carbon": []
                }

            comp: Any = entry.get('complexity')
            if isinstance(comp, (int, float)):
                models[m]["comp"].append(comp)

            exec_time: Any = entry.get('execution_time_sec')
            if isinstance(exec_time, (int, float)):
                models[m]["time"].append(exec_time)

            doc_cov: Any = entry.get('docstring_coverage', 0)
            if isinstance(doc_cov, (int, float)):
                models[m]["docs"].append(doc_cov)

            carbon: Any = entry.get('carbon_footprint_gCO2e')
            if isinstance(carbon, (int, float)):
                models[m]["carbon"].append(carbon)

            models[m]["bugs"] += entry.get('bad_practices_count', 0)
            models[m]["total"] += 1
            if entry.get('status') == 'Success':
                models[m]["success"] += 1
        return models

    def _format_summary_row(
        self, rank_str: str, m: str, stat: Dict[str, Any]
    ) -> str:
        """Formats a single row of the leaderboard summary table."""
        avg_c: float = (
            round(sum(stat["comp"]) / len(stat["comp"]), 2)
            if stat["comp"] else 0.0
        )
        avg_t: float = (
            round(sum(stat["time"]) / len(stat["time"]), 4)
            if stat["time"] else 0.0
        )
        avg_d: float = (
            round(sum(stat["docs"]) / len(stat["docs"]), 1)
            if stat["docs"] else 0.0
        )
        success_rate: str = (
            f"{stat['success']}/{stat['total']}"
            if stat["total"] > 0 else "0/0"
        )

        total_carbon_ug: Union[float, str] = "N/A"
        if stat["carbon"]:
            total_carbon_ug = round(sum(stat["carbon"]) * 1_000_000, 4)

        return (
            f"| {rank_str} | {m.upper()} | {avg_c} | {avg_t}s | "
            f"{avg_d}% | {stat['bugs']} | {success_rate} | "
            f"{total_carbon_ug} |\n"
        )

    def _format_detail_row(self, entry: Dict[str, Any]) -> str:
        """Formats a single row of the detailed file analysis table."""
        model: str = entry.get('model', 'N/A').upper()
        fname: str = entry.get('file', 'N/A')
        comp_val: Any = entry.get('complexity', 'N/A')
        exec_t: Any = entry.get('execution_time_sec')
        std: Any = entry.get('execution_time_std')

        exec_t_str: str = "N/A"
        if isinstance(exec_t, (int, float)):
            if isinstance(std, float):
                exec_t_str = f"{exec_t:.4f}s ± {std:.4f}s"
            else:
                exec_t_str = f"{exec_t:.4f}s"

        doc_cov_val: Any = entry.get('docstring_coverage')
        doc_cov_str: str = "N/A"
        if isinstance(doc_cov_val, (int, float)):
            doc_cov_str = f"{doc_cov_val:.1f}%"

        bad: int = entry.get('bad_practices_count', 0)
        status: str = entry.get('status', 'N/A')
        runs: int = entry.get('runs', 1)
        run_str: str = (
            f"{entry.get('successful_runs', '?')}/{runs}"
            if runs > 1 else "1/1"
        )
        return (
            f"| {model} | {fname} | {comp_val} | {exec_t_str} | "
            f"{doc_cov_str} | {bad} | {run_str} | {status} |\n"
        )

    def generate_markdown(
        self, output_file: str = "VibeBench_Leaderboard.md"
    ) -> None:
        """Creates a high-level leaderboard and detailed metric table."""
        if not self.data:
            print("⚠️ No data found in the report.")
            return

        md_content: str = "# 🏆 AI Code Quality Leaderboard\n"
        date_str: str = datetime.now().strftime('%Y-%m-%d %H:%M')
        md_content += f"**Report Date:** {date_str}\n\n"

        models = self._aggregate_model_stats()

        md_content += "## 📈 Model Comparison Summary\n\n"
        md_content += (
            "| Rank | Model | Avg Complexity | Avg Exec Time | "
            "Avg Doc Coverage | Bad Practices | Success Rate | "
            "Total CO₂e (µg) |\n"
        )
        md_content += (
            "| :---: | :--- | :---: | :---: | :---: | "
            ":---: | :---: | :---: |\n"
        )

        sorted_models: List[Tuple[str, Dict[str, Any]]] = sorted(
            models.items(),
            key=lambda x: (
                -(x[1]["success"] / x[1]["total"] if x[1]["total"] > 0 else 0),
                sum(x[1]["comp"]) / len(x[1]["comp"]) if x[1]["comp"] else 0
            )
        )

        rank: int = 1
        for m, stat in sorted_models:
            rank_str: str = "—" if m == "human_samples" else str(rank)
            if m != "human_samples":
                rank += 1
            md_content += self._format_summary_row(rank_str, m, stat)

        md_content += "\n## 🔍 Detailed File Analysis\n\n"
        md_content += (
            "| Model | File | Complexity | Exec Time | "
            "Doc Coverage | Bad Practices | Runs | Status |\n"
        )
        md_content += (
            "| :--- | :--- | :---: | :---: | :---: | "
            ":---: | :---: | :---: |\n"
        )

        for entry in self.data:
            md_content += self._format_detail_row(entry)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ Professional Leaderboard generated: {output_file}")

    def compare_models_statistically(
        self, metric: str = 'execution_time_sec'
    ) -> Dict[str, Dict[str, Any]]:
        """Performs pairwise Mann-Whitney U tests between all model pairs."""
        model_data: Dict[str, List[float]] = {}
        for entry in self.data:
            m: str = entry.get('model', 'Unknown')
            val: Any = entry.get(metric)
            if isinstance(val, (int, float)):
                if m not in model_data:
                    model_data[m] = []
                model_data[m].append(float(val))

        models: List[str] = sorted(model_data.keys())
        results: Dict[str, Dict[str, Any]] = {}

        for i, model_a in enumerate(models):
            results[model_a] = {}
            for model_b in models[i + 1:]:
                data_a: List[float] = model_data[model_a]
                data_b: List[float] = model_data[model_b]

                if len(data_a) < 3 or len(data_b) < 3:
                    results[model_a][model_b] = {
                        'u_statistic': None, 'p_value': None,
                        'significant': None, 'note': 'Insufficient data'
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
        self, output_file: str = "VibeBench_Significance_Report.md"
    ) -> None:
        """Generates a Markdown report of pairwise statistical significance."""
        md: str = "# VibeBench Statistical Significance Report\n\n"
        date_str: str = datetime.now().strftime('%Y-%m-%d %H:%M')
        md += f"**Report Date:** {date_str}\n\n"
        md += (
            "Statistical comparisons use two-sided Mann-Whitney U tests. "
            "Differences are considered significant at p < 0.05.\n\n"
        )

        for metric, label in [
            ('execution_time_sec', 'Execution Time'),
            ('complexity', 'Cyclomatic Complexity')
        ]:
            md += f"## {label} Comparisons\n\n"
            md += (
                "| Model A | Model B | U Statistic | "
                "p-value | Significant |\n"
            )
            md += "| :--- | :--- | :---: | :---: | :---: |\n"

            results: Dict[str, Dict[str, Any]] = (
                self.compare_models_statistically(metric)
            )
            any_results: bool = False
            for model_a, comparisons in results.items():
                for model_b, res in comparisons.items():
                    any_results = True
                    if res['p_value'] is None:
                        md += (
                            f"| {model_a.upper()} | {model_b.upper()} | "
                            f"— | — | Insufficient data |\n"
                        )
                    else:
                        sig: str = "✅ Yes" if res['significant'] else "❌ No"
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

    @staticmethod
    def _aggregate_run_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate benchmark records by model into summary stats."""
        models: Dict[str, Any] = {}
        for entry in data:
            m: str = entry.get('model', 'Unknown')
            if m not in models:
                models[m] = {'success': 0, 'total': 0, 'comp': [], 'time': []}
            models[m]['total'] += 1
            if entry.get('status') == 'Success':
                models[m]['success'] += 1
            comp_val: Any = entry.get('complexity')
            if isinstance(comp_val, (int, float)):
                models[m]['comp'].append(comp_val)
            exec_t: Any = entry.get('execution_time_sec')
            if isinstance(exec_t, (int, float)):
                models[m]['time'].append(exec_t)

        for m in models:
            models[m]['avg_comp'] = (
                round(sum(models[m]['comp']) / len(models[m]['comp']), 2)
                if models[m]['comp'] else None
            )
            models[m]['avg_time'] = (
                round(sum(models[m]['time']) / len(models[m]['time']), 4)
                if models[m]['time'] else None
            )
            models[m]['success_rate'] = (
                models[m]['success'] / models[m]['total']
                if models[m]['total'] > 0 else 0.0
            )
        return models

    @staticmethod
    def _format_comparison_row(
        m: str, stats_a: Dict[str, Any], stats_b: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Formats a model comparison row tracking performance shifts."""
        a = stats_a[m]
        b = stats_b[m]

        sr_a: str = f"{a['success']}/{a['total']}"
        sr_b: str = f"{b['success']}/{b['total']}"
        delta_sr: float = b['success_rate'] - a['success_rate']
        delta_sr_str: str = "—"
        if delta_sr > 0:
            delta_sr_str = f"+{delta_sr:.0%}"
        elif delta_sr < 0:
            delta_sr_str = f"{delta_sr:.0%}"

        comp_a: Any = a['avg_comp'] if a['avg_comp'] is not None else "N/A"
        comp_b: Any = b['avg_comp'] if b['avg_comp'] is not None else "N/A"
        delta_comp_str: str = "N/A"
        if isinstance(comp_a, float) and isinstance(comp_b, float):
            delta_comp: float = round(comp_b - comp_a, 2)
            delta_comp_str = (
                f"+{delta_comp}" if delta_comp > 0
                else str(delta_comp) if delta_comp < 0 else "—"
            )

        time_a: str = f"{a['avg_time']}s" if a['avg_time'] is not None else "N/A"
        time_b: str = f"{b['avg_time']}s" if b['avg_time'] is not None else "N/A"
        delta_time_str: str = "N/A"
        if a['avg_time'] is not None and b['avg_time'] is not None:
            delta_time: float = round(b['avg_time'] - a['avg_time'], 4)
            delta_time_str = (
                f"+{delta_time}s" if delta_time > 0
                else f"{delta_time}s" if delta_time < 0 else "—"
            )

        row_md = (
            f"| {m.upper()} | {sr_a} | {sr_b} | {delta_sr_str} | "
            f"{comp_a} | {comp_b} | {delta_comp_str} | "
            f"{time_a} | {time_b} | {delta_time_str} |\n"
        )

        delta_c_val: Optional[float] = None
        if isinstance(comp_a, float) and isinstance(comp_b, float):
            delta_c_val = round(comp_b - comp_a, 2)

        delta_t_val: Optional[float] = None
        if a['avg_time'] and b['avg_time']:
            delta_t_val = round(b['avg_time'] - a['avg_time'], 4)

        change_metrics = {
            'delta_success_rate': delta_sr,
            'delta_complexity': delta_c_val,
            'delta_exec_time': delta_t_val
        }
        return row_md, change_metrics

    @classmethod
    def compare_runs(
        cls,
        json_file_a: str,
        json_file_b: str,
        output_file: str = "VibeBench_Comparison.md"
    ) -> Dict[str, Dict[str, Any]]:
        """Compares two benchmark runs and builds an improvement report."""
        for path in (json_file_a, json_file_b):
            if not os.path.exists(path):
                raise FileNotFoundError(f"Benchmark file not found: {path}")

        with open(json_file_a, 'r', encoding='utf-8') as f:
            data_a: List[Dict[str, Any]] = json.load(f)
        with open(json_file_b, 'r', encoding='utf-8') as f:
            data_b: List[Dict[str, Any]] = json.load(f)

        stats_a = cls._aggregate_run_stats(data_a)
        stats_b = cls._aggregate_run_stats(data_b)

        added: set[str] = set(stats_b.keys()) - set(stats_a.keys())
        dropped: set[str] = set(stats_a.keys()) - set(stats_b.keys())
        common: set[str] = set(stats_a.keys()) & set(stats_b.keys())

        md: str = "# VibeBench Run Comparison Report\n\n"
        md += f"**Run A:** `{os.path.basename(json_file_a)}`\n"
        md += f"**Run B:** `{os.path.basename(json_file_b)}`\n"
        date_str: str = datetime.now().strftime('%Y-%m-%d %H:%M')
        md += f"**Generated:** {date_str}\n\n"

        if added:
            md += "## ✅ Models Added in Run B\n\n"
            for m in sorted(added):
                md += f"- `{m.upper()}`\n"
            md += "\n"
        if dropped:
            md += "## ❌ Models Dropped from Run A\n\n"
            for m in sorted(dropped):
                md += f"- `{m.upper()}`\n"
            md += "\n"

        md += "## 📊 Model Performance Changes\n\n"
        md += (
            "| Model | Success A | Success B | Δ Success | "
            "Avg Complexity A | Avg Complexity B | Δ Complexity | "
            "Avg Exec Time A | Avg Exec Time B | Δ Exec Time |\n"
        )
        md += (
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | "
            ":---: | :---: | :---: |\n"
        )

        changes: Dict[str, Dict[str, Any]] = {}
        for m in sorted(common):
            row_str, metrics = cls._format_comparison_row(m, stats_a, stats_b)
            md += row_str
            changes[m] = metrics

        regressions: List[str] = [
            m for m, c in changes.items() if c['delta_success_rate'] < 0
        ]
        improvements: List[str] = [
            m for m, c in changes.items() if c['delta_success_rate'] > 0
        ]

        md += "\n## 📋 Summary\n\n"
        if improvements:
            md += (
                f"**Improved:** "
                f"{', '.join(m.upper() for m in improvements)}\n\n"
            )
        if regressions:
            md += (
                f"**Regressed:** "
                f"{', '.join(m.upper() for m in regressions)}\n\n"
            )
        if not improvements and not regressions:
            md += "No success rate changes detected between runs.\n\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)

        print(f"✅ Comparison report generated: {output_file}")
        return changes

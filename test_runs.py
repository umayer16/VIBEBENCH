# test_runs.py — run this from the VIBEBENCH directory
from core.executor import CodeExecutor

executor = CodeExecutor(timeout=5)
result = executor.run_multiple(
    'datasets/human_samples/TASK-001_manual.py',
    runs=3
)
print(result)

# Subject: Open-source benchmark for LLM code quality evaluation— VibeBench

Dear Professor [Name],

I am a student researcher at Saint Joseph Higher Secondary School
in Dhaka, Bangladesh. I recently completed a study evaluating the
code quality of 7 large language models across 10 Python benchmark
tasks using a framework I built called VibeBench.

VibeBench goes beyond functional correctness by measuring cyclomatic
complexity, docstring coverage, bad practice detection, and sandboxed
execution under resource limits — metrics that HumanEval and MBPP
do not capture.

The key finding: every evaluated AI model failed a task requiring
async HTTP operations with an external dependency, while the human
baseline succeeded. This failure class is invisible to correctness-
only benchmarks but common in production deployment.

The framework is open-source (MIT License):
[VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)

A preprint is available on arXiv:
[arXiv link when live]

I would be grateful if you found the methodology or findings useful
for your own research. I am also happy to answer any questions
about the evaluation design.

Thank you for your time.

Best regards,
Muktadir Arif
Saint Joseph Higher Secondary School, Dhaka, Bangladesh
GitHub: [VibeBench GitHub Repository](https://github.com/umayer16/VIBEBENCH)

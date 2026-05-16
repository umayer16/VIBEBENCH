# Title

I built an open-source tool that measures AI code quality beyond
"does it run" — VibeBench
Body:
Most AI code benchmarks just check if the code passes tests.
VibeBench checks if it's actually good code:

- Cyclomatic complexity (is it overly complicated?)
- Docstring coverage (is it documented?)
- Bad practice detection (mutable defaults, hardcoded credentials, etc.)
- Sandboxed execution with resource limits
- Comparison against a human baseline

I ran it on 7 models across 10 tasks. Some highlights:

- Every AI model failed an async task because they assumed
  a library was installed that wasn't
- Claude wrote 0% documented code on most tasks despite high
  pass rates
- The human baseline had lower average complexity than every
  AI model tested

It's MIT licensed, extensible (add your own tasks/models),
and has tutorials for contributing.

GitHub:

# Dataset Quality Notes

This document records known data quality issues in the benchmark
dataset and the decisions made to address them. All issues are
documented rather than silently corrected to preserve the integrity
of the published benchmark results.

---

## Issue DQ-001: TASK-004_chatgpt.py contains Dijkstra code

**File:** `datasets/ai_samples/chatgpt/TASK-004_chatgpt.py`  
**Discovered:** May 2026 (GitHub Issue #5)  
**Severity:** Medium

### Description
This file contains Dijkstra shortest path implementation code
rather than a CSV average calculator as required by TASK-004.
This appears to be a data collection error where the ChatGPT
output for TASK-003 was accidentally saved under the TASK-004
filename.

### Evidence
- The file imports `heapq` and implements `dijkstra()` — 
  consistent with TASK-003 (Algorithms)
- The file contains no CSV reading, no file I/O operations,
  and no average calculation — inconsistent with TASK-004 
  (File I/O)
- The benchmark result for this file shows `Status: Success`
  because the Dijkstra code runs correctly, but it is testing
  the wrong capability

### Impact on Published Results
The TASK-004 ChatGPT result in the v1.2.0 leaderboard reflects
execution of Dijkstra code, not CSV processing. The complexity
score (6.0) and execution time (0.050s) are valid measurements
of the wrong program.

### Decision
The file is preserved as-is to maintain reproducibility of the
published v1.2.0 results. A corrected file will be collected
and added as `TASK-004_chatgpt_v2.py` in a future benchmark
refresh. The leaderboard will note this issue with a footnote
in v2.0.0.

---

## Issue DQ-002: Gemini TASK-004 does not skip header row

**File:** `datasets/ai_samples/gemini/TASK-004_ai.py`  
**Discovered:** May 2026 (GitHub Issue #6)  
**Severity:** Low

### Description
The Gemini TASK-004 solution reads the CSV file but does not
skip the header row. The string 'Price' (the column header)
causes a `ValueError` when parsed as float, which is silently
caught and skipped. The average is therefore calculated only
over the numeric rows, which happens to produce the correct
result — but for the wrong reason.

### Evidence
Looking at `TASK-004_ai.py`:
```python
for row in reader:
    if len(row) >= 2:
        try:
            value = float(row[1])  # 'Price' raises ValueError here
            ...
        except ValueError:
            continue  # silently skips header
```

### Impact on Published Results
The benchmark result shows `Status: Success` which is technically
correct — the output file contains the right answer. However the
implementation is fragile: if the header value happened to be
numeric it would be incorrectly included in the average.

### Decision
The file is preserved as-is. This is documented as a known
fragility in the Gemini solution. VibeBench's static analysis
does not currently detect this pattern — a future heuristic
improvement could flag CSV reading without explicit header
handling.
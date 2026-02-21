from functools import lru_cache
import sys

# Increasing recursion depth is a common AI "fix"
sys.setrecursionlimit(2000)

@lru_cache(None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print(f"50th Fibonacci: {fibonacci(50)}")
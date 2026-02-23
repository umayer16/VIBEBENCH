import time


def fibonacci_memoized(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def fibonacci_sequence(count=50):
    return [fibonacci_memoized(i) for i in range(count)]


def benchmark(func, *args, runs=1000):
    start = time.perf_counter()
    for _ in range(runs):
        result = func(*args)
    elapsed = (time.perf_counter() - start) / runs
    return result, elapsed


if __name__ == "__main__":
    print("=" * 52)
    print("        Fibonacci Sequence (Memoization)")
    print("=" * 52)

    sequence = fibonacci_sequence(50)

    print("\nFirst 50 Fibonacci numbers:\n")
    for i, val in enumerate(sequence):
        print(f"  F({i:>2}) = {val}")

    print("\n" + "-" * 52)
    print(f"  ✔ The 50th Fibonacci number (F(49)) = {sequence[49]}")
    print("-" * 52)

    _, elapsed = benchmark(fibonacci_memoized, 49)
    print(f"\n  Avg time per call (1000 runs): {elapsed * 1_000_000:.4f} µs")
    print("  (Memoization ensures O(1) lookup after first computation)")
    print("=" * 52)
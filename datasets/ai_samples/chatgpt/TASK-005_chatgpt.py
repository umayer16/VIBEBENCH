def fibonacci_memo(n, memo=None):
    """
    Returns the nth Fibonacci number using memoization.
    """
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
        return n

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def first_n_fibonacci(n):
    """
    Generates the first n Fibonacci numbers using memoization.
    """
    memo = {}
    sequence = []
    for i in range(n):
        sequence.append(fibonacci_memo(i, memo))
    return sequence


if __name__ == "__main__":
    n = 50
    fib_sequence = first_n_fibonacci(n)
    fiftieth_number = fib_sequence[-1]

    print(f"The first {n} Fibonacci numbers:")
    print(fib_sequence)
    print(f"\nThe 50th Fibonacci number is: {fiftieth_number}")
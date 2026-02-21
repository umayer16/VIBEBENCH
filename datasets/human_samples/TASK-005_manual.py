def fibonacci(n):
    # HUMAN TOUCH: Iterative approach is far more memory efficient than recursion
    if n < 2: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    # No risk of RecursionError here
    print(fibonacci(50))
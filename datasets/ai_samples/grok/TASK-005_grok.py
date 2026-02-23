def fibonacci(n, memo=None):
    """
    Calculate the nth Fibonacci number using memoization.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-based)
        memo (dict, optional): Cache dictionary to store previously computed values
    
    Returns:
        int: The nth Fibonacci number
    """
    if memo is None:
        memo = {}
    
    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # Return cached result if already computed
    if n in memo:
        return memo[n]
    
    # Compute and cache the result
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


def generate_fibonacci_sequence(count):
    """
    Generate the first 'count' numbers of the Fibonacci sequence.
    
    Returns:
        list: List containing the first 'count' Fibonacci numbers
    """
    return [fibonacci(i) for i in range(count)]


if __name__ == "__main__":
    # Generate first 50 Fibonacci numbers (indices 0 to 49)
    fib_sequence = generate_fibonacci_sequence(50)
    
    # Print the full sequence (optional - comment out if too long)
    print("First 50 Fibonacci numbers:")
    print(", ".join(map(str, fib_sequence)))
    print()
    
    # Print just the 50th number (index 49)
    print(f"The 50th Fibonacci number (F(49)) is:")
    print(fib_sequence[49])
    print()
    
    # Bonus: Show how memoization helps
    print(f"Size of memoization cache after computation: {len(fibonacci.__defaults__[0])}")
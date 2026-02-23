def fibonacci_memoized(n, memo=None):
    """
    Calculate the nth Fibonacci number using memoization for optimization.
    
    Args:
        n: The position in the Fibonacci sequence (0-based or 1-based depending on implementation)
        memo: Dictionary for memoization (used internally for recursive calls)
        
    Returns:
        The nth Fibonacci number
    """
    # Initialize memoization dictionary on first call
    if memo is None:
        memo = {}
    
    # Base cases
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    # Check if already calculated
    if n in memo:
        return memo[n]
    
    # Calculate and store in memo
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def fibonacci_sequence_memoized(count):
    """
    Generate the first 'count' numbers of the Fibonacci sequence using memoization.
    
    Args:
        count: Number of Fibonacci numbers to generate (count >= 1)
        
    Returns:
        list: First 'count' Fibonacci numbers
        
    Raises:
        ValueError: If count is less than 1
    """
    if count < 1:
        raise ValueError("Count must be at least 1")
    
    # Use memoization to efficiently generate the sequence
    memo = {0: 0, 1: 1}
    
    def fib_with_memo(n):
        if n in memo:
            return memo[n]
        memo[n] = fib_with_memo(n - 1) + fib_with_memo(n - 2)
        return memo[n]
    
    # Generate the sequence
    sequence = []
    for i in range(count):
        sequence.append(fib_with_memo(i))
    
    return sequence


def fibonacci_iterative(n):
    """
    Calculate the nth Fibonacci number iteratively (for comparison).
    
    Args:
        n: The position in the Fibonacci sequence
        
    Returns:
        The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def format_large_number(num):
    """
    Format large numbers with commas for better readability.
    
    Args:
        num: The number to format
        
    Returns:
        str: Formatted number string
    """
    return f"{num:,}"


def performance_comparison():
    """
    Compare performance of memoized vs naive recursive Fibonacci.
    Only runs for small values to avoid excessive computation time.
    """
    import time
    
    print("\nPerformance Comparison (for small values only):")
    print("-" * 50)
    
    def fib_naive(n):
        """Naive recursive Fibonacci (very slow for n > 30)"""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        return fib_naive(n - 1) + fib_naive(n - 2)
    
    # Test with n=30 (naive becomes very slow after this)
    test_value = 30
    
    # Test memoized version
    start = time.time()
    memoized_result = fibonacci_memoized(test_value)
    memoized_time = time.time() - start
    
    # Test naive version
    start = time.time()
    naive_result = fib_naive(test_value)
    naive_time = time.time() - start
    
    print(f"n = {test_value}:")
    print(f"  Memoized: {memoized_time:.6f} seconds - Result: {memoized_result}")
    print(f"  Naive: {naive_time:.6f} seconds - Result: {naive_result}")
    print(f"  Speed improvement: {naive_time/memoized_time:.2f}x faster with memoization")


if __name__ == "__main__":
    print("Fibonacci Sequence Generator with Memoization")
    print("=" * 60)
    
    # Generate first 50 Fibonacci numbers
    count = 50
    
    print(f"\nGenerating the first {count} Fibonacci numbers...")
    print("-" * 60)
    
    # Method 1: Using the sequence generator
    sequence = fibonacci_sequence_memoized(count)
    
    # Display the sequence in a readable format
    print("\nFibonacci Sequence (first 50 numbers):")
    for i, num in enumerate(sequence):
        if i < 10 or i >= 40:  # Show first 10 and last 10
            print(f"F({i:2d}) = {format_large_number(num)}")
        elif i == 10:
            print("..." * 20)
    
    # Method 2: Direct calculation using memoized function
    print("\n" + "=" * 60)
    print("Detailed Results:")
    print("-" * 60)
    
    # Calculate and print specific positions
    positions = [0, 1, 5, 10, 20, 30, 40, 49]  # 49 is the 50th number (0-based index)
    
    for pos in positions:
        # Calculate using memoized function
        fib_num = fibonacci_memoized(pos)
        
        if pos == 49:
            print(f"\n*** The 50th Fibonacci number (F(49)) is: {format_large_number(fib_num)} ***")
        else:
            print(f"F({pos:2d}) = {format_large_number(fib_num)}")
    
    # Verify the calculation
    print("\n" + "=" * 60)
    print("Verification:")
    print("-" * 60)
    
    # Verify using the iterative method
    iterative_result = fibonacci_iterative(49)
    memoized_result = fibonacci_memoized(49)
    
    print(f"Iterative method F(49): {format_large_number(iterative_result)}")
    print(f"Memoized method F(49): {format_large_number(memoized_result)}")
    print(f"Results match: {iterative_result == memoized_result}")
    
    # Show memoization benefits
    print("\n" + "=" * 60)
    print("Memoization Benefits:")
    print("-" * 60)
    
    import time
    
    # First call - calculates all values
    start = time.time()
    result1 = fibonacci_memoized(49)
    time1 = time.time() - start
    
    # Second call - instant lookup from memo
    start = time.time()
    result2 = fibonacci_memoized(49)
    time2 = time.time() - start
    
    print(f"First call (calculating): {time1:.6f} seconds")
    print(f"Second call (cached): {time2:.6f} seconds")
    print(f"Cache speed improvement: {time1/time2:.2f}x faster")
    
    # Show cache contents (limited)
    print("\n" + "=" * 60)
    print("Memoization Cache Statistics:")
    print("-" * 60)
    
    # Create a fresh memo dictionary to demonstrate
    memo = {}
    fib_49 = fibonacci_memoized(49, memo)
    
    print(f"Number of values cached: {len(memo)}")
    print(f"Cache keys (first 10): {sorted(memo.keys())[:10]}")
    
    # Calculate Fibonacci ratios (golden ratio approximation)
    print("\n" + "=" * 60)
    print("Golden Ratio Approximation:")
    print("-" * 60)
    
    if len(sequence) >= 2:
        ratio = sequence[-1] / sequence[-2]
        print(f"F(49) / F(48) = {ratio:.15f}")
        print(f"Golden ratio φ ≈ 1.618033988749895")
        print(f"Difference: {abs(ratio - 1.618033988749895):.15f}")
    
    # Optional: Performance comparison (commented out as it may take time)
    # performance_comparison()
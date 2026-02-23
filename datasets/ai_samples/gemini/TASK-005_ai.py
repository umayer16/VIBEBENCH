def fibonacci_memo(n, memo=None):
    """
    Calculates the nth Fibonacci number using recursion and memoization.
    
    Args:
        n (int): The position in the sequence (0-indexed).
        memo (dict): A dictionary to store previously calculated values.
        
    Returns:
        int: The nth Fibonacci number.
    """
    if memo is None:
        memo = {0: 0, 1: 1}
    
    # Check if value is already in the cache
    if n in memo:
        return memo[n]
    
    # Calculate, store in memo, and return
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

def get_fibonacci_sequence(count):
    """
    Generates a list of the first 'count' Fibonacci numbers.
    """
    sequence = []
    memo = {0: 0, 1: 1}
    for i in range(count):
        sequence.append(fibonacci_memo(i, memo))
    return sequence

if __name__ == "__main__":
    # Calculate the first 50 numbers (0 to 49)
    n_terms = 50
    fib_sequence = get_fibonacci_sequence(n_terms)
    
    # Access the 50th number (index 49)
    # The 50th number is often referred to by index 49 or 50 depending on starting convention.
    # Here, index 49 is the 50th element in a 0-indexed sequence.
    fiftieth_num = fib_sequence[49]
    
    print(f"First {n_terms} numbers of the sequence:")
    print(fib_sequence)
    
    print("-" * 30)
    print(f"The 50th Fibonacci number is: {fiftieth_num}")
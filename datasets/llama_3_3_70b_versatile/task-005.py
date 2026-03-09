def fibonacci(n, memo={}):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    elif n in memo:
        return memo[n]
    else:
        result = fibonacci(n-1, memo) + fibonacci(n-2, memo)
        memo[n] = result
        return result

def generate_fibonacci_sequence(n):
    return [fibonacci(i) for i in range(n)]

print(generate_fibonacci_sequence(50))
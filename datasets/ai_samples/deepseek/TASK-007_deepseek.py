def merge_sort(arr):
    """
    Sorts an unsorted list using the merge sort algorithm.

    Args:
        arr: Unsorted list of comparable elements

    Returns:
        A new sorted list (original remains unchanged)
    """
    # Base case: list with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr[:]  # Return a copy

    # Divide the list into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Merge the sorted halves
    return merge(left_sorted, right_sorted)


def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.

    Args:
        left: First sorted list
        right: Second sorted list

    Returns:
        A new merged sorted list
    """
    merged = []
    i = j = 0

    # Compare elements from both lists and add the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add remaining elements from left list (if any)
    while i < len(left):
        merged.append(left[i])
        i += 1

    # Add remaining elements from right list (if any)
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


# Alternative in-place implementation (creates new list but modifies during process)
def merge_sort_inplace(arr):
    """
    In-place merge sort (still returns a new sorted list but uses indices).
    This version is more memory efficient as it uses indices instead of
    creating many intermediate list copies.

    Args:
        arr: Unsorted list of comparable elements

    Returns:
        A new sorted list (original remains unchanged)
    """
    if len(arr) <= 1:
        return arr[:]

    # Helper function that works with indices
    def merge_sort_helper(start, end):
        if end - start <= 1:
            return arr[start:end]

        mid = (start + end) // 2
        left_sorted = merge_sort_helper(start, mid)
        right_sorted = merge_sort_helper(mid, end)
        return merge(left_sorted, right_sorted)

    return merge_sort_helper(0, len(arr))


# Example usage and test
if __name__ == "__main__":
    # Test cases
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1],
        [],
        [3, 3, 3, 3],
        [10, -5, 0, 7, -2],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1]   # Reverse sorted
    ]

    for test in test_cases:
        original = test.copy()
        sorted_arr = merge_sort(original)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}")
        print(f"Original unchanged: {original}\n")

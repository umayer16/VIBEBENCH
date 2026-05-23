def binary_search(sorted_list, target):
    """
    Perform binary search on a sorted list to find the target element.

    Args:
        sorted_list: A sorted list of elements (ascending order)
        target: The element to search for

    Returns:
        int: The index of the target element if found, otherwise -1
    """
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        # Calculate the middle index
        mid = (left + right) // 2

        # Check if target is present at mid
        if sorted_list[mid] == target:
            return mid
        # If target is greater, ignore left half
        elif sorted_list[mid] < target:
            left = mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1

    # Target not found
    return -1

# Example usage and test cases
if __name__ == "__main__":
    # Test with numbers
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    print(f"List: {numbers}")
    print(f"Search for 7: index {binary_search(numbers, 7)}")  # Should return 3
    print(f"Search for 1: index {binary_search(numbers, 1)}")  # Should return 0
    print(f"Search for 19: index {binary_search(numbers, 19)}") # Should return 9
    print(f"Search for 6: index {binary_search(numbers, 6)}")  # Should return -1

    # Test with strings
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    print(f"\nList: {words}")
    print(f"Search for 'cherry': index {binary_search(words, 'cherry')}")  # Should return 2
    print(f"Search for 'grape': index {binary_search(words, 'grape')}")    # Should return -1
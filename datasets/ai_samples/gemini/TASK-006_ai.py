def binary_search(arr, target):
    """
    Performs a binary search on a sorted list.
    
    Args:
        arr (list): A sorted list of elements.
        target: The element to search for.
        
    Returns:
        int: The index of the target if found, otherwise -1.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        # Find the middle index
        mid = (low + high) // 2
        guess = arr[mid]

        # Check if the target is at the mid position
        if guess == target:
            return mid
        
        # If the guess was too high, update 'high' to narrow search to the left
        if guess > target:
            high = mid - 1
        
        # If the guess was too low, update 'low' to narrow search to the right
        else:
            low = mid + 1

    # Return -1 if the target is not in the list
    return -1
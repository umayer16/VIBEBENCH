def binary_search(arr, target):
    """
    Perform binary search on a sorted list to find the target element.

    Args:
        arr (list): A sorted list of elements to search in.
        target: The element to search for.

    Returns:
        int: The index of the target element if found, otherwise -1.
    """
    if not arr:
        return -1

    left = 0
    right = len(arr) - 1

    while left <= right:
        # Calculate mid to avoid potential integer overflow (though rare in Python)
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

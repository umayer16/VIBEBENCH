def merge_sort(arr):
    """
    Sorts a list using the merge sort algorithm.

    Args:
        arr (list): The unsorted input list

    Returns:
        list: A new sorted list (original list is not modified)
    """
    if len(arr) <= 1:
        return arr[:]  # Return a copy

    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves
    return merge(left_half, right_half)


def merge(left, right):
    """
    Merges two sorted lists into one sorted list.
    """
    result = []
    i = j = 0

    # Compare elements from both lists and merge in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# Example usage:
if __name__ == "__main__":
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = merge_sort(unsorted)
    print("Original:", unsorted)
    print("Sorted:  ", sorted_list)

def merge_sort(arr):
    # Base case: a list of zero or one elements is already sorted
    if len(arr) <= 1:
        return arr

    # Split the list into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves and return the result
    return merge(left_half, right_half)

def merge(left, right):
    sorted_list = []
    i = j = 0

    # Compare elements from both lists and append the smaller one
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # If there are remaining elements in either list, append them
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    
    return sorted_list

# Example usage:
unsorted_data = [38, 27, 43, 3, 9, 82, 10]
sorted_data = merge_sort(unsorted_data)
print(f"Sorted list: {sorted_data}")
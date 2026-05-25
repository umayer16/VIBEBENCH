def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Tests
if __name__ == "__main__":
    tests = [
        ([3, 1, 4, 1, 5, 9, 2, 6], [1, 1, 2, 3, 4, 5, 6, 9]),
        ([], []),
        ([1], [1]),
        ([2, 1], [1, 2]),
        ([-3, 0, -1, 2], [-3, -1, 0, 2]),
    ]
    for inp, expected in tests:
        result = merge_sort(inp)
        status = "✓" if result == expected else "✗"
        print(f"{status} merge_sort({inp}) → {result}")

def binary_search(arr, target):
    # HUMAN TOUCH: Simple iterative approach, clean and readable
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

if __name__ == "__main__":
    sample = [1, 3, 5, 7, 9, 11, 13]
    print(binary_search(sample, 7))   # 3
    print(binary_search(sample, 4))   # -1
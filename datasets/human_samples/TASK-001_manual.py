def reverse_linked_list(arr):
    """
    Standard competitive programming approach: 
    Using a simple list to simulate the logic for speed.
    """
    return arr[::-1]

if __name__ == "__main__":
    # Clean, direct execution
    sample = [1, 2, 3]
    print(reverse_linked_list(sample))
    
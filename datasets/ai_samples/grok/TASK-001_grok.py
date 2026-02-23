class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head):
    """
    Reverses a singly linked list iteratively.
    Time: O(n), Space: O(1)
    """
    prev = None
    current = head
    
    while current is not None:
        # Store next node before we change the link
        next_node = current.next
        
        # Reverse the current node's pointer
        current.next = prev
        
        # Move prev and current one step forward
        prev = current
        current = next_node
    
    # prev is the new head after reversal
    return prev


def print_list(head):
    """Helper function to print the linked list"""
    current = head
    values = []
    while current:
        values.append(str(current.val))
        current = current.next
    print(" → ".join(values) if values else "Empty list")


def create_list(arr):
    """Helper function to create a linked list from a list of values"""
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


if __name__ == "__main__":
    # Test case
    values = [1, 2, 3]
    print("Original list:")
    original = create_list(values)
    print_list(original)
    
    print("\nAfter reversal:")
    reversed_head = reverse_list(original)
    print_list(reversed_head)
    
    # Additional small test cases
    print("\nEdge cases:")
    print("Single node [7] →", end=" ")
    print_list(reverse_list(create_list([7])))
    
    print("Empty list →", end=" ")
    print_list(reverse_list(None))
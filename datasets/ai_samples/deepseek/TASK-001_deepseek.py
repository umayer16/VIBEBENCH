class ListNode:
    """A node in a singly linked list."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linked_list(head):
    """
    Reverse a singly linked list iteratively.
    
    Args:
        head: The head node of the linked list to reverse
        
    Returns:
        The new head node of the reversed linked list
    """
    prev = None
    current = head
    
    while current:
        # Store the next node
        next_temp = current.next
        # Reverse the link
        current.next = prev
        # Move pointers forward
        prev = current
        current = next_temp
    
    return prev


def create_linked_list(values):
    """
    Create a linked list from a list of values.
    
    Args:
        values: List of values to create linked list from
        
    Returns:
        Head node of the created linked list
    """
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next
    
    return head


def linked_list_to_list(head):
    """
    Convert a linked list to a Python list for easy printing.
    
    Args:
        head: Head node of the linked list
        
    Returns:
        List containing all values from the linked list
    """
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result


if __name__ == "__main__":
    # Test case: Reverse [1, 2, 3]
    print("Testing reverse_linked_list function:")
    print("-" * 40)
    
    # Create original list
    original_values = [1, 2, 3]
    original_list = create_linked_list(original_values)
    
    print(f"Original list: {linked_list_to_list(original_list)}")
    
    # Reverse the list
    reversed_list = reverse_linked_list(original_list)
    
    print(f"Reversed list: {linked_list_to_list(reversed_list)}")
    
    # Additional test cases
    print("\nAdditional test cases:")
    print("-" * 40)
    
    # Test empty list
    empty_list = create_linked_list([])
    reversed_empty = reverse_linked_list(empty_list)
    print(f"Empty list reversed: {linked_list_to_list(reversed_empty)}")
    
    # Test single element
    single_list = create_linked_list([42])
    reversed_single = reverse_linked_list(single_list)
    print(f"Single element [42] reversed: {linked_list_to_list(reversed_single)}")
    
    # Test longer list
    longer_values = [5, 10, 15, 20, 25]
    longer_list = create_linked_list(longer_values)
    reversed_longer = reverse_linked_list(longer_list)
    print(f"Longer list {longer_values} reversed: {linked_list_to_list(reversed_longer)}")
class ListNode:
    """A simple node class for a singly linked list."""
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def reverse_linked_list(head):
    """
    Reverses a singly linked list iteratively.
    
    Args:
        head (ListNode): The head of the linked list.
        
    Returns:
        ListNode: The new head of the reversed linked list.
    """
    prev = None
    current = head
    
    while current:
        # Store the next node
        next_node = current.next
        # Reverse the link
        current.next = prev
        # Move pointers one step forward
        prev = current
        current = next_node
        
    return prev

def print_list(head):
    """Helper function to print the linked list."""
    elements = []
    current = head
    while current:
        elements.append(str(current.value))
        current = current.next
    print(" -> ".join(elements) if elements else "Empty List")

if __name__ == "__main__":
    # Create the sample list: 1 -> 2 -> 3
    node3 = ListNode(3)
    node2 = ListNode(2, node3)
    node1 = ListNode(1, node2)

    print("Original list:")
    print_list(node1)

    # Reverse the list
    reversed_head = reverse_linked_list(node1)

    print("\nReversed list:")
    print_list(reversed_head)
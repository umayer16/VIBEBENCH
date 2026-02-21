class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    """Reverses a singly linked list iteratively."""
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# Example test case provided by AI
if __name__ == "__main__":
    node3 = ListNode(3)
    node2 = ListNode(2, node3)
    node1 = ListNode(1, node2)
    
    reversed_head = reverse_linked_list(node1)
    print("Reversed list starts with:", reversed_head.val)
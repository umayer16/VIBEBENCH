class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linked_list(head):
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def build_linked_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def print_linked_list(head):
    result = []
    current = head
    while current:
        result.append(str(current.val))
        current = current.next
    print(" -> ".join(result))


if __name__ == "__main__":
    # Test case: reverse [1, 2, 3]
    values = [1, 2, 3]
    head = build_linked_list(values)

    print("Original list:")
    print_linked_list(head)

    reversed_head = reverse_linked_list(head)

    print("Reversed list:")
    print_linked_list(reversed_head)
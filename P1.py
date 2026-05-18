# Order representing the node in SLLQueue and DLLQueue
class OrderNode:
    def __init__(self, order_id):
        self.order_id = order_id
        self.next = None
        self.prev = None

# 1. Array Implementation
class ArrayQueue:
    def __init__(self):
        self.queue =[]
    
    def add_order(self, order_id):
        """Add order: Enqueue a new order."""
        self.queue.append(order_id)
        
    def process_order(self):
        """Process order: Dequeue and remove the order."""
        if not self.check_if_empty():
            return self.queue.pop(0)
        return None
        
    def view_next_order(self):
        """View next order without removing it."""
        return self.queue[0] if not self.check_if_empty() else None
        
    def cancel_order(self, order_id):
        """Cancel order: Remove specific order by ID (O(n))."""
        if order_id in self.queue:
            self.queue.remove(order_id)
            
    def check_if_empty(self):
        """Determine if there are pending orders."""
        return len(self.queue) == 0

# 2. Singly Linked List Implementation
class SLLQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_order(self, order_id):
        """Add order using SLL (O(1))."""
        new_node = OrderNode(order_id)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def process_order(self):
        """Process and remove the first order (O(1))."""
        if not self.head: return None
        val = self.head.order_id
        self.head = self.head.next
        if not self.head: self.tail = None
        return val

    def view_next_order(self):
        """Peek at the next order in SLL."""
        return self.head.order_id if self.head else None

    def cancel_order(self, order_id):
        """Search and remove a specific order (O(n))."""
        curr = self.head
        prev = None
        while curr:
            if curr.order_id == order_id:
                if prev: prev.next = curr.next
                else: self.head = curr.next
                if curr == self.tail: self.tail = prev
                return True
            prev = curr
            curr = curr.next
        return False

    def check_if_empty(self):
        """Check if SLL is empty."""
        return self.head is None

# 3. Doubly Linked List (Optimized for Direct Reference)
class DLLQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_order(self, order_id):
        """Add order and return direct node reference (O(1))."""
        new_node = OrderNode(order_id)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return new_node

    def process_order(self):
        """Process order from the front (O(1))."""
        if not self.head: return None
        val = self.head.order_id
        self.head = self.head.next
        if self.head: self.head.prev = None
        else: self.tail = None
        return val

    def view_next_order(self):
        """Peek at front of DLL."""
        return self.head.order_id if self.head else None

    def check_if_empty(self):
        """Check if DLL is empty."""
        return self.head is None

    def cancel_order_direct(self, node):
        """Remove specific order in O(1) using a direct node reference."""
        if not node: return
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev



print("--- Comprehensive ArrayQueue Functionality Test ---")
aq = ArrayQueue()

print(f"1. Check if empty (Initial): {aq.check_if_empty()}")

aq.add_order(501)
aq.add_order(502)
aq.add_order(503)
print(f"2. Added orders 501, 502, 503. Check if empty: {aq.check_if_empty()}")

print(f"3. View next order (Peek): {aq.view_next_order()}")

print(f"4. Cancel order 502 (Middle): {aq.cancel_order(502)}")
print(f"5. View next after cancel (Should be 501): {aq.view_next_order()}")

print(f"6. Process order: {aq.process_order()}")
print(f"7. Process order (Should be 503): {aq.process_order()}")

print(f"8. Cancel non-existent order (999): {aq.cancel_order(999)}")
print(f"9. Final check if empty: {aq.check_if_empty()}")

print("\n--- Singly Linked List (SLL) Functionality Test ---")
sq = SLLQueue()
print(f"1. Is SLL empty? {sq.check_if_empty()}")
sq.add_order(601)
sq.add_order(602)
sq.add_order(603)
print(f"2. Peek (Should be 601): {sq.view_next_order()}")
print(f"3. Cancel 602: {sq.cancel_order(602)}")
print(f"4. Process: {sq.process_order()}")
print(f"5. Final Process (Should be 603): {sq.process_order()}")
print(f"6. Is SLL empty? {sq.check_if_empty()}")

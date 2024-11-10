class BinaryMinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        """Insert an item into the heap."""
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """Move the element at index up to maintain the heap property."""
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            # Swap current element with its parent
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def extract_min(self):
        """Remove and return the minimum element (root) from the heap."""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_item

    def _heapify_down(self, index):
        """Move the element at index down to maintain the heap property."""
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def peek_min(self):
        """Return the minimum element without removing it."""
        return self.heap[0] if self.heap else None

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def size(self):
        """Return the number of elements in the heap."""
        return len(self.heap)

    def get_heap(self):
        """Return a copy of the current heap."""
        return list(self.heap)

        """Search for an item by key in the heap and return its index or -1 if not found."""
    def search(self, key):
        for i, item in enumerate(self.heap):
            if item[0] == key:
                return i
        return -1

    """Delete an element by key from the heap."""
    def delete(self, key):
        index = self.search(key)
        if index == -1:
            return
        # Swap the element with the last element and remove the last element
        self.heap[index], self.heap[-1] = self.heap[-1], self.heap[index]
        removed_element = self.heap.pop()

        # Restore the heap property
        if index < len(self.heap):
            self._heapify_down(index)
            self._heapify_up(index)
        return removed_element

    """Update an element's key and value in the heap."""
    def update(self, key, new_value=None):
        index = self.search(key)
        if index == -1:
            return
        # Update the key and value
        self.heap[index] = (key, new_value)
        # Restore the heap property
        if index > 0 and self.heap[index][0] < self.heap[(index - 1) // 2][0]:
            self._heapify_up(index)
        else:
            self._heapify_down(index)

class WaitList:
    def __init__(self):
        """Initialize the priority queue using a binary min-heap."""
        self.min_heap = BinaryMinHeap()

    def enqueue(self,item, priority):
        """Add an item with a given priority to the queue."""
        # Insert as a tuple (priority, item) to the min-heap
        self.min_heap.insert((item, priority))

    def dequeue(self):
        """Remove and return the item with the highest priority (smallest value)."""
        min_item = self.min_heap.extract_min()
        return min_item[1] if min_item else None  # Return only the item, not the priority

    def peek(self):
        """Return the item with the highest priority without removing it."""
        min_item = self.min_heap.peek_min()
        return min_item[1] if min_item else None  # Return only the item, not the priority

    def is_empty(self):
        """Check if the priority queue is empty."""
        return self.min_heap.is_empty()

    def size(self):
        """Return the number of items in the priority queue."""
        return self.min_heap.size()

    def get_queue(self):
        """Return the current state of the priority queue as a list of (priority, item) tuples."""
        return self.min_heap.get_heap()

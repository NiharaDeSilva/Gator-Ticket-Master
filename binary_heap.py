class BinaryHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, key, value=None):
        self.heap.append((key, value))
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while parent_index >= 0 and self.heap[parent_index] > self.heap[index]:
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            index = parent_index
            parent_index = (index - 1) // 2

    def get_min(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def delete_min(self):
        if self.is_empty():
            return None

        min_value = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)

        return min_value

    def _heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest]:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest]:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

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

    def get_size(self):
        return len(self.heap)

    """Return a copy of all items in the heap."""
    def get_items(self):
        return list(self.heap)





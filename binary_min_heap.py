'''
Data structure for Binary Min Heap
Supports initialization, check empty, search, insertion, deletion, find minimum, delete minimum, heapify up and
heapify down and get items.
'''
class BinaryMinHeap:
    def __init__(self):
        self.heap = []

    # Check if heap is empty
    def is_empty(self):
        return len(self.heap) == 0

    # Search for an item by key in the heap and return its index or -1 if not found.
    def search(self, key):
        for i, item in enumerate(self.heap):
            if item[0] == key:
                return i
        return -1

    # Insert a new element to heap
    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    # Delete an element by key from the heap
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

    # Return min value
    def get_min(self):
        if self.is_empty():
            return None
        return self.heap[0]

    # Delete min element from heap
    def delete_min(self):
        if self.is_empty():
            return None
        min_value = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)

        return min_value

    '''
    Restores the heap property after insertion or deletion by moving the element at `index` up the heap until it's in 
    the correct position. Compares the element with its parent and swaps if the parent is greater, ensuring that each 
    parent node is smaller than its children, which maintains the min-heap property.
    '''
    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while parent_index >= 0 and self.heap[parent_index] > self.heap[index]:
            self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
            index = parent_index
            parent_index = (index - 1) // 2

    '''
    Restores the heap property after deletion by moving the element at `index` down the heap until it's in the correct 
    position. Compares the element with its children and swaps with the smallest child if needed, maintaining the
    min-heap structure where each parent node is smaller than its children'''
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

    # Return a copy of all items in the heap
    def get_items(self):
        return list(self.heap)

    # Return size of the heap
    def get_size(self):
        return len(self.heap)

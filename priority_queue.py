class BinaryMinHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, key):
        self.heap.append(key)
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

    # """Update an element's key and value in the heap."""
    # def update(self, key, new_value=None):
    #     index = self.search(key)
    #     if index == -1:
    #         return
    #     # Update the key and value
    #     self.heap[index] = (key, new_value)
    #     # Restore the heap property
    #     if index > 0 and self.heap[index][0] < self.heap[(index - 1) // 2][0]:
    #         self._heapify_up(index)
    #     else:
    #         self._heapify_down(index)

    def get_size(self):
        return len(self.heap)

    """Return a copy of all items in the heap."""
    def get_items(self):
        return list(self.heap)

class Waitlist(BinaryMinHeap):
    def __init__(self):
        super().__init__()

    def add_to_waitlist(self, user, priority, timeStamp):
        self.insert((user, priority, timeStamp))  # Insert as (priority, item_details)

    def remove_from_waitlist(self):
        if self.is_empty():
            return None
        # Find the highest priority item in the heap
        highest_priority_item = max(self.heap, key=lambda x: x[1])
        self.heap.remove(highest_priority_item)  # Remove the item from the heap
        self._rebuild_heap()  # Rebuild the heap to maintain the heap property
        return highest_priority_item[1]

    def search(self, userID):
        for index,(user, priority, timeStamp) in enumerate(self.heap):
            if user == userID:
                return index, (user, priority, timeStamp)
        return None  # Item not found

    def delete(self, userID):
        search_result = self.search(userID)
        if search_result:
            index, _ = search_result
            self.heap[index] = self.heap[-1]  # Replace with the last element
            self.heap.pop()  # Remove the last element
            if index < len(self.heap):
                self._heapify_down(index)
                self._heapify_up(index)
            return True
        else:
            # print(f"User '{userID}' not found in the waitlist.")
            return False

    def update_priority(self, userID, new_priority):
        search_result = self.search(userID)
        if search_result:
            index, (user, priority, timeStamp) = search_result
            self.heap[index] = (userID, new_priority, timeStamp)
            if new_priority < priority:
                self._heapify_up(index)
            else:
                self._heapify_down(index)
            print(f"User {userID} priority has been updated to {new_priority}")
            return True
        else:
            print(f"User {userID} priority is not updated")
            return False

    def remove_highest_priority(self):
        if self.is_empty():
            return None
        highest_priority_item = max(self.heap, key=lambda x: x[0])
        self.heap.remove(highest_priority_item)
        self._rebuild_heap()
        return highest_priority_item[1]

    def _rebuild_heap(self):
        items = self.heap[:]
        self.heap.clear()
        for item in items:
            self.insert(item)

    def get_waitlist(self):
        return [(user, priority, timeStamp) for user, priority, timeStamp in self.heap]

        # def peek_highest_priority(self):
    #     """Return the item with the highest priority without removing it."""
    #     if self.is_empty():
    #         return None
    #     highest_priority_item = max(self.heap, key=lambda x: x[0])
    #     return highest_priority_item[1]
    def get_size(self):
        return len(self.heap)


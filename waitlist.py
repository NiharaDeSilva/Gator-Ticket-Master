from binary_min_heap import BinaryMinHeap

'''
Class to manage the Waitlist extending the Binary Min Heap class
Supports initialization, search, add to waitlist, remove from waitlist, modify priority, drop_from_waitlist, 
get waitlist, get size and sort waitlist by priority functions.
'''
class Waitlist(BinaryMinHeap):
    def __init__(self):
        super().__init__()

    def search(self, userID):
        for index,(user, priority, timeStamp) in enumerate(self.heap):
            if user == userID:
                return index, (user, priority, timeStamp)
        return None

    def add_to_waitlist(self, user, priority, timeStamp):
        self.insert((user, priority, timeStamp))

    # Remove user with highest priority from waitlist
    def remove_from_waitlist(self):
        if self.is_empty():
            return None
        # Find the highest priority item in the heap
        highest_priority_item = max(self.heap, key=lambda x: x[1])
        self.heap.remove(highest_priority_item)
        self._rebuild_heap()
        return highest_priority_item[1]

    # Drop the user matching the userID from waitlist
    def drop_from_waitlist(self, userID):
        search_result = self.search(userID)
        if search_result:
            index, _ = search_result
            self.heap[index] = self.heap[-1]
            self.heap.pop()
            if index < len(self.heap):
                self._heapify_down(index)
                self._heapify_up(index)
            return True
        else:
            return False

    #Update priority of User
    def modify_priority(self, userID, new_priority):
        search_result = self.search(userID)
        if search_result:
            index, (user, priority, timeStamp) = search_result
            self.heap[index] = (userID, new_priority, timeStamp)
            if new_priority < priority:
                self._heapify_up(index)
            else:
                self._heapify_down(index)
            return True
        else:
            return False

    def _rebuild_heap(self):
        items = self.heap[:]
        self.heap.clear()
        for item in items:
            self.insert(item)

    def get_waitlist(self):
        return [(user, priority, timeStamp) for user, priority, timeStamp in self.heap]

    def get_size(self):
        return len(self.heap)

    def sort_waitlist_by_priority(self):
        list = self.get_waitlist()
        sortedList = sorted(list, key=lambda x: (-x[1], x[2]))
        return sortedList








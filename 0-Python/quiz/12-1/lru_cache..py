# LRU dictionary perspective
"""
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capa = capacity
        self.dict = {}
        self.order = []
    def get(self, key: str) -> str | None:
        if key not in self.dict.keys():
            return None
        else:
            self.order.remove(key)
            self.order.append(key) # update key as most recently used
            return self.dict[key]

    def put(self, key: str, value: str) -> None:
        # check if key exists in dictionary, y update dict value, order lru
        if key in self.dict.keys():
            self.order.remove(key)
            self.order.append(key)
            self.dict[key]=value
        else: # no exist
            # 1. if capa fill
            if len(self.order) == self.capa:
                del self.dict[self.order[0]]
                self.order.pop(0)

            self.order.append(key)
            self.dict[key] = value
"""

class DoubleLinkedListNode:
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value
        self.pre = None
        self.next = None
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capa = capacity
        self.cache = {}         # empty dict
        # empty double linked list
        self.head = DoubleLinkedListNode()
        self.tail = DoubleLinkedListNode()
        self.head.next = self.tail
        self.tail.pre = self.head

    def _add_node(self, node):
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        prev = node.prev
        new = node.next
        prev.next = new
        new.prev = prev


    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_node(node)


    def _pop_tail(self):
        res = self.tail.prev
        self._remove_node(res)
        return res
    def get(self, key: str) -> str | None:
        if key not in self.cache.keys():
            return None
        else:
            node = self.cache.get(key)
            self._move_to_head(node)
            return node.val

    def put(self, key: str, value: str) -> None:
        if key in self.cache.keys():
            node = self.cache.get(key)
            self._move_to_head(node)
            self.cache[node] = value
        else:
            node = DoubleLinkedListNode(key, value)

            if len(self.cache)>=self.capa:
                res = self._pop_tail()
                del self.cache[res]
            self._add_node(node)
            self.cache[key]=value




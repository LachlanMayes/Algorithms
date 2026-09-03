"""Data structure implementations.

This module provides canonical implementations of fundamental data structures,
all using plain Python with type hints and full docstrings.
"""

from __future__ import annotations

from collections import OrderedDict
from collections import deque as _deque
from typing import Generic, Hashable, Iterable, TypeVar

T = TypeVar("T")
N = TypeVar("N", bound=Hashable)


# --------------------------------------------------------------------------- #
# Stack
# --------------------------------------------------------------------------- #


class Stack(Generic[T]):
    """LIFO stack backed by a Python list.

    Complexity:
        push: O(1) amortized. pop: O(1). peek: O(1). size: O(1).
    """

    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"


# --------------------------------------------------------------------------- #
# Queue
# --------------------------------------------------------------------------- #


class Queue(Generic[T]):
    """FIFO queue backed by ``collections.deque``.

    Complexity:
        enqueue: O(1). dequeue: O(1). peek: O(1).
    """

    def __init__(self) -> None:
        self._data: _deque[T] = _deque()

    def enqueue(self, item: T) -> None:
        self._data.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return not self._data

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)!r})"


# --------------------------------------------------------------------------- #
# Singly Linked List
# --------------------------------------------------------------------------- #


class _SLLNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _SLLNode[T] | None = None


class LinkedList(Generic[T]):
    """Singly linked list.

    Complexity:
        append: O(n). prepend: O(1). delete: O(n). find: O(n).
    """

    def __init__(self) -> None:
        self.head: _SLLNode[T] | None = None

    def append(self, item: T) -> None:
        new_node = _SLLNode(item)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def prepend(self, item: T) -> None:
        new_node = _SLLNode(item)
        new_node.next = self.head
        self.head = new_node

    def delete(self, item: T) -> bool:
        cur = self.head
        prev: _SLLNode[T] | None = None
        while cur is not None:
            if cur.value == item:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

    def find(self, item: T) -> int:
        cur = self.head
        index = 0
        while cur is not None:
            if cur.value == item:
                return index
            cur = cur.next
            index += 1
        return -1

    def display(self) -> list[T]:
        out: list[T] = []
        cur = self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out


# --------------------------------------------------------------------------- #
# Doubly Linked List
# --------------------------------------------------------------------------- #


class _DLLNode(Generic[T]):
    __slots__ = ("value", "next", "prev")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _DLLNode[T] | None = None
        self.prev: _DLLNode[T] | None = None


class DoublyLinkedList(Generic[T]):
    """Doubly linked list with head and tail sentinels (as node references).

    Complexity:
        append: O(1) (tail). prepend: O(1) (head). delete: O(n). display: O(n).
    """

    def __init__(self) -> None:
        self.head: _DLLNode[T] | None = None
        self.tail: _DLLNode[T] | None = None

    def append(self, item: T) -> None:
        new_node = _DLLNode(item)
        if self.tail is None:
            self.head = self.tail = new_node
            return
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def prepend(self, item: T) -> None:
        new_node = _DLLNode(item)
        if self.head is None:
            self.head = self.tail = new_node
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def delete(self, item: T) -> bool:
        cur = self.head
        while cur is not None:
            if cur.value == item:
                if cur.prev is not None:
                    cur.prev.next = cur.next
                else:
                    self.head = cur.next
                if cur.next is not None:
                    cur.next.prev = cur.prev
                else:
                    self.tail = cur.prev
                return True
            cur = cur.next
        return False

    def display(self) -> list[T]:
        out: list[T] = []
        cur = self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out


# --------------------------------------------------------------------------- #
# Binary Search Tree (BST)
# --------------------------------------------------------------------------- #


class _BSTNode(Generic[T]):
    __slots__ = ("value", "left", "right")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.left: _BSTNode[T] | None = None
        self.right: _BSTNode[T] | None = None


class BinarySearchTree(Generic[T]):
    """Binary search tree. Allows duplicates inserted to the right.

    Complexity (balanced): O(log n) per op. Worst case (skewed): O(n).
    """

    def __init__(self) -> None:
        self.root: _BSTNode[T] | None = None

    def insert(self, value: T) -> None:
        if self.root is None:
            self.root = _BSTNode(value)
            return
        cur = self.root
        while True:
            if value < cur.value:
                if cur.left is None:
                    cur.left = _BSTNode(value)
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = _BSTNode(value)
                    return
                cur = cur.right

    def search(self, value: T) -> bool:
        cur = self.root
        while cur is not None:
            if value == cur.value:
                return True
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        return False

    def delete(self, value: T) -> bool:
        parent: _BSTNode[T] | None = None
        cur = self.root
        direction = ""  # "left" or "right" relative to parent
        while cur is not None and cur.value != value:
            parent = cur
            if value < cur.value:
                cur = cur.left
                direction = "left"
            else:
                cur = cur.right
                direction = "right"
        if cur is None:
            return False

        # Case 1: leaf
        if cur.left is None and cur.right is None:
            if parent is None:
                self.root = None
            elif direction == "left":
                parent.left = None
            else:
                parent.right = None
            return True

        # Case 2: one child
        if cur.left is None or cur.right is None:
            child = cur.left if cur.left is not None else cur.right
            if parent is None:
                self.root = child
            elif direction == "left":
                parent.left = child
            else:
                parent.right = child
            return True

        # Case 3: two children - inorder successor
        succ_parent = cur
        succ = cur.right
        while succ.left is not None:
            succ_parent = succ
            succ = succ.left
        cur.value = succ.value
        # Remove succ (which has at most a right child)
        if succ_parent.left is succ:
            succ_parent.left = succ.right
        else:
            succ_parent.right = succ.right
        return True

    def inorder(self) -> list[T]:
        out: list[T] = []

        def walk(node: _BSTNode[T] | None) -> None:
            if node is None:
                return
            walk(node.left)
            out.append(node.value)
            walk(node.right)

        walk(self.root)
        return out

    def preorder(self) -> list[T]:
        out: list[T] = []

        def walk(node: _BSTNode[T] | None) -> None:
            if node is None:
                return
            out.append(node.value)
            walk(node.left)
            walk(node.right)

        walk(self.root)
        return out

    def postorder(self) -> list[T]:
        out: list[T] = []

        def walk(node: _BSTNode[T] | None) -> None:
            if node is None:
                return
            walk(node.left)
            walk(node.right)
            out.append(node.value)

        walk(self.root)
        return out


# --------------------------------------------------------------------------- #
# Trie
# --------------------------------------------------------------------------- #


class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_end: bool = False


class Trie:
    """Standard trie for lowercase / arbitrary strings.

    Complexity:
        insert / search / starts_with: O(L) where L is the key length.
    """

    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# --------------------------------------------------------------------------- #
# Heaps
# --------------------------------------------------------------------------- #


class MinHeap(Generic[T]):
    """Binary min-heap backed by a list.

    Complexity:
        push: O(log n). pop: O(log n). peek: O(1). heapify: O(n).
    """

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._data: list[T] = list(items) if items is not None else []
        if self._data:
            self._heapify()

    def _heapify(self) -> None:
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i, n)

    def _sift_down(self, start: int, end: int) -> None:
        data = self._data
        root = start
        while True:
            child = 2 * root + 1
            if child >= end:
                return
            if child + 1 < end and data[child + 1] < data[child]:
                child += 1
            if data[child] < data[root]:
                data[root], data[child] = data[child], data[root]
                root = child
            else:
                return

    def _sift_up(self, idx: int) -> None:
        data = self._data
        while idx > 0:
            parent = (idx - 1) // 2
            if data[idx] < data[parent]:
                data[idx], data[parent] = data[parent], data[idx]
                idx = parent
            else:
                return

    def push(self, item: T) -> None:
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0, len(self._data))
        return top

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def size(self) -> int:
        return len(self._data)


class MaxHeap(Generic[T]):
    """Binary max-heap backed by a list.

    Complexity:
        push / pop: O(log n). peek: O(1). heapify: O(n).
    """

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._data: list[T] = list(items) if items is not None else []
        if self._data:
            self._heapify()

    def _heapify(self) -> None:
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i, n)

    def _sift_down(self, start: int, end: int) -> None:
        data = self._data
        root = start
        while True:
            child = 2 * root + 1
            if child >= end:
                return
            if child + 1 < end and data[child + 1] > data[child]:
                child += 1
            if data[child] > data[root]:
                data[root], data[child] = data[child], data[root]
                root = child
            else:
                return

    def _sift_up(self, idx: int) -> None:
        data = self._data
        while idx > 0:
            parent = (idx - 1) // 2
            if data[idx] > data[parent]:
                data[idx], data[parent] = data[parent], data[idx]
                idx = parent
            else:
                return

    def push(self, item: T) -> None:
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0, len(self._data))
        return top

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def size(self) -> int:
        return len(self._data)


# --------------------------------------------------------------------------- #
# Union-Find (Disjoint Set Union)
# --------------------------------------------------------------------------- #


class UnionFind(Generic[N]):
    """Disjoint-set union with path compression and union-by-rank.

    Complexity (amortized):
        find / union: inverse Ackermann, effectively O(1).
    """

    def __init__(self, elements: Iterable[N] | None = None) -> None:
        self.parent: dict[N, N] = {}
        self.rank: dict[N, int] = {}
        for e in elements or []:
            self.parent[e] = e
            self.rank[e] = 0

    def add(self, element: N) -> None:
        if element not in self.parent:
            self.parent[element] = element
            self.rank[element] = 0

    def find(self, x: N) -> N:
        parent = self.parent
        if x not in parent:
            raise KeyError(f"{x!r} not in UnionFind")
        root = x
        while parent[root] != root:
            root = parent[root]
        # Path compression
        while parent[x] != root:
            nxt = parent[x]
            parent[x] = root
            x = nxt
        return root

    def union(self, a: N, b: N) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

    def connected(self, a: N, b: N) -> bool:
        return self.find(a) == self.find(b)


# --------------------------------------------------------------------------- #
# Graph (Adjacency List)
# --------------------------------------------------------------------------- #


class Graph(Generic[N]):
    """Undirected/directed adjacency-list graph.

    Complexity:
        add_edge: O(1). bfs/dfs: O(V + E). Space: O(V + E).
    """

    def __init__(self, directed: bool = False) -> None:
        self.adj: dict[N, set[N]] = {}
        self.directed = directed

    def add_edge(self, u: N, v: N) -> None:
        self.adj.setdefault(u, set()).add(v)
        if not self.directed:
            self.adj.setdefault(v, set()).add(u)
        else:
            self.adj.setdefault(v, set())

    def bfs(self, start: N) -> list[N]:
        visited = [start]
        seen = {start}
        queue = _deque([start])
        while queue:
            u = queue.popleft()
            for v in self.adj.get(u, set()):
                if v not in seen:
                    seen.add(v)
                    visited.append(v)
                    queue.append(v)
        return visited

    def dfs(self, start: N) -> list[N]:
        visited = []
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            visited.append(u)
            for v in self.adj.get(u, set()):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return visited


# --------------------------------------------------------------------------- #
# LRU Cache
# --------------------------------------------------------------------------- #


class LRUCache(Generic[N, T]):
    """Least Recently Used cache using ``OrderedDict``.

    Complexity (amortized):
        get / put: O(1).
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._data: OrderedDict[N, T] = OrderedDict()

    def get(self, key: N) -> T:
        if key not in self._data:
            raise KeyError(key)
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: N, value: T) -> None:
        if key in self._data:
            self._data.move_to_end(key)
            self._data[key] = value
            return
        self._data[key] = value
        if len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data


__all__ = [
    "Stack",
    "Queue",
    "LinkedList",
    "DoublyLinkedList",
    "BinarySearchTree",
    "Trie",
    "MinHeap",
    "MaxHeap",
    "UnionFind",
    "Graph",
    "LRUCache",
]
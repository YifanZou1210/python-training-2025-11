
# Python Interview Questions & Coding Challenges - Session 2

## Concept Questions

* What is the difference between mutable and immutable data types in Python?
  * Mutable data types can be changed after creation (e.g., `list`, `dict`, `set`), while immutable data types cannot be changed once created (e.g., `int`, `float`, `str`, `tuple`).

* What's the difference between a list and a tuple in Python?
  * Lists are mutable and can be modified (append, remove, etc.), while tuples are immutable and cannot be changed after creation. Tuples are generally faster and can be used as dictionary keys.

* What's the difference between `list.append()`, `list.extend()`, and `list.insert()`?
  *  `append(x)` adds a single element `x` at the end; `extend(iterable)` adds all elements from an iterable to the end; `insert(index, x)` inserts element `x` at the specified index, shifting other elements.

* Explain the difference between shallow copy and deep copy between `list.copy()`, `list[:]`, and `copy.deepcopy()`
  *  `list.copy()` and `list[:]` create a **shallow copy**, meaning the outer list is copied but inner mutable objects are shared. `copy.deepcopy()` creates a **deep copy**, recursively copying all nested objects.

* What are the advantages and disadvantages of using set comprehensions vs converting a list comprehension to a set?
  *  Set comprehensions `{x for x in iterable}` directly create a set and remove duplicates efficiently, whereas `set([x for x in iterable])` first creates a list then converts it to a set (slightly less efficient). Both achieve similar results, but direct set comprehension is cleaner.

* What's the time complexity difference between checking membership (`in` operator) in a list vs a set?
  *  Membership check in a list is O(n) (linear search), while in a set it is O(1) on average (hash table lookup).

* Why are tuples immutable but you can still modify a list inside a tuple?
  *  Tuples are immutable regarding the tuple object itself (cannot add/remove/replace elements), but if a tuple contains mutable objects like lists, those objects can be modified because the tuple only holds references to them.

* What will `my_list[::2]`, `my_list[::-1]`, and `my_list[1::3]` return for `my_list = [0,1,2,3,4,5,6,7,8,9]`?
    * `my_list[::2]` → `[0, 2, 4, 6, 8]` (every 2nd element starting from index 0)
    * `my_list[::-1]` → `[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]` (reversed list)
    * `my_list[1::3]` → `[1, 4, 7]` (every 3rd element starting from index 1)

* What's the difference between `remove()`, `pop()`, and `del` for lists?
  * `remove(x)` deletes the first occurrence of value `x`; `pop(index)` removes and returns the element at `index` (default is last element); `del list[index]` deletes the element at `index` but does not return it. You can also use `del list[start:end]` to remove a slice.


---

## Coding Questions

### Coding Problem 1: Two Sum

**Problem:**  
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

**Description:**  
You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.

**Function Signature:**
```python
from collections import defaultdict
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List containing indices of the two numbers
    
    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
        
        >>> two_sum([3, 2, 4], 6)
        [1, 2]
    """
    dic = defaultdict(int)
    for i, e in enumerate(nums):
        if target-e in dic:
            return [i, dic[target-e]]
        dic[e] = i 

```

---

### Coding Problem 2: Longest Substring Without Repeating Characters

**Problem:**  
Given a string `s`, find the length of the longest substring without repeating characters.

**Description:**  
A substring is a contiguous sequence of characters within a string. You need to find the longest substring where all characters are unique (no character appears more than once).

**Function Signature:**
```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    
    Args:
        s: Input string
    
    Returns:
        Integer representing the length of longest substring
    
    Example:
        >>> length_of_longest_substring("abcabcbb")
        3  # "abc"
        
        >>> length_of_longest_substring("bbbbb")
        1  # "b"
        
        >>> length_of_longest_substring("pwwkew")
        3  # "wke"
    """
    l = 0
    mxl = 0 
    dic = defaultdict(int)
    for r in range(len(s)):
        dic[s[r]]+=1
        while r-l+1>len(dic):
            dic[s[l]]-=1
            if not dic[s[l]]:
                del dic[s[l]]
            l+=1
        if r-l+1==len(dic):
            mxl = max(mxl, r-l+1)
    return mxl
```

---

### Coding Problem 3: Product of Array Except Self

**Problem:**  
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

**Description:**  
You must write an algorithm that runs in O(n) time and without using the division operation. The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

**Function Signature:**
```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Calculate product of array except self.
    
    Args:
        nums: List of integers
    
    Returns:
        List where each element is the product of all other elements
    
    Example:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        # For index 0: 2*3*4 = 24
        # For index 1: 1*3*4 = 12
        # For index 2: 1*2*4 = 8
        # For index 3: 1*2*3 = 6
        
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    n = len(nums)
    pre, suf = [1]*n, [1]*n
    for i in range(1,n):
        pre[i] = pre[i-1]*nums[i-1]
    # print(pre)
    for i in range(n-2, -1, -1):
        suf[i] = suf[i+1]*nums[i+1]
    # print(suf)
    return [l*r for l, r in zip(pre, suf)]
```

---

### Coding Problem 4: Group Anagrams

**Problem:**  
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Description:**  
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once. For example, "listen" and "silent" are anagrams.

**Function Signature:**
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams together.
    
    Args:
        strs: List of strings
    
    Returns:
        List of lists, where each inner list contains anagrams
    
    Example:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        
        >>> group_anagrams([""])
        [[""]]
        
        >>> group_anagrams(["a"])
        [["a"]]
    """
    dic = defaultdict(list)
    for i, e in enumerate(strs):
        k = ''.join(sorted(e))
        dic[k].append(e)
    return [e for e in dic.values()]
```
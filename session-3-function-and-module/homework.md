# Python Coding Questions - Session 3: Recursion & Functions

## Concept Questions

* What is a lambda function, and how is it different from a regular function in Python?
  A lambda function is an anonymous, inline function defined with `lambda` keyword. It can take any number of arguments but has only one expression. Unlike regular functions defined with `def`, it does not have a name and cannot contain multiple statements.

* What is the difference between `*args` and `**kwargs` in function definitions?
  `*args` collects extra positional arguments as a tuple, while `**kwargs` collects extra keyword arguments as a dictionary.

* What is LEGB? Explain LEGB rule with a code example
  LEGB stands for Local, Enclosing, Global, Built-in, the order Python searches for variables. Example:

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # prints "local"
    inner()
outer()
```

* What is a closure in Python? How is it different from a regular nested function?
  A closure is a nested function that remembers values from its enclosing scope even after the outer function has finished execution. Regular nested functions do not retain these values once the outer function ends.

* What is the purpose of `if __name__ == "__main__":`?
  It ensures that a Python file runs certain code only when executed directly, not when imported as a module.

* Can you modify a global variable inside a function without using the `global` keyword?
  No, to reassign a global variable inside a function, you must use `global`. You can, however, mutate mutable objects like lists or dictionaries without `global`.

* In what order must you define parameters in a function signature?
  Positional arguments → default arguments → `*args` → keyword-only arguments → `**kwargs`.

* What is the difference between the `global` and `nonlocal` keywords?
  `global` allows modifying variables at the module level. `nonlocal` allows modifying variables in the nearest enclosing non-global scope.

* What is a common pitfall when using mutable default arguments?
  Using mutable defaults (like lists or dictionaries) can lead to unexpected shared state across function calls.

* What is a higher-order function? Give examples of built-in higher-order functions
  A higher-order function takes functions as arguments or returns a function. Examples: `map()`, `filter()`, `reduce()`, `sorted()` with key function.



---

## Coding Questions
### Coding Problem 1: Fibonacci Sequence with Optimization

**Problem:**  
Write a recursive function to calculate the nth Fibonacci number.

**Description:**  
The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1.
- Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
- Formula: F(n) = F(n-1) + F(n-2), where F(0) = 0 and F(1) = 1

**Requirements:**
- Must use recursion
- Must be efficient enough to handle large values (e.g., n = 50 or higher) without timing out
- Time complexity should be O(n), not O(2^n)
- Hint: Consider using memoization/caching to optimize your solution

**Function Signature:**
```python
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using optimized recursion.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed)
    
    Returns:
        The nth Fibonacci number
    
    Example:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(6)
        8
        >>> fibonacci(10)
        55
        >>> fibonacci(50)
        12586269025
    """
    if n == 0:
        return 0 
    return fibonacci(n-1)+fibonacci(n-2)
```

---

## Coding Problem 2: Maximum Value in Nested List

**Problem:**  
Write a recursive function to find the maximum value in a nested list structure of arbitrary depth.

**Description:**  
Given a list that may contain integers and other lists (which may also contain integers and lists), find the maximum integer value at any level of nesting. The list can be nested to any depth.

**Function Signature:**
```python
def find_max_nested(nested_list: list) -> int:
    """
    Find the maximum value in a nested list structure using recursion.
    
    Args:
        nested_list: A list containing integers and/or other nested lists
    
    Returns:
        The maximum integer value found at any nesting level
    
    Example:
        >>> find_max_nested([1, 2, 3, 4, 5])
        5
        
        >>> find_max_nested([1, [2, 3], 4, [5, [6, 7]]])
        7
        
        >>> find_max_nested([[1, 2], [3, [4, [5, 6]]], 7])
        7
        
        >>> find_max_nested([10, [20, [30, [40, [50]]]]])
        50
    """
    mx = float('-inf')
    for e in nested_list:
        if isinstance(e, int):
            mx = max(mx, e)
        elif isinstance(e, list):
            mx = max(mx, find_max_nested(e))
    return mx
```

---

## Coding Problem 3: Reverse String Using Recursion

**Problem:**  
Write a recursive function to reverse a string without using built-in reverse methods, slicing, or any iteration.

**Description:**  
Given a string, reverse it using only recursion. You cannot use:
- String slicing (`s[::-1]`)
- The `reversed()` function
- Any loops (`for`, `while`)
- The `.reverse()` method
- List comprehensions or any iterative constructs

You must solve this purely using recursive function calls.

**Function Signature:**
```python
def reverse_string(s: str) -> str:
    """
    Reverse a string using only recursion (no loops, slicing, or built-in reverse).
    
    Args:
        s: Input string to reverse
    
    Returns:
        Reversed string
    
    Example:
        >>> reverse_string("hello")
        "olleh"
        
        >>> reverse_string("Python")
        "nohtyP"
        
        >>> reverse_string("a")
        "a"
        
        >>> reverse_string("")
        ""
        
        >>> reverse_string("racecar")
        "racecar"
    """
    nums = list(s)
    def recur(l, r):
        if l >= r:      
            return
        nums[l], nums[r] = nums[r], nums[l]  # 交换
        recur(l + 1, r - 1)
    
    recur(0, len(nums) - 1)
    return ''.join(nums) 
```

---
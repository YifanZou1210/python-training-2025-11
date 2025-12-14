# Python Interview Questions & Coding Challenges - Session 1

## Concept Questions
* What is Python's main characteristic regarding syntax compared to other programming languages?
  * Python use indentation instead of curly brace `{}` as block boundary
* What are the basic data types available in Python?
  * `int, float, str, list, tuple, dic, set, bool, None`
* Why is indentation important in Python?
  * It's symbolized code structure, begining and ending of a code block, espescially for some nested blocks, like for-loop, closure, etc
* What happens when you try to mix incompatible data types in an operation?
  * raise type error when they mixed, we need use explicit type conversion, like use `int()` to transder `str` into `int`
* What is Git Flow?
  * a blue print or project branch version tracking for managing feature development and mvp upgrade, fix, agenda, etc, we use independent branch like /main, /dev, /fea, etc to control collaboration and release effect
* Explain the difference between `==` and `is` operators
  * `==` symbolizes liberal variable comparison 
  * `is` symbolizes reference address comparison in memory
* What's the difference between implicit and explicit type conversion?
  * former one used when one data type transfered to another one is safe and no data loss, like int to float
  * latter one used when user would like to use, like some conversion that implicit conversion fails, etc
* What's the difference between `if x:` and `if x == True:`?
  * former one checks if x condition is truth
  * latter one checks if x value equal to `True`, x type should be `boolean`

---

## Coding Questions

### Coding Problem 1: Palindrome Checker

**Problem:**  
Write a function that checks if a string is a palindrome (reads the same forwards and backwards), ignoring spaces, punctuation, and case.

**Description:**  
A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Your function should:
- Ignore spaces
- Ignore punctuation marks
- Be case-insensitive
- Return `True` if the string is a palindrome, `False` otherwise

**Function Signature:**
```python
def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s (str): Input string to check
    
    Returns:
        bool: True if palindrome, False otherwise
    
    Example:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    s = s.strip().lower()
    l, r = 0, len(s)-1
    while l<=r:
        if not s[l].isalnum():
          l+=1
        if not s[r].isalnum():
          r-=1
        if s[l]==s[r]:
          l+=1
          r-=1
        else:
          return False 
    return True 
```
---

### Coding Problem 2: Valid Parentheses

**Problem:**  
Given a string containing just the characters `'(', ')', '{', '}', '[', ']'`, determine if the input string is valid.

**Description:**  
A string is considered valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type
4. Every open bracket must have a corresponding close bracket

**Function Signature:**
```python
def is_valid_parentheses(s: str) -> bool:
    """
    Check if a string has valid parentheses.
    
    Args:
        s (str): String containing only '(', ')', '{', '}', '[', ']'
    
    Returns:
        bool: True if parentheses are valid, False otherwise
    
    Example:
        >>> is_valid_parentheses("()")
        True
        >>> is_valid_parentheses("()[]{}")
        True
        >>> is_valid_parentheses("(]")
        False
    """
    if not s:
        return True 
    dic = {'(':')', '{':'}', '[':']'}
    stk = [] 
    for e in s:
        if stk and dic[stk[-1]]==e:
            stk.pop()
        else:
            stk.append(e)
    return not stk
```
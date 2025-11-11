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


----


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

----

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


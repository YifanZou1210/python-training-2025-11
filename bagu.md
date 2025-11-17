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

---
# session-4-oop

**1. What are the four principles of OOP?**
* **Encapsulation** – Hides internal data; accessed through public methods or properties.
* **Abstraction** – Exposes only essential behavior; hides complexity.
* **Inheritance** – Allows classes to derive and extend functionality from a base class.
* **Polymorphism** – Enables different classes to define methods with the same name but different behaviors.

**Example:**

```python
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof"

class Cat(Animal):
    def speak(self): return "Meow"
```


**2. What's the difference between `__str__` and `__repr__` magic methods?**


* `__str__`: For **readable** string representation (used by `print()` or `str()`).
* `__repr__`: For **developer/debug** representation (used by `repr()` or console).

**Example:**

```python
class Book:
    def __str__(self):
        return "Readable: Book Info"
    def __repr__(self):
        return "Book(title='X', author='Y')"
```


**3. How do magic methods like `__eq__` affect object comparison?**

* `__eq__` defines how objects are compared using `==`.
* Without it, equality compares **object identity (memory address)** by default.

**Example:**

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```


**4. Explain the difference between `@classmethod` and `@staticmethod`.**

* `@classmethod`: Receives the **class itself (`cls`)** as the first argument; can modify class state.
* `@staticmethod`: Receives **no automatic first argument**; behaves like a regular function in a class.

**Example:**

```python
class Example:
    count = 0

    @classmethod
    def set_count(cls, value):
        cls.count = value

    @staticmethod
    def add(x, y):
        return x + y
```


**5. What are property decorators in Python?**

 
Used to define **getter/setter/deleter** for attributes — enabling **controlled access** like Java getters/setters.

**Example:**

```python
class Person:
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Invalid age")
        self._age = value
```


**6. What's the difference between public, protected (`_`), and private (`__`) attributes?**

 

| Type      | Prefix | Access Level                               | Example         |
| --------- | ------ | ------------------------------------------ | --------------- |
| Public    | none   | Accessible anywhere                        | `self.name`     |
| Protected | `_`    | Conventionally internal (not enforced)     | `self._balance` |
| Private   | `__`   | Name-mangled; accessible only within class | `self.__secret` |


**7. What's Singleton pattern? How to implement it?**

 
Ensures **only one instance** of a class exists.

**Example:**

```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```


**8. What's Factory pattern? How to implement it?**

 
Provides a **method to create objects** without specifying exact class names.

**Example:**

```python
class ShapeFactory:
    def get_shape(self, shape_type):
        if shape_type == "circle": return Circle()
        if shape_type == "square": return Square()
```


**9. What is the `self` parameter?**

 
Represents the **current instance** of a class; used to access instance variables and methods.

**Example:**

```python
class Car:
    def __init__(self, brand):
        self.brand = brand
```


**10. What are abstract base classes (ABC) in Python?**

 
Define **interfaces** that subclasses must implement, using `abc` module.

**Example:**

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass
```

---

# session-5-advanced concept of python 

* **What is a decorator in Python, and where is it used?**
  A callable that wraps another function or method to modify or enhance its behavior without changing its code; commonly used for logging, authentication, caching, or timing.
* **What's the difference between a generator and a regular function that returns a list?**
  A generator yields items one at a time lazily, consuming less memory; a regular function builds and returns the entire list at once, consuming memory for all elements immediately.
* **When would you choose generators over lists, and what are the memory implications?**
  Use generators for large or infinite sequences to avoid storing all elements in memory; memory usage is minimal since only the current element is kept.
* **Explain the difference between threading, multiprocessing, and asyncio in Python**
  Threading: multiple threads share memory, good for IO-bound; Multiprocessing: separate processes, each with own memory, bypasses GIL, good for CPU-bound; Asyncio: single-threaded cooperative concurrency, efficient for high-latency IO tasks.
* **What is the Global Interpreter Lock (GIL)? How does it affect threading and multiprocessing?**
  GIL allows only one Python bytecode instruction to execute at a time per process; threading is limited for CPU-bound tasks, multiprocessing bypasses GIL and can fully use multiple cores.
* **When to use threading, asyncio, multiprocess?**
  Threading: IO-bound tasks; Asyncio: high-concurrency IO tasks; Multiprocessing: CPU-bound tasks needing parallel execution.
* **What are CPU-bound vs IO-bound tasks?**
  CPU-bound: tasks limited by computation speed; IO-bound: tasks limited by input/output latency, e.g., network, disk.
* **What's the difference between yield and return in a function**
  `return` sends a final value and exits the function; `yield` produces a value and pauses function, allowing iteration to resume later.
* **What's the difference between using open() with explicit close() vs using the with statement**
  Explicit close() requires manual cleanup; `with` ensures automatic resource release even if exceptions occur.
* **How to handle exceptions? Why is exception handling important?**
  Use try-except blocks to catch and respond to errors; important to prevent crashes, maintain program flow, and provide meaningful error messages.

---

# session-6-db

- What are primary keys and foreign keys? How are they used in relational databases?
  - A primary key is a column or set of columns in a table that uniquely identifies each row. A foreign key is a column or set of columns in one table that refers to the primary key in another table, establishing a relationship between the two tables. They are used to enforce data integrity and relational links between tables.

- What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN
  - INNER JOIN returns only the rows that have matching values in both tables. LEFT JOIN returns all rows from the left table and the matched rows from the right table, with NULLs for unmatched rows. FULL OUTER JOIN returns all rows when there is a match in either table, filling in NULLs for missing matches.

- What is normalization? 数据库范式
  - Normalization is the process of organizing database tables and columns to reduce redundancy and improve data integrity, typically through a series of normal forms (1NF first normal form, 2NF, 3NF, etc.).

- What are the different types of database relationships (1:1, 1:many, many:many) and how do you implement them in SQL?
  - 1:1 relationship: each row in Table A is linked to exactly one row in Table B. Implemented by having a foreign key in either table referencing the other’s primary key with UNIQUE constraint.
  - 1:many relationship: each row in Table A can be linked to multiple rows in Table B. Implemented by having a foreign key in the “many” table referencing the primary key of the “one” table.
  - Many:many relationship: rows in Table A can be linked to multiple rows in Table B and vice versa. Implemented using a junction table with foreign keys referencing both tables.

- What are transactions and isolation levels? Explain the problems each isolation level solves.
  - Transactions are sequences of database operations executed as a single unit. Isolation levels control visibility of changes between concurrent transactions.

  * Read Uncommitted: allows dirty reads; solves no problem, lowest isolation.
  * Read Committed: prevents dirty reads; solves the dirty read problem.
  * Repeatable Read: prevents dirty and non-repeatable reads; solves dirty and non-repeatable read problems.
  * Serializable: prevents dirty, non-repeatable, and phantom reads; ensures full isolation, highest level.

- What's the difference between PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints?
  - PRIMARY KEY enforces unique and non-null values for the column(s). UNIQUE enforces uniqueness but allows one NULL per column (depending on DBMS). FOREIGN KEY enforces referential integrity by linking to a primary key in another table.

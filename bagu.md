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

---
# session-7-database-advanced 

### 1. 视图、物化视图、表的区别

What's difference between View, Materialized View, and Table

* **表（Table）**：真实存储数据。
* **视图（View）**：不存数据，实时查询底层 SQL。
* **物化视图（Materialized View）**：存储查询结果，需要刷新。

A table actually stores your data; it's the real thing. A view is just a saved query—like a lens that shows data from tables but doesn’t store anything itself. A materialized view is basically a precomputed view where the results are stored like a snapshot, so reads are faster but you need to refresh it. You’d use tables for your real data, views to simplify queries, and materialized views for heavy analytical reads where speed matters.

### 2. 什么是 ORM？为什么需要 ORM？

What is ORM? Why do we need ORM?

ORM 将数据库表映射为编程语言对象，让开发者用对象操作数据而不写 SQL。
优点：减少 SQL、避免注入、管理事务与关系、跨数据库迁移容易。

ORM is a way to map your code’s classes to database tables so you can work with data using objects instead of writing SQL everywhere. It helps keep code cleaner, safer, and easier to maintain, especially in large codebases. You still need SQL sometimes, but ORM handles the boring boilerplate for you.


### 3. ACID 属性解释

Explain the ACID Properties

* **原子性 atomicity**：全部成功或全部失败
* **一致性 consistency**：数据规则不被破坏
* **隔离性 isolation**：并发事务互不干扰
* **持久性 durability**：提交后数据不会丢失

确保数据库不会出现脏写、部分更新或数据丢失。

ACID means a transaction is all-or-nothing (Atomic), always leaves data valid (Consistent), doesn’t get messed up by other transactions (Isolated), and stays saved once committed (Durable). Together, these properties make sure your database doesn’t end up in a broken or half-updated state.


### 4. CAP 定理

Explain the CAP Theorem


分布式系统无法同时满足：一致性、可用性、分区容错性；
实际中必须在 **CP**（放弃可用） 或 **AP**（放弃强一致）中选择。

CAP says a distributed system can’t give you perfect Consistency, Availability, and Partition Tolerance at the same time. Since network partitions always happen, you must pick between stronger consistency (CP) or higher availability (AP). It’s a trade-off, not a bug.


### 5. SQL 与 NoSQL 的使用场景

When choose SQL vs NoSQL?

SQL：结构化数据、复杂查询、事务要求强（银行、订单）。
NoSQL：超大规模、灵活结构、高并发读写（日志、社交、缓存）。

SQL fits systems with structured data, clear relationships, and strong transaction requirements. NoSQL shines when you need huge scale, flexible data shapes, or extremely high read/write throughput. It's more about choosing the right tool for the pattern of your data and traffic.

---

### 6. 什么是最终一致性

What is Eventual Consistency?

*Eventual consistency means updates might not show up instantly everywhere, but if nothing else changes, all nodes will eventually catch up and show the same data. It trades immediate correctness for better performance and availability.

---

### 7. 分布式系统的一致性模型

What's difference between Consistency Models: Strong, Weak, Eventual

* **强一致性**：每次读取都是最新值
* **弱一致性**：不保证读取最新值
* **最终一致性**：短期不一致，最终收敛

Strong consistency means every read sees the latest write. Weak consistency makes no such promise. Eventual consistency is in the middle—you might read stale data now, but the system will synchronize over time. It's about choosing speed vs correctness.


### 8. 横向扩展 vs 纵向扩展

What's difference between Horizontal vs Vertical Scaling

* **横向扩展**：加机器；分布式扩容；可线性扩展。
* **纵向扩展**：提升单机性能；受硬件极限限制。

* **Horizontal**: Add more servers
* **Vertical**: Add more CPU/RAM to one machine
Vertical scaling means giving a single machine more power. Horizontal scaling means adding more machines to share the load. Scaling out is more flexible long-term but requires more distributed-system thinking.

### 9. MongoDB 如何支持 ACID

### (How does MongoDB handle ACID?)

**答案（中文）**

* 单文档天然 ACID
* 多文档事务（4.0+）支持完整 ACID
* 分片集群仍是最终一致（复制延迟）
* 事务开销大，仅在需要时使用

**Answer (English)**

* Single-document ops are inherently ACID
* Multi-doc ACID transactions supported since 4.0
* Sharded clusters remain eventually consistent
* Transactions are expensive; use only when needed
MongoDB is fully ACID for single-document updates. Since version 4.0 it also supports multi-document transactions, making it behave much more like a relational DB when needed. But multi-document transactions cost performance, so MongoDB encourages embedding related data in one document.


### 10. 什么是分片？和分区有何区别？

What is Sharding? How does it differ from Partitioning?

* **分片**：把数据拆到多台服务器（分布式横向扩展）
* **分区**：把单表拆成多个逻辑/物理分区（同一服务器内部）

**区别：**分片=跨机器；分区=单机内部。

* **Sharding**: Split data across multiple servers
* **Partitioning**: Split data within one server/table

Partitioning splits data inside one database instance. Sharding splits data across multiple servers, each holding part of the dataset. Sharding is basically distributed partitioning and helps scale out when one machine can’t handle the load.

---
# session-8-http-flask
**How does routing work in Flask?**

Routing in Flask works by associating URLs with Python functions using decorators like `@app.route('/path')`. When a request matches the URL pattern, Flask calls the corresponding function to handle it.

**What is restful service**

A RESTful service is a web service that follows REST principles: stateless communication, resource-based URLs, standard HTTP methods (GET, POST, PUT, DELETE), and representation in JSON or XML.

**What are the categories of HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx)? Provide examples for each.**

* 1xx: Informational (e.g., 100 Continue)
* 2xx: Success (e.g., 200 OK, 201 Created)
* 3xx: Redirection (e.g., 301 Moved Permanently, 302 Found)
* 4xx: Client error (e.g., 400 Bad Request, 404 Not Found)
* 5xx: Server error (e.g., 500 Internal Server Error, 503 Service Unavailable)

**What is HTTP and how does it work**

HTTP (Hypertext Transfer Protocol) is a request-response protocol where clients (browsers, apps) send requests to servers over TCP, and servers respond with status codes and content.

**Explain the concept of idempotency in HTTP methods**

Idempotency means that performing the same HTTP request multiple times has the same effect as performing it once. For example, GET, PUT, and DELETE are idempotent; POST is generally not.

**Explain the difference between HTTP and HTTPS**

HTTP is unsecured and sends data in plaintext; HTTPS uses SSL/TLS to encrypt communication, ensuring confidentiality and integrity.

**Design a RESTful API for a blogging platform**

* `GET /posts` → list all posts
* `GET /posts/<id>` → get a single post
* `POST /posts` → create a new post
* `PUT /posts/<id>` → update a post
* `DELETE /posts/<id>` → delete a post
* `GET /posts/<id>/comments` → list comments for a post

**What is the MVC architecture**

MVC architecture separates an application into:

* Model → data and business logic
* View → user interface
* Controller → handles input and updates Model/View

**What are Flask's request objects**

Flask’s request objects encapsulate HTTP request data, including:

* `request.args` → query parameters
* `request.form` → form data
* `request.json` → JSON payload
* `request.headers` → HTTP headers
* `request.method` → HTTP method used


---
# session-9-authN-authZ

**Difference between authentication and authorization**
Authentication verifies who a user is (identity check), while authorization determines what an authenticated user is allowed to do (permissions/access control).

**What are HTTP cookies? How do they work and what are their main use cases?**
HTTP cookies are small pieces of data stored by the browser and sent with requests to the server. They work by the server sending `Set-Cookie` headers, which the browser stores and includes in subsequent requests. Main use cases: session tracking, user preferences, authentication tokens.

**What are the limitations of cookies**

* Limited size (~4KB per cookie)
* Sent with every HTTP request (can increase bandwidth)
* Security risks: susceptible to XSS, CSRF if not configured properly
* Domain and path restrictions can complicate usage

**What is JWT and how does it work?**
JWT (JSON Web Token) is a compact, self-contained token that encodes claims in JSON, signed using a secret or public/private key. It works by the server issuing a token after authentication; clients include the token in requests for stateless verification without server-side session storage.

**What are the advantages and disadvantages of using JWT compared to traditional session-based authentication?**
Advantages:

* Stateless: no server-side session storage required
* Portable across domains and microservices
* Can include custom claims

Disadvantages:

* Token revocation is harder
* Token size larger than session ID
* Sensitive info must be encrypted if included

**How do you invalidate or blacklist JWT tokens?**

* Maintain a server-side blacklist of token IDs until expiration
* Issue short-lived access tokens and use refresh tokens
* Change the signing key to invalidate all existing tokens

**What is password hashing and why is it important?**
Password hashing converts a plaintext password into a fixed-length, irreversible string using algorithms like bcrypt or Argon2. It is important to protect passwords in case of database breaches and prevent storing plaintext passwords.

**What is the access / refresh token pattern**

* **Access token**: short-lived token for accessing protected resources
* **Refresh token**: long-lived token used to obtain new access tokens without re-authentication
* Pattern improves security and reduces the need to store long-lived tokens on clients

**What is the Oauth2 flow**
OAuth2 flow allows third-party apps to access resources on behalf of users without sharing passwords. Common flows:

* **Authorization Code**: app gets a code via user authorization, then exchanges it for tokens
* **Implicit**: token returned directly in URL fragment (mostly deprecated)
* **Resource Owner Password Credentials**: user provides credentials to app (legacy, less secure)
* **Client Credentials**: app accesses its own resources, no user involved



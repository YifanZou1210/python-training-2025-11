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

* **表（Table）**：真实存储数据，增删查改都是直接修改表中数据
* **视图（View）**：不存数据，只存储sql定义， 查询视图时会实时查询执行他背后的sql
* **物化视图（Materialized View）**：存储sql查询结果，类似缓存表，查询速度快，因为结果是premake的， 但是数据可能过时，需要刷新，常用于分析、报表、复杂聚类查询

- Table is physically stored data on disk, which implementation data changes through insertion, deletion, addition, etc, the primary storage structure in a database
- View does not store data, only store sql definition, each time we query a view, the database will rerun sql on underlying tables
- Materialized View store actual query res physically, like a cached table, it query very fast cuz res are precomputed, but data can be stale, needs to refresh frequently

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

HTTP is unsecured and sends data in plaintext; HTTPS uses SSL/TLS to encrypt communication, ensuring safety and integrity.

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

jwt是一种 无状态的令牌格式，用于 用户认证 与 授权。服务端不保存 session，所有信息都编码在 token 内，由客户端携带。
组成： header+payload+signature 
工作流程： 
- 用户登录并输入正确凭证。
- 服务端验证密码 → 生成 JWT（含用户 ID、角色等）。
- 客户端保存 token（通常在 localStorage 或 HTTP-only Cookie）。
- 客户端后续请求在 Authorization: Bearer <token> 中发送 JWT。
- 服务端收到请求：
- 验证签名
- 检查过期时间
- 解出用户角色/权限
- 如果验证成功 → 放行，否则返回 401。

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

---

# session-10-fast api 
1. **Explain the difference between def and async def in FastAPI route handlers. When should you use each?**

   * `def` defines a synchronous function; it blocks the event loop while executing.
   * `async def` defines an asynchronous coroutine; allows concurrent request handling when awaiting I/O.
   * **Use `async def`** for I/O-bound operations (DB queries, HTTP calls); use `def` for CPU-bound or synchronous code.

2. **What is dependency injection in FastAPI and how does it work behind the scene?**

   * Dependencies are functions that provide values or setup/cleanup for route handlers.
   * Declared using `Depends()`.
   * **Behind the scenes:** FastAPI builds a dependency graph per request, resolves it recursively, and injects returned values into handler parameters.

3. **How does FastAPI achieve automatic API documentation?**

   * Generates OpenAPI schema from route definitions, type hints, and Pydantic models.
   * Exposes Swagger UI (`/docs`) and ReDoc (`/redoc`) automatically.
   * Type hints + Pydantic models allow FastAPI to infer request/response structure and validation for docs.

4. **Explain the difference between Path, Query, Header, Body, and Cookie parameters in FastAPI.**

   * `Path`: URL path variables, required (`/items/{id}`).
   * `Query`: query string parameters, optional by default (`?q=test`).
   * `Header`: HTTP headers (`X-Token`).
   * `Body`: request body, usually JSON; often Pydantic models.
   * `Cookie`: HTTP cookies.
   * FastAPI uses parameter type and `Path()`, `Query()`, etc., to extract values from requests.

5. **What is the purpose of Pydantic models in FastAPI? How do they differ from SQLAlchemy/SQLModel database models?**

   * Pydantic: validate and serialize data, parse request/response JSON; not tied to DB.
   * SQLAlchemy/SQLModel: define database tables, ORM mapping, handle persistence.
   * Pydantic focuses on input/output structure; SQLAlchemy focuses on storage.

6. **Explain how FastAPI's dependency caching works within a single request. Why is this important?**

   * Dependencies are cached once per request; repeated `Depends()` calls with the same function return the same object.
   * Ensures efficiency and consistency, e.g., DB session reused across multiple parameters/routes in a request.

7. **How does FastAPI handle request validation and what happens when validation fails? How can you customize error responses?**

   * Validates requests automatically via Pydantic and type hints.
   * On failure, returns `422 Unprocessable Entity` with details.
   * Customize errors using `@app.exception_handler(RequestValidationError)`.

8. **Explain the difference between using Annotated[Session, Depends(get_db)] vs Session = Depends(get_db) for type hints. Which is recommended and why?**

   * `Annotated[Session, Depends(get_db)]`: separates type hint from dependency injection; preferred for clarity and type checking.
   * `Session = Depends(get_db)`: mixes type hint and dependency.
   * **Recommendation:** use `Annotated` for clearer typing and better IDE/type-checker support.

---
# session-11-fast api

1. **What's the difference between using `requests` and `httpx` for making HTTP calls in FastAPI, and why is `httpx` preferred in async contexts?**

   `requests` is a synchronous HTTP client; every request blocks the thread until the response arrives. `httpx` supports both synchronous and asynchronous requests, allowing `async`/`await` syntax. In async FastAPI routes, `httpx` is preferred because it allows non-blocking calls, letting other coroutines run concurrently and improving performance under high I/O workloads.

---

2. **What are the key differences in the database URL connection string when migrating from sync SQLAlchemy to async SQLAlchemy, and what driver changes are required for PostgreSQL?**
   For async SQLAlchemy with PostgreSQL, you need an async driver like `asyncpg`. The URL changes from:

```
postgresql://user:pass@host:port/dbname
```

to

```
postgresql+asyncpg://user:pass@host:port/dbname
```

The `+asyncpg` tells SQLAlchemy to use the async driver, enabling `async` sessions with `AsyncSession`.

---

3. **What is ASGI (Asynchronous Server Gateway Interface) and how does it differ from WSGI?**
   WSGI is a synchronous interface for Python web servers and apps, suitable for blocking code. ASGI is asynchronous, supporting `async`/`await`, WebSockets, and long-lived connections. ASGI allows concurrent handling of multiple requests without blocking threads, which is essential for modern async frameworks like FastAPI.

---

4. **How is FastAPI different from Flask?**

* FastAPI is **async-first** and uses Python type hints for automatic request validation, serialization, and OpenAPI generation.
* Flask is synchronous, minimalistic, and requires manual validation and documentation.
* FastAPI has built-in support for modern features like async routes, dependency injection, and automatic docs via Swagger/OpenAPI, making it better suited for high-performance APIs.

---

5. **Explain the difference between `response_model`, `response_model_exclude`, and `response_model_include` in FastAPI route decorators. When would you use each?**

* `response_model`: defines the Pydantic model used to serialize the response; validates and formats outgoing data.
* `response_model_include`: specifies which fields to include from the response model; useful for partial responses.
* `response_model_exclude`: specifies fields to exclude from the response; useful for hiding sensitive data like passwords.

Example use:

* `response_model` → standard API output.
* `response_model_include` → only return `id` and `name`.
* `response_model_exclude` → exclude `password` or `secret_token`.

---

6. **How do you implement JWT authentication in FastAPI**

* Use `JWT`  to encode/dec ode tokens.
* Create a login route that generates a JWT with user info and expiry.
* Define a dependency that extracts and verifies the token from `Authorization` header.
* Use the dependency in protected routes to access user information.
* Example:

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```
**General Procedure to Implement JWT Authentication in FastAPI:**

1. **Create a login endpoint** that accepts user credentials, like password or username.
2. **Verify credentials** against your database or user store, check the user exists in db or not, compare hash password.
3. **Generate a JWT token** with user info and expiration using a secret key and algorithm hs256.
4. **Return the token** to the client.
5. **Create a dependency** (e.g., `get_current_user`) that reads and validates the token from the `Authorization` header.
6. **Apply the dependency** to protected routes to enforce authentication.
7. **Optionally handle token expiration and refresh logic**.


---

7. **How does FastAPI handle synchronous functions differently?**

* FastAPI can run synchronous functions in a **thread pool** using `starlette.concurrency.run_in_threadpool`.
* Sync functions **block the thread** they're running in, but the event loop continues handling other async tasks in other threads.
* Async functions are preferred for I/O-bound operations, but sync functions still work for CPU-bound tasks or libraries without async support.

---
# session-12-django

**What is Django's MTV pattern?**

Django follows the MTV (Model-Template-View) architecture:

* **Model**: Defines the data structure and database schema.
* **Template**: Handles presentation logic, rendering HTML to the user.
* **View**: Contains the business logic, handles requests, fetches data from models, and renders templates.

---

**What's the difference between blank=True and null=True?**

* **null=True**: Database-related; allows storing `NULL` in the database.
* **blank=True**: Form/validation-related; allows form fields to be left empty.
  Typically, for string-based fields, use `blank=True, null=False`.

---

**What's the difference between auto_now and auto_now_add?**

* **auto_now_add=True**: Sets the field to the current timestamp when the object is first created.
* **auto_now=True**: Updates the field to the current timestamp every time the object is saved.

---

**What are Django migrations and why are they important?**

* Migrations are Django’s way of propagating model changes to the database schema.
* They allow version control of the database structure, easy schema updates, and consistency across environments.

---

**What is the N+1 query problem? How to avoid it in Django?**

* **N+1 problem**: Querying a list of objects (N) and then accessing a related field causes an additional query per object, leading to N+1 queries.
* **Solution in Django**: Use `select_related` for foreign key/one-to-one relations or `prefetch_related` for many-to-many/one-to-many relations to fetch related objects efficiently.

---

**What is the Meta class in Django models?**

* `Meta` is an inner class in a Django model used to define model metadata, such as:

    * Database table name (`db_table`)
    * Ordering of results (`ordering`)
    * Verbose name (`verbose_name`)
    * Unique constraints (`unique_together`)

---

**What's the purpose of str() method in models?**

* The `__str__` method defines the human-readable string representation of a model instance, used in admin, shell, and templates for easier identification.


---

# Session14 - advanced web development 


 1. Explain the WebSocket protocol and how it differs from HTTP polling and long polling

**Answer:**

1. **WebSocket 协议**

    * 建立一次 **持久化的全双工连接**
    * 客户端与服务器都可以主动发送消息
    * 使用 HTTP 握手升级协议 → 之后不再需要重复建立连接
    * 低延迟、高实时性（如聊天、协作编辑、行情推送）

2. **与 Polling、Long Polling 的区别**

    * **HTTP Polling**

        * 客户端定期发请求(如每 1s)
        * 非实时，高网络开销
    * **HTTP Long Polling**

        * 客户端发请求 → 服务端保持连接直到有数据
        * 半实时，但仍是 *request-response*
    * **WebSocket**

        * 一次连接，多次通信
        * 真正的双向实时推送
        * 网络开销最小、延迟最低

---

2. What caching strategy would you use for frequently accessed but slowly changing data

**Answer:**

1. **Cache-aside (Lazy Loading)** 最常用

    * 读取：先查缓存，不在再查数据库 → 放入缓存
    * 更新：先更新数据库，再删除缓存
    * 适用于：**读多、写少、数据变化慢**
    * 示例：商品详情页、配置、排行榜

2. 可搭配：

    * **TTL（过期时间）**
    * **定期 refresh 预热**
    * **Redis + JSON serialization**

---

 3. Explain the difference between cache-aside, write-through, and write-behind caching patterns

**Answer:**

1. **Cache-aside（旁路缓存）**

    * 读时加载，写时更新 DB + 删除缓存
    * 优点：最灵活
    * 缺点：写不一致风险（已被业界成熟方案避免）

2. **Write-through（写穿）**

    * 写 → 同时写缓存 & DB
    * 数据绝对一致
    * 缺点：写性能慢

3. **Write-behind（写回）**

    * 写 → 写缓存；DB 在后台异步刷新
    * 写性能最快
    * 缺点：DB 与缓存**强一致性无法保证**

---

 4. Describe the differences between RabbitMQ, Kafka, and SQS

**Answer:**

1. **RabbitMQ**

    * 消息队列（MQ）
    * 强调**可靠投递、复杂路由（exchange）、确认机制**
    * 适用于：短消息、任务队列、同步解耦

2. **Kafka**

    * 分布式流处理平台
    * 强调**高吞吐、可持久化日志存储、分区**
    * 适用于：日志、事件流、真实时间大数据处理

3. **AWS SQS**

    * 托管队列服务
    * 简单、无需管理 Broker
    * 适用于：云原生微服务解耦，低维护成本

---

 5. What are message queues and why are they important in distributed systems?

**Answer:**

1. **定义**

    * 异步通信机制，通过队列传递消息，不要求双方同时在线

2. **重要性**

    * **解耦**：服务独立
    * **削峰填谷**：缓冲流量
    * **异步任务**：提高响应速度
    * **重试机制**：提高可靠性
    * **容错性**：服务宕机不会丢消息（视 MQ 具体配置）

---

 6. How would you implement a retry mechanism with exponential backoff for failed message processing?

**Answer:**

1. **步骤**

    * 捕获处理失败
    * 重试次数限制（如 3 次）
    * 使用 **2^n × baseDelay** 进行等待
    * 重试仍失败 → 进入 DLQ

2. **伪代码**

```python
delay = base
for attempt in range(max_retries):
    try:
        process(msg)
        break
    except:
        sleep(delay)
        delay *= 2
else:
    send_to_dlq(msg)
```

---

 7. Explain the concept of dead letter queues and when you'd use them

**Answer:**

1. **定义**

    * Dead Letter Queue (DLQ) 是存放 **处理失败消息** 的特殊队列

2. **用途**

    * 重试超过次数
    * 消息格式错误
    * 无法被消费者处理
    * 需要人工检查与修复

3. **重要性**

    * 确保系统不因为坏消息而卡死
    * 提供可审计性
    * 确保主队列性能不受损

---

 8. How does FastAPI handle synchronous functions differently?

**Answer:**

1. **Sync（普通函数）**

    * FastAPI 会在 **ThreadPoolExecutor** 中运行
    * 适用于：CPU-bound、阻塞 IO 的代码
    * 每个请求占用一个线程

2. **Async（async def）**

    * 运行在 event loop
    * 适用于：非阻塞 IO、HTTP 调用
    * 并发更高，资源消耗更低

3. **FastAPI 区别处理**

    * 根据函数类型自动选择执行策略
    * 避免阻塞 event loop

---

## English Version


1. **Explain the WebSocket protocol and how it differs from HTTP polling and long polling**

**Answer:**
WebSocket is a full-duplex communication protocol built on top of TCP. After an initial HTTP handshake, the connection upgrades to WebSocket and stays open, allowing both client and server to push messages at any time.

**Key differences:**

1. **HTTP Polling**

    * Client repeatedly sends requests (e.g., every 1s).
    * Highly inefficient; many requests return no new data.
2. **Long Polling**

    * Client sends a request and the server holds it until new data is available.
    * Better than polling, but still reopens HTTP connections repeatedly.
3. **WebSocket**

    * One persistent connection.
    * No repeated HTTP overhead.
    * Real-time, bidirectional updates.

---

2. **What caching strategy would you use for frequently accessed but slowly changing data?**

**Answer:**
Use a **cache-aside strategy with TTL (time-to-live)**.

**Why this fits:**

* The data is read often → caching avoids unnecessary database hits.
* The data changes infrequently → TTL ensures cache eventually refreshes.
* Cache-aside gives full control over when to reload.

Typical TTL: **5–30 minutes**, depending on consistency requirements.

---

3. **Explain the difference between cache-aside, write-through, and write-behind patterns**

**Answer:**

1. **Cache-Aside (Lazy Loading)**

    * Application reads from cache first.
    * If missing → fetch from DB → store in cache.
    * Writes go to DB first, cache is updated or invalidated.
    * Pros: simple, flexible.
    * Cons: first read is slow (“cache miss”).

2. **Write-Through**

    * All writes go to cache first; cache immediately writes to DB.
    * Read always comes from cache.
    * Pros: data in cache is always consistent.
    * Cons: writes become slower.

3. **Write-Behind (Write-Back)**

    * Application writes to cache only; cache asynchronously flushes changes to DB.
    * Pros: very fast writes.
    * Cons: risk of data loss if cache dies before flushing.

---

4. **Describe RabbitMQ, Kafka, and SQS in terms of use cases and guarantees**

**Answer:**
**RabbitMQ**

* **Type:** Message broker, queue-based
* **Use cases:** Task queues, request/response, events requiring ordering
* **Guarantee:** At-least-once delivery, routing flexibility

**Kafka**

* **Type:** Distributed log streaming platform
* **Use cases:** High-throughput event streaming, logs, analytics pipelines
* **Guarantee:** Durable log with partition ordering; consumer groups

**SQS (AWS)**

* **Type:** Fully managed queue service
* **Use cases:** Simple decoupling between microservices
* **Guarantee:** At-least-once; FIFO option available

---

5. **What are message queues and why are they important in distributed systems?**

**Answer:**
Message queues decouple producers and consumers by allowing messages to be stored temporarily until processed.

**Importance:**

* Smooth out traffic spikes
* Prevent service overload
* Improve fault tolerance
* Enable asynchronous workflows
* Increase scalability and resilience

Examples: task processing, event notifications, job scheduling.

---

6. **How would you implement a retry mechanism with exponential backoff for failed message processing?**

**Answer:**
Use a retry loop with a delay that grows exponentially after each failure.

**Example logic:**

1. Try to process the message.
2. On failure → wait `base_delay * (2^attempt)` seconds.
3. Retry up to a maximum attempt count.
4. If still failing → send to a Dead Letter Queue.

**Example pattern:**

* 1s → 2s → 4s → 8s → …
* With jitter to avoid retry storms.

---

7. **Explain dead letter queues and when you'd use them**

**Answer:**
A Dead Letter Queue (DLQ) holds messages that could not be processed successfully after multiple retries.

**Use cases:**

* Messages with malformed data
* Infinite retry prevention
* Operational debugging
* Monitoring abnormal behavior
* Ensuring the main queue stays clean

DLQs improve reliability and prevent system clogging.

---

8. **How does FastAPI handle synchronous functions differently?**

**Answer:**
FastAPI automatically executes synchronous functions (`def`) in a threadpool managed by Starlette.

**Details:**

* Synchronous functions run in a worker thread → do not block the event loop
* Asynchronous functions (`async def`) run directly on the event loop
* FastAPI chooses the correct execution model based on the function signature

This enables CPU-bound or blocking operations to run without affecting overall concurrency.

---

# Session-15-graphQL

**What is GraphQL and how does it differ from REST? What problems does it solve?**

**English:**

1. GraphQL is a query language and runtime that lets clients request exactly the data they need.
2. Unlike REST—which exposes multiple endpoints—GraphQL exposes a single endpoint where clients specify the shape of the response.
3. It solves problems such as over-fetching (receiving more data than needed) and under-fetching (requiring multiple requests to gather data).
4. It is especially useful for complex frontends and mobile apps needing efficient data loading.

**Chinese:**

1. GraphQL 是一种查询语言与运行时，允许客户端“精确地”请求所需要的数据结构。
2. 与需要多个 endpoint 的 REST 不同，GraphQL 只提供一个 endpoint，客户端自己定义返回数据的结构。
3. 它解决了 REST 常见的 **数据过度获取**（拿了太多）和 **数据获取不足**（需要多次请求）的问题。
4. 在前端复杂或移动端需要高效节流数据量的场景下特别有价值。

---

**What is the N+1 query problem in GraphQL and how can it be resolved?**

**English:**

1. N+1 happens when a resolver fetches data for each item individually, causing one query for the list + N queries for each item.
2. Example: fetching a list of posts, then fetching the author for each post.
3. It is resolved using batching and caching techniques, most commonly via **DataLoader**, which groups many small queries into one.

**Chinese：**

1. N+1 问题指：GraphQL resolver 对列表中的每个元素分别查询，例如先查一次 posts 列表，再对列表中的每个 post 查一次 author。
2. 导致总共 1 + N 次查询，性能非常差。
3. 解决方式是 **批处理（batching）与缓存（caching）**，最常用工具是 **DataLoader**，它会把多个独立查询合并成“一次查询”。

---

**Describe the difference between nullable and non-nullable fields in GraphQL. How do you denote them in the schema?**

**English:**

1. Nullable fields can return null; non-nullable fields must always return a value.
2. Non-nullable types are marked with an exclamation mark `!`.
3. Example:

    * `name: String` → may return null
    * `name: String!` → guaranteed non-null

**Chinese：**

1. 可空字段可以返回 null；不可空字段必须返回实际值。
2. 不可空字段在 schema 中用 `!` 标记。
3. 示例：

    * `name: String` → 可以返回 null
    * `name: String!` → 一定不能是 null

---

**What is the DataLoader pattern and why is it important for GraphQL performance?**

**English:**

1. DataLoader batches multiple similar requests into a single query and caches results during a request cycle.
2. It prevents N+1 queries by grouping multiple loads for the same resource.
3. It improves both DB efficiency and backend throughput.

**Chinese：**

1. DataLoader 会将多个相似的数据请求（例如根据多个 id 查多个用户）合并成“一次批量查询”，并在一次请求生命周期中做缓存。
2. 它能避免 N+1 查询，把大量小查询变成少量批量查询。
3. 作用是显著提升数据库效率和后端吞吐量。

---

**What are GraphQL fragments and when would you use them?**

**English:**

1. Fragments allow reusing shared field selections across multiple queries.
2. They avoid repeated boilerplate and ensure consistency.
3. Example use case: multiple components needing the same user fields.

**Chinese：**

1. Fragment 用于复用重复的字段选择，让多个 query 能共享同一段字段定义。
2. 它减少重复代码并保持字段一致性。
3. 典型场景：多个前端组件都需要 User 的部分共同字段。

---

**How would you implement pagination in a Python GraphQL API?**

**English:**

1. Two common patterns: **offset-based** and **cursor-based** pagination.
2. Offset: pass offset/limit to the DB (simple but less scalable).
3. Cursor: use stable encoded cursors (better for large or frequently updated data).
4. In Python (Graphene or Strawberry):

    * Define arguments (`first`, `after`)
    * Query DB based on cursor
    * Return edges + pageInfo

**Chinese：**

1. 分页有两种常见方式：**offset 分页**与 **cursor 分页**。
2. Offset：通过 offset/limit 控制，简单但对大数据或频繁更新的表不稳定。
3. Cursor：基于游标（稳定字段，例如 ID），更适合大规模数据分页。
4. 在 Python GraphQL（Graphene / Strawberry）中：

    * 定义分页参数（如 `first`, `after`）
    * 根据 cursor 查询
    * 返回 edges + pageInfo，符合 Relay 分页规范。

---

**How do you handle errors and exceptions in GraphQL resolvers?**

**English:**

1. GraphQL never throws raw server errors to the client; instead, it returns partial data + an `errors` array.
2. In Python, wrap resolver logic in try/except and raise GraphQLError for user-friendly errors.
3. This keeps the response structure predictable and prevents breaking the entire query when only one field fails.

**Chinese：**

1. GraphQL 的错误不会导致整个请求直接失败，而是返回部分数据并带上 `errors` 数组。
2. 在 Python 实现中，可在 resolver 中使用 try/except，并抛出 GraphQLError 来返回可读错误。
3. 好处是：一个字段失败不会导致整个 query 崩溃，增强 API 鲁棒性。


---

# Session-16-ci-cd-unit-test

## 1. What’s the difference between unit tests, integration tests, and end-to-end tests? When would you use each?

### **English**

**Unit tests**

* Test a single function/class in isolation.
* Fast, small scope, no external systems.
  **Use when:** verifying core logic correctness.

**Integration tests**

* Test how multiple components work together (e.g., service + DB layer).
* Medium speed.
  **Use when:** validating interfaces bw components.

**End-to-end (E2E) tests**

* Test the full system from user perspective, including network, DB, auth.
* Slowest but highest confidence.
  **Use when:** validating full real-world scenarios.

### **中文**

**单元测试**

* 测试最小逻辑单元（函数/类），完全隔离外部依赖。
* 快、覆盖逻辑细节。
  **使用场景：** 核心算法、业务逻辑正确性。

**集成测试**

* 测试多个模块如何协同工作（例如：Service + Repository）。
* 速度中等。
  **使用场景：** 验证模块接口和数据流。

**端到端测试**

* 模拟用户行为，测试整个系统链路（网络、数据库、权限）。
* 最慢但最真实。
  **使用场景：** 回归测试、上线前验收。

---

## 2. Explain the purpose of mocking in unit tests. Difference between Mock, MagicMock, and patch.

### **English**

**Purpose of mocking**

* Replace external dependencies (DB, API, file I/O) so unit tests run fast and deterministically.

**Mock**

* Basic mock object that tracks calls, arguments, return values.

**MagicMock**

* Extends Mock and adds “magic methods” (e.g., `__len__`, `__iter__`, `__getitem__`), useful for mocking objects that behave like collections.

**patch**

* Temporarily replaces an object in a module (`function`, `class`, `variable`) during a test.
* Used when you want to mock at the correct import path.

### **中文**

**Mock 的目的**

* 屏蔽外部依赖（数据库、HTTP、文件系统），让单测只关注逻辑本身并且执行更快、更稳定。

**Mock**

* 基础 mock 对象，可记录调用次数、参数、返回值。

**MagicMock**

* Mock 的增强版，支持各种“魔术方法”，适合 mock 列表/字典/迭代器等对象。

**patch**

* 动态替换模块中的对象，用来 mock 函数、类、变量。
* 重点：必须 patch **代码实际 import 的路径**。

---

## 3. Explain test coverage. What's a good percentage?

### **English**

**Test coverage**

* A metric showing the percentage of executed code during tests (lines, branches, functions).

**Good coverage target:**

* 80% is common industry baseline.
* 100% is unnecessary—high coverage doesn’t guarantee quality.

### **中文**

**测试覆盖率**

* 表示测试过程中被执行的代码占总代码的比例（行覆盖、分支覆盖、函数覆盖）。

**比较合理的目标：**

* 行业普遍标准：80%。
* 不需要追求 100%，关键是测试质量而不是数字。

---

## 4. How do you test code involving databases without hitting real DBs?

### **English**

Strategies:

1. **Mock the database layer** (replace queries with fakes).
2. **Use an in-memory DB** (SQLite for lightweight tests).
3. **Use test containers** (Dockerized Postgres/MySQL specifically for integration tests).
4. **Repository pattern** to isolate DB logic for easier mocking.

### **中文**

测试数据库相关代码的策略：

1. **Mock 数据访问层**（把数据库调用替换成假对象）。
2. **使用内存数据库**（如 SQLite）加快测试。
3. **使用 Testcontainers**（用 Docker 启动真实但独立的数据库进行集成测试）。
4. **使用 Repository 抽象层**，便于隔离和 mock。

---

## 5. What’s test-driven development (TDD)?

### **English**

TDD cycle:

1. **Write a failing test** (Red)
2. **Write minimal code to make it pass** (Green)
3. **Refactor** while keeping tests green

Goal: clean design, high test coverage, clear requirements.

### **中文**

TDD 工作流程：

1. **先写失败的测试**（红）
2. **写最少代码让测试通过**（绿）
3. **重构代码**，所有测试保持通过

目标：更好的设计、天然高覆盖率、更清晰的需求。

---

## 6. Explain the typical stages in a CI/CD pipeline.

### **English**

Stages:

1. **Source / Checkout** – pull code from repo
2. **Build** – compile, package, install dependencies
3. **Unit Tests** – fast logic validation
4. **Integration Tests** – service + DB tests
5. **Static analysis** – lint, type check, security scan
6. **Artifact packaging** – build Docker image / wheel
7. **Deploy** – to staging → production
8. **Post-deploy tests** – smoke tests/health checks

### **中文**

CI/CD 流水线典型阶段：

1. **源码拉取**
2. **构建依赖/编译**
3. **单元测试**
4. **集成测试**
5. **静态分析（lint、类型、安全扫描）**
6. **制品打包（Docker 镜像、wheel 包）**
7. **部署（测试环境 → 生产环境）**
8. **部署后校验（健康检查、冒烟测试）**

---

## 7. What’s the purpose of environment variables & secrets management in CI/CD?

### **English**

Purpose:

* Keep configuration out of code
* Securely manage sensitive data (DB passwords, API keys)
* Support environment-specific configs (dev/staging/prod)

How to handle secrets:

* Secrets Manager (AWS/GCP/Azure)
* Vault
* CI/CD encrypted variables
* Kubernetes Secrets

### **中文**

目的：

* 配置与代码分离
* 安全管理敏感信息（数据库密码、API Key）
* 区分不同环境的配置（开发/测试/生产）

管理方式：

* 云厂商 Secrets Manager
* Vault
* CI/CD 的加密变量
* Kubernetes Secrets

---

## 8. Explain Scrum roles: Product Owner, Scrum Master, Development Team.

### **English**

**Product Owner**

* Owns the product vision
* Prioritizes backlog
* Defines requirements and acceptance criteria

**Scrum Master**

* Facilitates meetings
* Removes blockers
* Ensures Scrum practices

**Development Team**

* Implements features
* Self-organizing
* Responsible for delivering increments

### **中文**

**产品负责人（PO）**

* 负责产品愿景
* 维护 backlog 优先级
* 定义需求和验收标准

**Scrum Master**

* 主持会议
* 移除团队阻碍
* 保障 Scrum 流程正确执行

**开发团队**

* 实现功能
* 自组织协作
* 负责每个迭代的可交付成果

---
# GenAI Day2 

### **Q1. What is a text embedding and why is it useful for RAG?**

A text embedding is simply a way to turn a piece of text into a numeric vector so machines can measure how “related” two pieces of text are. In RAG, this lets the system search by meaning instead of exact words. So even if the user phrases something differently from how it appears in the document, the system can still find the right content. It’s the foundation that allows RAG to do semantic search and provide accurate, grounded answers.

### **Q2. What does embedding dimension mean, and why does it matter?**

The dimension is just how many numbers are in each vector. Bigger vectors usually capture more detail, which can improve search accuracy, but they also cost more memory, more storage, and take longer to compare. Smaller vectors are cheaper and faster but may lose nuance in complex documents. Most RAG systems choose a dimension that balances accuracy with performance and cost.

### **Q3. How do you choose an embedding model for a RAG system?**

The choice depends on your documents, your traffic, and your budget. If your content is technical or sensitive to context, you choose a stronger model for better recall. If your system serves a lot of users or needs very low latency, you pick a lighter model to reduce cost and response time. You usually test a few models on real queries to see which one gives the best mix of accuracy and speed.

### **Q4. Why use a vector database instead of FAISS directly?**

FAISS does fast vector search, but that’s all it does. A vector database adds all the “real product” features you need: metadata filters, access control, sharding, backups, dashboards, ingestion pipelines, and API endpoints. It saves the engineering team from building a lot of infrastructure and lets you operate at scale safely. In production, these surrounding features matter just as much as the search itself.

### **Q5. What role does metadata play? How does it help with access control?**

Metadata gives each chunk extra information, like where it came from, who owns it, or what type of content it is. During search, it lets you filter results so a user only sees content they’re allowed to access. It also improves retrieval quality by scoping search to the right document type or product area. Without metadata, you lose both precision and security.

### **Q6. Why is naïve PDF/HTML parsing not enough?**

Raw text extraction throws away structure: columns merge, tables flatten, headers get mixed into body text, and page numbers sneak in. When this messy text goes into embeddings, retrieval results become noisy and unreliable. For production, you need parsing that understands layout so the meaning of the document stays intact. Otherwise your RAG system answers incorrectly even if the information exists.

### **Q7. How does your system represent documents internally before building the index?**

We treat a document as a hierarchy to keep structure clear. First it becomes pages, then pages break into blocks like paragraphs, headings, lists, or tables. From there we create clean, readable chunks that keep related content together. This makes the embeddings more accurate because each chunk represents a coherent section of the document.

### **Q8. How does your system handle tables and charts?**

Tables and charts don’t work well if treated as plain text because their meaning comes from layout and numbers. Our system detects them and converts them into structured formats that preserve rows, columns, and labels. For charts, we extract any underlying data and also keep descriptive text. This makes retrieval based on numbers or table structure much more reliable.

### **Q9. How did you design your chunking strategy, and an example where bad chunking failed?**

The goal is to make each chunk readable and self-contained so the vector truly represents what the user might want. Bad chunking often happens when content from different parts of the document gets mixed, or when a paragraph is split mid-thought. For example, we once split a policy section across chunks, and searches for “refund rules” returned vague or wrong parts. After fixing the chunking to keep the entire policy section together, retrieval quality improved immediately.
### **Q10. Walk me through your full indexing pipeline.**

We start by loading the raw document and running a layout-aware parser so we don’t lose structure. Then we clean the text, break it into pages and blocks, and create coherent chunks. Each chunk gets embedded into a vector along with metadata like document ID, page number, and permissions. Finally, we store everything in a vector database where it can be filtered and searched quickly during RAG queries. The end result is a clean, searchable knowledge index that stays aligned with the original documents.


# Python 装饰器参数详解

让我详细解释装饰器的参数关系和括号使用。

---

## 🎯 装饰器的三种形式

### 形式 1: 无参数装饰器（最简单）

```python
def my_decorator(func):           # ← 接收被装饰的函数
    def wrapper(*args, **kwargs):  # ← 接收原函数的参数
        print('装饰器逻辑')
        result = func(*args, **kwargs)  # ← 调用原函数
        return result
    return wrapper

@my_decorator     # ← 不带括号！
def say_hello(name):
    print(f"Hello, {name}")

# 等价于：
# say_hello = my_decorator(say_hello)
```

**参数流向：**
```
my_decorator(func)           ← func = say_hello 函数对象
    ↓
  wrapper(*args, **kwargs)   ← args = ("Alice",)
    ↓
  func(*args, **kwargs)      ← 调用 say_hello("Alice")
```

---

### 形式 2: 带参数装饰器（需要返回装饰器）

```python
def log_performance(level="INFO"):      # ← 接收装饰器的参数
    def decorator(func):                # ← 接收被装饰的函数
        def wrapper(*args, **kwargs):   # ← 接收原函数的参数
            print(f'[{level}]')         # ← 使用装饰器参数
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@log_performance(level="DEBUG")  # ← 带括号！传参数
def say_hello(name):
    print(f"Hello, {name}")

# 等价于：
# decorator = log_performance(level="DEBUG")  # 先调用外层，得到 decorator
# say_hello = decorator(say_hello)            # 再调用 decorator
```

**参数流向：**
```
log_performance(level="DEBUG")   ← 装饰器的参数
    ↓ 返回
  decorator(func)                ← func = say_hello
    ↓ 返回
  wrapper(*args, **kwargs)       ← args = ("Alice",)
    ↓
  func(*args, **kwargs)          ← 调用 say_hello("Alice")
```

---

### 形式 3: 类装饰器（不常用）

```python
class MyDecorator:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print("类装饰器")
        return self.func(*args, **kwargs)

@MyDecorator
def say_hello():
    print("Hello")
```

---

## 📊 你的代码分析

### 代码结构

```python
def log_performance(level="INFO"):        # ← 外层函数（装饰器参数）
    def decorator(func):                  # ← 中层函数（被装饰的函数）
        def wrapper(*args, **kwargs):     # ← 内层函数（原函数参数）
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f'[{level}] {func.__name__} is taking {end - start:.4f} seconds')
            return result
        return wrapper
    return decorator
```

---

## 🔑 三层参数关系详解

### 第一层：装饰器自己的参数

```python
def log_performance(level="INFO"):  # ← level 是装饰器的参数
```

**用途：** 配置装饰器的行为

**示例：**
```python
@log_performance(level="DEBUG")  # ← 传入 "DEBUG"
@log_performance(level="ERROR")  # ← 传入 "ERROR"
@log_performance()               # ← 使用默认值 "INFO"
```

---

### 第二层：被装饰的函数

```python
def decorator(func):  # ← func 是被装饰的函数对象
```

**用途：** 接收要被装饰的函数

**示例：**
```python
@log_performance(level="INFO")
def fun1():           # ← 这个函数会被传给 decorator(func)
    pass
```

---

### 第三层：原函数的参数

```python
def wrapper(*args, **kwargs):  # ← *args, **kwargs 是原函数的参数
    result = func(*args, **kwargs)
```

**用途：** 接收并传递原函数的所有参数

**示例：**
```python
@log_performance()
def add(a, b):        # ← a, b 会变成 wrapper 的 args
    return a + b

result = add(1, 2)    # ← (1, 2) 传给 wrapper(*args, **kwargs)
```

---

## 🎓 完整执行流程

### 装饰时发生了什么

```python
@my_decorator
@log_performance(level="INFO")
def fun1():
    print('func1')
```

**等价于：**
```python
# 步骤 1: 执行 log_performance(level="INFO")
temp_decorator = log_performance(level="INFO")
# temp_decorator 现在是 decorator 函数

# 步骤 2: 执行 temp_decorator(fun1)
temp_func = temp_decorator(fun1)
# temp_func 现在是 wrapper 函数

# 步骤 3: 执行 my_decorator(temp_func)
fun1 = my_decorator(temp_func)
# 最终 fun1 是 my_decorator 的 wrapper
```

**调用顺序（从下往上）：**
```
@my_decorator          ← 第 3 步：最外层
@log_performance()     ← 第 2 步：中间层
def fun1():            ← 第 1 步：原函数
    pass
```

---

### 调用时发生了什么

```python
fun1()

# 实际执行顺序：
# 1. 调用 my_decorator 的 wrapper
#    └─ 打印 "my decorator is called"
#    └─ 调用被装饰的函数（log_performance 的 wrapper）
#        └─ 记录开始时间
#        └─ 调用被装饰的函数（原始的 fun1）
#            └─ 打印 "func1"
#            └─ 计算
#        └─ 记录结束时间
#        └─ 打印耗时
```

**输出：**
```
my decorator is called
func1
[INFO] fun1 is taking 0.0012 seconds
```

---

## 🔍 括号的使用规则

### 规则总结

| 装饰器类型 | 使用方式 | 原因 |
|-----------|---------|------|
| **无参数装饰器** | `@decorator` | 直接传函数给装饰器 |
| **有参数装饰器** | `@decorator(args)` | 先调用外层得到装饰器，再装饰函数 |
| **有默认参数** | `@decorator()` 或 `@decorator(args)` | 都可以 |

---

### 详细解释

#### 情况 1: 无参数装饰器

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator     # ← 不加括号
def hello():
    print("Hello")

# 执行过程：
# Python 看到 @my_decorator
# 调用：my_decorator(hello)
# hello = wrapper 函数
```

---

#### 情况 2: 有参数装饰器

```python
def log_performance(level="INFO"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f'[{level}]')
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_performance(level="DEBUG")  # ← 必须加括号
def hello():
    print("Hello")

# 执行过程：
# Python 看到 @log_performance(level="DEBUG")
# 步骤 1: 调用 log_performance(level="DEBUG")，返回 decorator
# 步骤 2: 调用 decorator(hello)，返回 wrapper
# hello = wrapper 函数
```

---

#### 情况 3: 有默认参数的装饰器

```python
def log_performance(level="INFO"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 方式 A: 使用默认值
@log_performance()     # ← 加空括号，level="INFO"
def hello():
    pass

# 方式 B: 传入参数
@log_performance(level="DEBUG")  # ← 加括号传参
def hello():
    pass
```

---

## 💡 常见错误

### 错误 1: 括号用错

```python
# 定义
def my_decorator(func):
    def wrapper():
        func()
    return wrapper

# ❌ 错误使用
@my_decorator()  # TypeError: my_decorator() missing 1 required positional argument
def hello():
    pass

# ✅ 正确使用
@my_decorator
def hello():
    pass
```

---

### 错误 2: 忘记括号

```python
# 定义
def log_performance(level="INFO"):
    def decorator(func):
        def wrapper():
            func()
        return wrapper
    return decorator

# ❌ 错误使用
@log_performance  # 会把 fun1 传给 level 参数！
def fun1():
    pass

# ✅ 正确使用
@log_performance()  # 或 @log_performance(level="INFO")
def fun1():
    pass
```

---

## 🎯 参数传递完整示例

### 示例：带多个参数的装饰器

```python
def retry(max_attempts=3, delay=1):
    """装饰器参数：max_attempts, delay"""
    
    def decorator(func):
        """被装饰的函数：func"""
        
        def wrapper(*args, **kwargs):
            """原函数的参数：*args, **kwargs"""
            
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)  # 传递原函数参数
                    return result
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)  # 使用装饰器参数
        
        return wrapper
    return decorator


# 使用 1: 传入装饰器参数
@retry(max_attempts=5, delay=2)
def flaky_function(x, y):
    """原函数参数：x, y"""
    print(f"尝试计算 {x} + {y}")
    if random.random() < 0.5:
        raise ValueError("失败")
    return x + y


# 调用
result = flaky_function(10, 20)  # ← x=10, y=20 传给 wrapper(*args, **kwargs)
```

**参数流向：**
```
装饰时：
  retry(max_attempts=5, delay=2)
    ↓ 返回 decorator
  decorator(flaky_function)
    ↓ 返回 wrapper
  flaky_function = wrapper

调用时：
  flaky_function(10, 20)
    ↓ 实际调用
  wrapper(10, 20)
    ↓ args=(10, 20)
  func(10, 20)
    ↓ 原函数执行
  return 30
```

---

## 📊 对比表格

### 三层函数的职责

| 层级 | 函数名 | 参数 | 职责 | 何时调用 |
|------|-------|------|------|---------|
| **外层** | `log_performance` | `level="INFO"` | 接收装饰器配置 | 装饰时（`@decorator()`）|
| **中层** | `decorator` | `func` | 接收被装饰函数 | 装饰时（自动）|
| **内层** | `wrapper` | `*args, **kwargs` | 接收原函数参数，执行逻辑 | 每次调用函数时 |

---

### 括号使用规则

| 装饰器定义 | 使用时 | 原因 |
|-----------|--------|------|
| `def decorator(func):` | `@decorator` | 直接传函数，不需要括号 |
| `def outer(param): def decorator(func):` | `@outer(param)` | 需要先调用外层函数 |
| `def outer(param="default"):` | `@outer()` 或 `@outer(param=value)` | 有默认值，括号可选参数 |

---

## 🎓 你的代码详细分析

### 代码 1: `log_performance`（三层结构）

```python
def log_performance(level="INFO"):         # 第 1 层：装饰器参数
    def decorator(func):                   # 第 2 层：被装饰函数
        def wrapper(*args, **kwargs):      # 第 3 层：原函数参数
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f'[{level}] {func.__name__} is taking {end - start:.4f} seconds')
            return result
        return wrapper
    return decorator
```

**参数来源：**
- `level` - 来自 `@log_performance(level="DEBUG")`
- `func` - 来自被装饰的函数（`fun1`）
- `*args, **kwargs` - 来自调用 `fun1()` 时传入的参数

---

### 代码 2: `my_decorator`（两层结构）

```python
def my_decorator(func):      # 第 1 层：被装饰函数
    def wrapper():           # 第 2 层：无参数（固定的）
        print('my decorator is called')
        func()               # ← 调用原函数（无参数）
    return wrapper
```

**问题：** `wrapper()` 没有参数，所以只能装饰无参数的函数

**改进：**
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):  # ✅ 接受任意参数
        print('my decorator is called')
        return func(*args, **kwargs)
    return wrapper
```

---

### 代码 3: 多个装饰器堆叠

```python
@my_decorator
@log_performance()
def fun1():
    print('func1')
```

**执行顺序（装饰时）：**
```python
# 从下往上装饰

# 步骤 1: 
temp1 = log_performance()(fun1)
# log_performance() 返回 decorator
# decorator(fun1) 返回 wrapper1

# 步骤 2:
temp2 = my_decorator(temp1)
# my_decorator(temp1) 返回 wrapper2

# 最终：
fun1 = temp2
```

**调用顺序（调用时）：**
```python
fun1()

# 实际执行：
# 1. my_decorator 的 wrapper
#    └─ 打印 "my decorator is called"
#    └─ 调用 func()（其实是 log_performance 的 wrapper）
#        └─ 记录开始时间
#        └─ 调用 func()（原始的 fun1）
#            └─ 打印 "func1"
#            └─ 循环计算
#        └─ 记录结束时间
#        └─ 打印耗时
```

**输出：**
```
my decorator is called
func1
[INFO] fun1 is taking 0.0012 seconds
```

---

## 🔄 完整的参数传递示例

```python
def verbose_decorator(prefix=">>>", suffix="<<<"):
    """装饰器参数：prefix, suffix"""
    
    def decorator(func):
        """被装饰函数：func"""
        
        def wrapper(*args, **kwargs):
            """原函数参数：*args, **kwargs"""
            
            print(f"{prefix} 调用 {func.__name__}")
            print(f"{prefix} 参数: args={args}, kwargs={kwargs}")
            
            result = func(*args, **kwargs)
            
            print(f"{suffix} 结果: {result}")
            return result
        
        return wrapper
    return decorator


@verbose_decorator(prefix=">>>", suffix="<<<")
def add(a, b, operation="sum"):
    """原函数：接受 a, b, operation"""
    if operation == "sum":
        return a + b
    elif operation == "multiply":
        return a * b


# 调用
result = add(10, 20, operation="sum")
```

**输出：**
```
>>> 调用 add
>>> 参数: args=(10, 20), kwargs={'operation': 'sum'}
<<< 结果: 30
```

**参数追踪：**
```
装饰器层级                参数来源
────────────────────────────────────────
verbose_decorator        prefix=">>>", suffix="<<<"
    ↓
  decorator              func=add 函数对象
    ↓
  wrapper                args=(10, 20), kwargs={'operation': 'sum'}
    ↓
  func(*args, **kwargs)  调用 add(10, 20, operation="sum")
```

---

## 🆚 关键对比

### 有参数 vs 无参数装饰器

#### 无参数装饰器

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@simple_decorator  # ← 不加括号
def hello():
    pass

# 等价于：
hello = simple_decorator(hello)
```

---

#### 有参数装饰器

```python
def param_decorator(param):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

@param_decorator(param="value")  # ← 必须加括号
def hello():
    pass

# 等价于：
decorator = param_decorator(param="value")  # 先得到装饰器
hello = decorator(hello)                     # 再装饰函数
```

---

## 📝 实用模板

### 模板 1: 无参数装饰器

```python
def decorator_name(func):
    def wrapper(*args, **kwargs):
        # 执行前的逻辑
        result = func(*args, **kwargs)
        # 执行后的逻辑
        return result
    return wrapper

@decorator_name
def my_function(x, y):
    return x + y
```

---

### 模板 2: 带参数装饰器

```python
def decorator_name(decorator_param1, decorator_param2="default"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 使用 decorator_param1, decorator_param2
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@decorator_name(param1="value")
def my_function(x, y):
    return x + y
```

---

### 模板 3: 通用装饰器（支持有无参数）

```python
from functools import wraps

def smart_decorator(arg=None, **decorator_kwargs):
    """可以带参数或不带参数使用"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行逻辑
            return func(*args, **kwargs)
        return wrapper
    
    # 如果直接装饰函数（无括号）
    if callable(arg):
        return decorator(arg)
    
    # 如果带参数装饰
    return decorator

# 两种用法都可以：
@smart_decorator
def func1():
    pass

@smart_decorator(param="value")
def func2():
    pass
```

---

## 🎯 记忆口诀

**装饰器参数层级：**
```
外层：装饰器的配置参数
中层：被装饰的函数对象
内层：原函数的运行参数
```

**括号使用：**
```
无参数装饰器：@decorator
有参数装饰器：@decorator(params)
调用函数：func(params)
```

**执行顺序：**
```
装饰：从下往上（最靠近函数的先装饰）
调用：从上往下（最外层先执行）
```

---

## 📊 你的代码执行完整追踪

```python
@my_decorator
@log_performance()
def fun1():
    print('func1')
    for i in range(100000):
        n = 0
        n += 1

fun1()
```

**装饰过程：**
```
1. log_performance() 
   → 返回 decorator

2. decorator(fun1) 
   → 返回 wrapper1
   → fun1 = wrapper1

3. my_decorator(fun1)  # fun1 已经是 wrapper1 了
   → 返回 wrapper2
   → fun1 = wrapper2
```

**调用过程：**
```
fun1()
  ↓ 调用 wrapper2（my_decorator 的）
    ↓ 打印 "my decorator is called"
    ↓ 调用 func()（就是 wrapper1）
      ↓ start = time.time()
      ↓ 调用 func()（原始 fun1）
        ↓ 打印 "func1"
        ↓ 循环计算
      ↓ end = time.time()
      ↓ 打印 "[INFO] fun1 is taking X seconds"
```

**输出：**
```
my decorator is called
func1
[INFO] fun1 is taking 0.0023 seconds
```

这就是装饰器参数的完整解析！🎯
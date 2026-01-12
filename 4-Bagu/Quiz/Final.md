## What is Django’s MTV architecture and how is it different from MVC?

MTV architecture of Django refer to Model, Template and View:
MVC refer to Model, View, Controller
difference is :
MTV used as a pre-design fullstack framework boilerplate, dev customize through attributes and pre-setting field to update its UI, metadata, db-relative operations, security.
MVC is not prepared framework but a standard, popular, modernized architecture which frequently assign by backend developer.

## Difference between primary key, unique index, and non-unique index

- primary key: unique identifiers to clarify each row, usually id or a set of ids
- ❓ unique index: index to optimize searching speed in the background when dev apply query, identify current version of result is unique
- non-unique index: normal, regular index used for searching optimization in queries

## What is a transaction? Which ACID property is hardest to guarantee and why?

- a series of queries which either pass or no any passed for suspain data integrity, r/w consistency of database
- ❓ acid refer to atomicity, consistency, isolation and durability. consistency: atomicity and isolation are natively support with attribute setting, durability just require dev to commit, but consistency is hard to metric in distributed system

## How does row-level locking work in InnoDB? When can it degrade to table locks?

❓

## Differences between threading, multiprocessing, and asyncio in Python

- threading share memory, cpu, lock for multi thread, aim for io-bound task and concurrency
- multi-process have seperate memory, cpu, GIL for each process to natively avoid race condition, used for cpu-bound tasks
- asyncio used for async process, concurrency and coroutine, no block io for event loop, IO-bound-task

## What is the GIL, and why can multiprocessing bypass it?

GIL: Global Interpreter Lock, exist in each process and share between threads in single process, avoid race condition and multiprocess will bypass it for seperate existence in each process

## What does the event loop do? Difference between a coroutine and a task?

event loop like a queue, squeeze sync and async event/task into queue one by one, process them in order, if io intensive or task queue block will block event loop.
❓ coroutine is like parallel processing task with current task in event loop, frequently occur in async tasks, no block io and event loop, will concurrently process multiple tasks.

## Use cases of list vs deque vs heapq

- list: `test = [1,2,3], append, extend, list[index]`
- deque: lib for native double queue, `queue = deque([root]) , add(), remove(), popleft(), pop()`
- heapq: lib for heap operation, `heapfiy(), heapq.heappush(heap, object), heapq.heappop(heap), etc`

## Difference between cProfile and line_profiler, and when to use each?

❓

## Which Python operations look O(1) but are not?

❓

- random search of list: which is easy to mix with updation of list:O(1), but should be O(n)

## Difference between staticmethod, classmethod, and instance method？

- `@staticmethod`, no `cls` or `self` as parameters, regular method in class level
- `@classmethod`, `cls` as parameter, retrive class attributes through class name and dot, shared among all instance
- pass `self` as para, retrieve attribtue/method through instance name, need initialization

## What is idempotency in REST? Which HTTP methods should be idempotent?

❓
Same rest request return same resource, no data change after first handshake.
Get, Delete, Put are, but patch is not, it will iteratively change resource in db

## How does Django ORM prevent SQL injection?

1. avoid direct sql execution, instead use sqlalchemy or sqlmodel engine to alternatively execute respective sql operation in python
2. use `select_related` and `prefetch_related` to avoid n+1 problems

### Difference between `select_related` and `prefetch_related` in Django ORM?

select_related aimed for 1:1, prefetch_related for 1:n

## What is an API contract and why is it critical?

❓
API contract like restful, graphql, grpc, etc's common aggreement that request/response should all follow relative rules, payload, token, metadata and communication architecture design should be standard like contract guided. It's critical cuz it leading a uniform style for whole fullstack architecture design, usually decided after business logic design created.

## What problem does FastAPI-style dependency injection solve?

1. avoid different context or scope of function, avoid dependency context mess
2. request-based dependency attached, which suspain lifecycle management, module-based reference combined, explicitly annotation of dependency type

### Are FastAPI dependencies singleton or request-scoped?

request-scoped, also cached for each request

## What is middleware, and how is it different from an interceptor?

❓
middleware is middle layer added for performance optimization, like api gateway, or caching, or firewall, forward proxy, etc.
interceptor used before controller, middleware usually exists after controller. interceptor is for serialization, authentication preparation, data invalidation, etc, in python, like pydantic schema

## How implement global exception handling in FastAPI?

❓ seperate exception logic in external file, use relative annotation, set categories and filter respective exception to categories.

## JWT vs session: key differences and why JWT is stateless

- JWT: no backend storage for token, but session does
- no state attached in single server, jwt with state only exist with itself and client(local cache) to avoid state loss in distributed sys

### What's the biggest risk of JWT?

- largest: security, xss or other attack ❓
- large set of data attached, heavy token, boost bindwidth, can not revoke old jwt?
  ❓ list, deque, heapq, tc

## Key design differences between Flask and FastAPI

- flask design for synchronous, block event loop, aim for io task, heavy weight framework
- fastapi designed for both, but async is prefered feature, no block io, like springwebflux in java, create async session when connect with db, boost efficiency, reduce latency.

## What problems does GraphQL solve compared to REST?

- multiple concrete endpoint exposure, complicate to handle, troublesome to designd api doc
- rest can only receive fix payload design from backend, not flexible, but graphql is active query, customize json design, avoid shut down due to exception

## When would you prefer composition over inheritance in Python?

composition should always be prefered, especially design odd, composition will avoid diamond problem, mess in multi-inheritance

## What does the CAP theorem really state?

CAP refer to consistency(first retrieve latest data for each node), Availability(firstly reponse to request, and then weak/eventual consistency for data retrieval), Parition Tolerance in distributed sys
always trade-off between ap and cp

## What is idempotent retry and why must retries include timeouts?

❓ refer to re-validation of idempotent response in database, if not idempotent means transations occur no isolation, read repeatable data from other commition.
without timeouts, retries will occur for long period, cause blocking of event loop, heavy burnout of sys

## What is the purpose of consumer groups in Kafka?

consumer group will map to relative topic, whose consumer will receive only one parition from each topic, which boost parallelled efficiency with producer, reduce latency, build concurrency and async processing of data.

## What is a circuit breaker and what problem does it solve?

circuit breaker used as handler for io bindwidth. If huge QPS out of stack will shut down whole system even in distributed architecture, so for each node, a circuit breaker used for handle fixed request number based on specific metric with monitor, if open, stop receiving of current node, then slowly receive request to gain eventual balance, if no break down, then close.

## How does the GIL affect concurrent model inference in Python?

GIL exist for each process ( multi-thread), it will only allow one thread enter critical area to access resource, avoid race condition, boost efficiency of concurrency, is a native lock existed in python.

## Why do AI inference services often use async + batching?

❓
AI inference usually attached with huge dataset from website, books, blogs, file, database, etc, batching will reduce latency, boost data processing efficiency, improve correctness of analytics, async support concurrency, when prompt generated or other inference occurs, async will not block io.

## Why is NumPy faster than Python loops

❓
Numpy is computation lib in python for data analyse, designed as async and distributed computing lib, support large number of method for complicated structure, boost efficiency and performance than loop

## What causes cold start issues in model-serving systems?

usually, if api fail, exception catched, db connection fail, no data storage, config error will cause cold start

## If AI API is slow, which layers would you investigate first?

❓

1. indexing layer, vector db is most complex to boost efficiency and comparison algorithm between prompt and vector list in db is an ongoing project to consider

# Coding

```python
from collection import Counter
def k_frequent(self, nums: List[int], k: int):
    nums_sorted = sorted(counter(nums).items(), key=lambda x: x[1], reverse=True)
    return [item for item, freq in nums_sorted[:k]]
# O(n)
```

1. I will use heap as frequency counter, size is `k`, inside save element: frequency pairs, during loop of process, iteratively compare counted frequency for currenct element from top to bottom till end of `nums`. tc is O(n)
2. with dictionary to count frequency of elements then use loop to save result in array, tc is `O(n)`

```PostgreSQL
select name, department, salary
from (
    select name, department, salary,
    array_agg(salary order by salary desc) over (partition by department) as allsalary
    from employees
) t
where salary =
    case when array_length(allsalary,1)> 1 then allsalary[2]
    else allsalary[1]
    end
order by department, salary desc
```

Q1. What concrete performance advantages does FastAPI have compared to Flask or 
Django?
- FastAPI naively ensure asynchronous and synchrounous support, non blocking event loop, boost efficiency of io boundaryt task, decoupling services
- FastAPI naively support swagger/OpenAPI, auto-generate api doc
- FastAPI support pydantic model to validate data input 

Q2. How does FastAPI achieve high performance internally?
- use `annotated` syntax to support dependency injection 
- use asynchronous, asyncio, asynchttp to decouple service, enable low latency 
- use `load()` to solve n+1 problem 

Q3. What is Dependency Injection in FastAPI, and why is it useful?
- It use `depends` to automatically define dependency object, pass it into parameters of function, decouple scope of request and define lifecycle
- use `annotated` to simutaneously define type of dependency 
- it is useful due to limit scope of current function and define recursive injection of dependency injection behind, through dependency map to background execution 
Q4. How does Django prevent SQL injection?
- instead use sql api, use orm api, take sql operation as separate object operations 
- reasonably set config in metadata of function or object, instead of mannual hardcode sql 

❓Q5. What is Idempotency, and why is it important in APIs and CI/CD systems?
- means multiple request receive same response. 
- for apis, like get, put, delete, the api should be idempotent, for post and patch, it usually not. 
- for cicd, idempotency ensure result consistency of cicd file, especially when bug exists after partial execution of cicd pipeline. 

Q6. How would you optimize a slow SQL query in production?
- check metrics in cloudwatch, promethus, grafana, monitoring and audit 
- target root cause, use replicas of db to replace slow sql queried db 
- adjust schema, avoid nested mergement between multiple db, create index reasonably, avoid big key or value inside
- for nsql db, set isolation and priority, authentication for security, cpu support and io limitation to optimize performance 

❓Q7. What are common causes of slow SQL queries even when indexes exist?
- invalid index design 
- unreasonable table design, like for nested json, we should use jsonb structure in table 

❓Q8. Difference between RDS and DynamoDB? When would you choose each?
- rds 

Q9. What are the core features of GraphQL compared to REST?
- graphql is proactively query lang in terms of client, can request for required response shape, fine-grained design of metadata, function, json structure, no shut down due to exception, only expose one single link for accessing, which reduce security exposure, increase flexibility

Q10. What is the N+1 problem in GraphQL, and how do you solve it?
- we use dataloader to merge batch of query in function into one time query, then pass it to specific tools in graphql. 

Q11. Why do large-scale systems prefer horizontal scaling over vertical scaling?
- horizontal scaling needs seperate server scally, vertical need to power current hose server like add cpu, ram, compiler, which cost a lot for hardware, and hard to backoff and retry 

Q12. What problems can horizontal scaling introduce?
- data consistency 
- availaibity of replicas 
- network between nodes 
- metadata chaning of  registration of all servers
- communication of data between nodes

❓ Q13. What are Master, Core, and Task nodes in an EMR cluster?
- Master is leading node for task/event allocation 
- Core is aim for metadata
- task is for mainly for operation pipeline of event 

Q14. Why is AWS Lambda not suitable for heavy data processing jobs like Spark or Hadoop?
- lambda is stateless and anonymous, it do have size limitation and timeout setting, large data processing task will partial processed then overhead time period 

Q15. When would you choose EMR over Lambda or ECS for data processing?
Coding challenge 
- When we plan for fine-grain, self-configuration, large datasize processing then i will choose EMR


```python 
# question1 
from typing import List
class solution: 
    def trans(self, transactions:List[str])->List:
        stk = [] 
        res = [] 
        if not transactions:
            return [] 
        for trans in transactions:
            name, time, amount, city = trans.split(',')
            time = int(time)
            amount = int(amount)
            # print(name, time, amount, city)
            if not stk:
                if amount>1000:
                    res.append(trans)
                    return res 
                else:
                    stk.append(trans)
            else:
                # print(abs(time-int(stk[0][1])))
                time_ = int(stk[0].split(',')[1])
                city_ = stk[0].split(',')[3]
                if abs(time-time_)<60 and city == city_:
                    res.append(trans)
                else:
                    stk.append(trans)
        return res

sol = solution()
sol.trans(["alice,20,800,mtv","alice,50,1200,mtv"])
# sol.trans(["alice,20,800,mtv","bob,50,1200,mtv"])
```

```python 
# question2 
# my code 
from typing import List 
import heapq
class solution: 
    def allocation(self, n: int, meetings: List[List[int]]):
        minheap = []*n 
        heapq.heapify(minheap, key = lambda x: x[1])
        i = 0 
        for meet in meetings:
            if i<n:
                k = 1
                heapq.heappush(minheap, (i,meet,k))
                i+=1
            print(minheap)
            if minheap and meet[1]>minheap[0][1]:
                i = minheap[0][0]
                meet_ = minheap[0][1]
                k = minheap[0][2]
                heapq.heappop(minheap)
                heapq.heappush(minheap, (i, [meet_[0], meet_[0]+meet[1]-meet[0]], k+1))
# minimal solution based on my code 
from typing import List
import heapq

class Solution:
    def allocation(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort(key=lambda x: x[0])
        count = [0] * n
        available = list(range(n))
        heapq.heapify(available)
        busy = []

        for start, end in meetings:
            while busy and busy[0][0] <= start:
                _, room_id = heapq.heappop(busy)
                heapq.heappush(available, room_id)

            duration = end - start

            if available:
                room_id = heapq.heappop(available)
                heapq.heappush(busy, (end, room_id))
                count[room_id] += 1
            else:
                earliest_end, room_id = heapq.heappop(busy)
                new_end = earliest_end + duration
                heapq.heappush(busy, (new_end, room_id))
                count[room_id] += 1

        max_meetings = max(count)
        for i, c in enumerate(count):
            if c == max_meetings:
                return i

```


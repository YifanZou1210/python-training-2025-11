import time
import threading
import asyncio
"""
Threading: 多线程, 适合IO task
Multiprocessing: 多进程, 适合CPU task
Async/Await: 异步, 基于Coroutine, 使用event loop, 适合IO task,一个线程里可以调度成百上千个协程,协程在 I/O 阻塞时主动“让出控制权”，事件循环去调度其他协程。
    1. 单线程， 没有GIL race
    2. asyncio 解决io阻塞, 其他解决方案： multithread, multiprocess
"""
# 阻塞线程
def fake_blocking_io_task(name):
    print(f"{name} start blocking I/O task")
    time.sleep(2) # blocking 阻塞：程序当前线程在这里停止等待2s
    print(f'{name} done')

# 非阻塞线程
# async def定义了一个协程 coroutine, 可以异步执行
async def fake_non_blocking_IO_task(name):
    print(f"{name} start async I/O task")
    await asyncio.sleep(2)
    # asyncio.to_thread(): Python 3.9+ 提供的一个函数，用于在 异步上下文中安全地运行阻塞函数，本质是把一个阻塞函数放到 线程池中执行，并返回一个可以 await 的协程。
    # asyncio.to_thread(func, *args, **kwargs) func: blocking function 
    # return coroutine object, 需要await才能得到func实际返回值 = func(*args, **kwargs)
    asyncio.to_thread(fake_non_blocking_IO_task(), "name")
    print(f'{name} done')
    
def execute_blocking_tasks():
    start = time.time()
    for i in range(5):
        fake_blocking_io_task(f"task - {i}")
        
    print(f"[Blocking] Total time {time.time() - start:.2f} seconds")
        

# execute_blocking_tasks()

# I/O bounding tasks: sleep, read Database, make api call to to other service IO密集型任务，大部分时间都在等待外部操作
# 比如等待网络响应 API调用、读写文件、数据库查询、time.sleep()\asyncio.sleep()
# CPU bound tasks: cpu calculation heavy task

# GIL (Global Interpreter lock) - limit only one thread is running in python Python 同一时刻只允许一个线程执行 Python 字节码,即使有多核 CPU，多线程也无法并行执行 Python 代码
# GIL 释放时机：IO操作（文件、网络）、time.sleep()

def cpu_task(): # cpu密集任务+多线程
    print(f'calculating')
    pow(365, 1000000) # take about 1s
    print('done')

# io-task在当前线程sleep或者api释放GIL，其他线程可以获得GIL并开始操作
def threading_run():
    threads = []
    start = time.time()
    for i in range(5):
        # 创建线程
        # t = threading.Thread(target=fake_blocking_io_task, args=(f"task - {i}",)) # iotask
        t = threading.Thread(target=cpu_task) # cpu task
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join() # 等待线程t执行完毕，如果不join，主线程可能在子线程还没执行完就提前结束，或者输出可能不完整或者程序提前退出，调用之后，主线程辉阻塞等待该线程完成，然后再继续往下执行
    
    print(f"[Threading] Total time {time.time() - start:.2f} seconds")
    
# threading_run()
# threading_run()
# multi thread vs multi process


async def async_run():
    start = asyncio.get_event_loop().time() # 获取当前时间循环的时间为起点，和time.time()相似，但用时间循环的时间可以更精确的计算写成运行耗时
    await asyncio.gather(*[fake_non_blocking_IO_task(f"task {i}") for i in range(5)]) # 并发运行多个协程 asyncio.gather()
    print(f"[async run] Total time { asyncio.get_event_loop().time() - start:.2f} seconds")
    
asyncio.run(async_run())




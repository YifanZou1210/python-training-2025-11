1.What is the difference between shallow copy and deep copy?
- shallow copy means copy object itself but not reference address, the reference point refer to original object
- deep copy means copy object and its insided reference objects, like refer to all element in a list 

2.Describe Python’s garbage collection mechanisms.

- mechanism use reference pointer to actuate existed objects, whenever the objects do not be referred, they will be destroyed 

3.Explain coroutines vs threads. How does async/await work internally?

- coroutine is associated with async/await syntax for concurrency, a shared thread stack for multiple threads, which is used for io bound task, another way to boost efficiency
- threads are managed by os, global level tools, used for io bound tasks, and preferred for concurrency and process

4.Explain Python’s import system. How are modules loaded and cached?

- py use import keyword to inject dependency into current module, cache returned dependency for each implementation whenever module calls 

5.Explain FastAPI’s startup/shutdown event system.

- use `app.on_event('startup or shutdown')` to run relative function before app starts or shut down 

❌ 6.How do you implement background tasks in FastAPI?

❌ 7.Explain how FastAPI’s lifespan events work. What is the difference between using @app.on_event("startup"), @app.on_event("shutdown"), and the newer lifespan context manager? When would you choose one over the other? Provide examples.

❌ 8.How do Django sessions work? Where are sessions stored?

- Sessions store user-specific data between requests or db (default django_session table), cache, filesystem, or signed cookies.

9.How does Django serve static and media files? How do you handle it in production?

- use cdn to distributed allocate static resource or use cloud service feature to save external files
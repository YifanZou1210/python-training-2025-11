## 1. Tell me about a time you optimized a slow Python script. What did you do?

* First, I used simple timing (`time`, logging) to find which part was slow.
* I checked for common issues: heavy loops, repeated I/O, unnecessary list copies.
* I replaced loops with **list comprehensions** or **built-in functions** like `sum`, `map`.
* For large data, I used **pandas vectorized operations** instead of row-by-row loops.
* Result: runtime reduced significantly and code became cleaner.

说说你优化一个慢的 Python 脚本的经历，你是怎么做的？

* 先用简单的计时方法（`time`、日志）找出慢的部分。
* 检查常见问题：大量循环、重复 I/O、不必要的列表拷贝。
* 用 **列表推导式** 或 `sum`、`map` 等内置函数替换循环。
* 对大数据使用 **pandas 向量化操作**，避免逐行处理。
* 结果：运行时间明显降低，代码更简洁。

- Zhiwei: debugging, monitoring, cpu/io-sync/async, optimize sql, replicas, sharding, caching. 
- 


## 2. Describe a time you cleaned messy data for analysis. How did you handle it?

* I inspected data using `head()`, `info()`, `describe()` to understand issues.
* Handled **missing values** using fill or drop based on business meaning.
* Removed **duplicates** and fixed data types.
* Standardized formats, such as dates and strings.
* After cleaning, I validated row counts and basic statistics.

描述一次你为分析清洗脏数据的经历，你是如何处理的？

* 用 `head()`、`info()`、`describe()` 先了解数据问题。
* 根据业务含义处理 **缺失值**（填充或删除）。
* 去除 **重复数据**，修正数据类型。
* 统一格式，如日期、字符串。
* 清洗后通过行数和统计值验证结果。

- product table, analytical tables, report daily, sql queries optimization, tailer table for specific data, relative weathers, fast read, frequent read data into cache, amount of data, groupby()


## 3. Tell me about a time you wrote Python code to process large files or logs.

* I avoided reading the whole file into memory.
* Used **generators** or line-by-line reading with `for line in file`.
* Processed and wrote results in chunks.
* This kept memory usage low and stable.

说说你用 Python 处理大文件或日志的经历。

* 避免一次性读入内存。
* 使用 **生成器** 或逐行读取 `for line in file`。
* 分批处理并写出结果。
* 这样内存占用低且稳定。



## 4. Describe a time you built a small data pipeline in Python.

* Steps: read data → clean → transform → save to DB or file.
* Used `pandas` for processing and `sqlalchemy`/DB API for writing.
* Added logging and simple error handling with `try-except`.
* Scheduled it with cron or a simple scheduler.

描述一次你用 Python 构建小型数据管道的经历。

* 步骤：读取数据 → 清洗 → 转换 → 保存到数据库或文件。
* 使用 `pandas` 处理，`sqlalchemy` 或 DB API 写入。
* 加入日志和 `try-except` 错误处理。
* 用 cron 或简单调度器定时执行。

- zhiwei: django, mysql, extract student, transform missing values, remove duplicates, one class, calculate relates, mysql db, pandas for transformation, schedule etl for processing. pandas, sqlalchemy, 




## 5. Tell me about a time you used SQL together with Python in a project.

* Used Python to connect to DB and run queries.
* Pulled data into pandas for analysis or reporting.
* Pushed results back to DB as summary tables.
* This separated **heavy querying in SQL** and **logic in Python**.

说说你在项目中结合使用 Python 和 SQL 的经历。

* 用 Python 连接数据库并执行查询。
* 将结果读入 pandas 做分析或报表。
* 再把汇总结果写回数据库。
* 实现 **SQL 负责查询，Python 负责逻辑** 的分工。



## 6. Describe a bug you found in production and how you fixed it.

* First, I checked logs to reproduce the issue.
* Added more logging to narrow down the root cause.
* Wrote a small test to confirm the fix.
* Deployed a hotfix and monitored results.

描述一次你在生产环境发现 bug 并修复的经历。

* 先查看日志复现问题。
* 增加日志缩小问题范围。
* 写一个小测试验证修复。
* 发布热修复并持续监控。

- zhiwei: backend microservice with java springboot, k8s cluster, docker for error code, no ideas, cookies -> 5s, expired, 1 hours. 



## 7. Tell me about a time you improved code readability or maintainability.

* Broke large functions into smaller ones.
* Added clear variable names and comments.
* Followed PEP8 style and used linters.
* Result: easier for others to review and extend.

说说你提升代码可读性或可维护性的经历。

* 将大函数拆成小函数。
* 使用清晰的变量名和注释。
* 遵循 PEP8 并使用代码检查工具。
* 结果：他人更容易理解和扩展。



## 8. Describe your experience building a simple web API in Python (not Flask).

* Used frameworks like **FastAPI or Django**.
* Defined request/response models and endpoints.
* Handled validation, status codes, and errors.
* Tested APIs using curl or Postman.

描述你用 Python 构建简单 Web API（非 Flask）的经验。

* 使用 **FastAPI 或 Django**。
* 定义请求/响应模型和接口。
* 处理校验、状态码和错误。
* 用 curl 或 Postman 测试接口。



## 9. Tell me about a time you worked with JSON data from an API.

* Parsed JSON into dicts/lists.
* Validated required fields and default values.
* Converted it into pandas DataFrame for analysis or storage.
* Handled missing or nested fields carefully.

说说你处理 API 返回 JSON 数据的经历。

* 将 JSON 解析为 dict/list。
* 校验必要字段并设置默认值。
* 转换成 pandas DataFrame 做分析或存储。
* 小心处理缺失和嵌套字段。



## 10. Describe a time you collaborated with others on a Python project.

* Used Git for version control and pull requests.
* Reviewed others’ code and accepted feedback.
* Discussed logic before big changes.
* This reduced bugs and improved overall quality.

描述一次你在 Python 项目中与他人协作的经历。

* 使用 Git 和 PR 进行版本管理。
* 互相做代码评审并接受反馈。
* 大改动前先讨论思路。
* 降低 bug，提高整体质量。



## 11. Tell me about a time you handled exceptions in Python to make code more robust.

* Wrapped risky code in `try-except`.
* Logged errors with clear messages.
* Returned safe defaults or stopped the pipeline gracefully.
* Avoided catching broad exceptions unless necessary.

说说你通过异常处理提升 Python 代码健壮性的经历。

* 用 `try-except` 包裹高风险代码。
* 记录清晰的错误日志。
* 返回安全默认值或优雅终止流程。
* 非必要不捕获过宽异常。



## 12. Describe a time you learned a new Python library quickly for a task.

* Read official docs and simple examples first.
* Built a small demo to test key functions.
* Applied it to real task and refined later.
* This helped deliver on time.

描述一次你为了任务快速学习新 Python 库的经历。

* 先读官方文档和示例。
* 写小 demo 测试核心功能。
* 应用到实际任务中再逐步优化。
* 确保按时交付。


Got it. Here’s a **keyword-focused list of answers** **without changing the questions**, just mapping each question to keywords and concepts you can mention:


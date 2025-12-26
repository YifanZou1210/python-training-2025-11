
### 1. What is the difference between structured, semi-structured, and unstructured data?

* **Structured:** data in tables/columns, easy to query (e.g., SQL databases).
* **Semi-structured:** partially organized, may have tags/keys (e.g., JSON, XML).
* **Unstructured:** no predefined schema, hard to query (e.g., images, logs).

结构化、半结构化和非结构化数据有什么区别？

* **结构化**：表格或列形式，易查询（如 SQL 数据库）。
* **半结构化**：部分组织，有标签或键值（如 JSON, XML）。
* **非结构化**：无固定模式，难以直接查询（如图片、日志）。


---

### 2. Why do we need data replication in distributed systems?

* Ensures **fault tolerance**: data is still available if a node fails.
* Improves **read availability**: multiple copies allow concurrent access.

为什么分布式系统需要数据复制？

* 保证 **容错**：节点故障时数据仍可用。
* 提高 **读取可用性**：多份副本允许并发访问。

---

### 3. What is the difference between batch processing and stream processing?

* **Batch:** processes a large chunk of data at once, higher latency.
* **Stream:** processes data as it arrives, low latency, near real-time.

批处理和流处理有什么区别？

* **批处理**：一次处理大块数据，延迟较高。
* **流处理**：数据到达就处理，低延迟，接近实时。

---

### 4. Why is data partitioning important in a distributed system?

* Splits data across nodes for **parallel computation**.
* Reduces **network congestion** and improves **performance**.

为什么分区在分布式系统中很重要？

* 将数据分散到节点，实现 **并行计算**。
* 减少 **网络拥堵**，提升 **性能**。

---

### 5. What is a data lineage and why is it important?

* Tracks **where data comes from, how it was transformed**, and where it goes.
* Helps **debug errors, audit, and ensure data quality**.

什么是数据血缘（data lineage），为什么重要？

* 追踪 **数据来源、转换过程和去向**。
* 有助于 **调试错误、审计和保证数据质量**。

---

### 6. What is a key-value store and give a simple use case?

* Stores data as **key → value pairs**.
* Example: caching user sessions in Redis.

什么是键值存储（key-value store），举一个简单的应用场景？

* 将数据存储为 **键 → 值** 对。
* 例子：使用 Redis 缓存用户会话信息。

---

### 7. What is the difference between a primary key and a surrogate key in a database?

* **Primary key:** natural identifier from data itself (e.g., email).
* **Surrogate key:** system-generated ID, often numeric, used for joins.

数据库中主键（primary key）和代理键（surrogate key）有什么区别？

* **主键**：来自数据本身的自然标识（如邮箱）。
* **代理键**：系统生成的 ID，通常是数字，用于表连接。

---

### 8. Why is immutability important in Spark RDDs?

* Ensures **fault tolerance**: lost partitions can be recomputed from lineage.
* Avoids **side effects** from changing data mid-computation.

Spark RDD 中不可变性为什么重要？

* 保证 **容错**：丢失的分区可以通过血缘重新计算。
* 避免计算中途修改数据带来的 **副作用**。

---

### 9. What is a watermark in stream processing?

* Watermark indicates **how far in event time the system has processed**.
* Helps handle **late-arriving data** and trigger aggregations.

流处理中的 watermark 是什么？

* Watermark 表示 **系统在事件时间上已处理到哪里**。
* 有助于处理 **延迟到达的数据** 并触发聚合。

---

### 10. Why might you choose Parquet or ORC over CSV for big data storage?

* Columnar formats reduce **I/O** for analytical queries.
* Support **compression and schema evolution**, improving storage and query efficiency.

在大数据存储中，为什么选择 Parquet 或 ORC 而不是 CSV？

* 列式格式减少分析查询的 **I/O**。
* 支持 **压缩和模式演化**，提升存储和查询效率。






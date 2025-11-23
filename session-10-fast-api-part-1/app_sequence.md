# 构建 FastAPI CRUD 应用完整步骤总结

## 📚 总体架构概览

```
FastAPI CRUD Application
│
├── Database Layer (数据库层)
├── Model Layer (模型层)
├── Schema Layer (验证层)
├── Dependency Layer (依赖注入层)
├── Router Layer (路由层)
└── Main Application (主应用)
```

---

## 🎯 完整步骤清单

### **Phase 0: 项目准备阶段**

#### Step 0.1: 安装依赖
```bash
pip install fastapi        # Web 框架
pip install uvicorn        # ASGI 服务器
pip install sqlmodel       # ORM (包含 SQLAlchemy + Pydantic)
pip install psycopg2-binary # PostgreSQL 驱动
pip install httpx          # HTTP 客户端（如果需要调用外部 API）
```

#### Step 0.2: 创建项目结构
```
project_name/
└── app/
    ├── __init__.py         # 标记为 Python 包
    ├── main.py            # 主应用入口
    ├── database.py        # 数据库配置
    ├── models.py          # 数据库模型
    ├── schemas.py         # Pydantic 验证模型
    ├── dependency.py      # 依赖注入函数
    ├── data_init.py       # 初始化数据（可选）
    └── routers/           # 路由模块
        ├── __init__.py
        └── resource.py    # 资源路由（如 users, tasks）
```

---

### **Phase 1: 数据库配置层**

#### Step 1.1: 设置数据库连接 (`database.py`)

**关键要素：**
1. 定义数据库连接 URL
2. 创建数据库引擎
3. 创建会话生成器函数

```python
from sqlmodel import create_engine, Session

# 1. Database URL
DATABASE_URL = "postgresql://user:password@host:port/dbname"

# 2. Create engine
engine = create_engine(DATABASE_URL, echo=True)

# 3. Session generator
def get_session():
    with Session(engine) as session:
        yield session
```

**要点：**
- `echo=True`: 打印 SQL 语句，方便调试
- 使用 `with` 语句确保会话自动关闭
- `yield` 使其成为生成器，FastAPI 会自动管理生命周期

---

### **Phase 2: 模型定义层**

#### Step 2.1: 定义数据库模型 (`models.py`)

**关键要素：**
1. 继承 `SQLModel`，设置 `table=True`
2. 定义表名
3. 定义字段（类型、约束）
4. 定义主键和外键
5. 定义关系（一对多、多对一）

```python
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    # 1. Primary key
    id: int | None = Field(default=None, primary_key=True)
    
    # 2. Regular fields
    name: str = Field(max_length=100)
    
    # 3. Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    
    # 4. Relationships
    tasks: list['Task'] = Relationship(
        back_populates='user',
        cascade_delete=True
    )

class Task(SQLModel, table=True):
    __tablename__ = 'tasks'
    
    id: int | None = Field(default=None, primary_key=True)
    title: str
    
    # Foreign key
    user_id: int = Field(foreign_key='users.id')
    
    # Relationship
    user: User = Relationship(back_populates='tasks')
```

**要点：**
- `Field()` 定义字段约束
- `foreign_key` 建立外键关系
- `Relationship()` 建立 ORM 关系
- `cascade_delete=True` 级联删除

---

### **Phase 3: Schema 验证层**

#### Step 3.1: 定义 Pydantic Schemas (`schemas.py`)

**关键要素：**
1. **Create Schema**: 创建资源时的输入验证
2. **Update Schema**: 更新资源时的输入验证（字段可选）
3. **Response Schema**: 返回给客户端的数据格式

```python
from pydantic import BaseModel, Field

# 1. Create Schema - 所有字段必填
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=1)
    user_id: int

# 2. Update Schema - 字段可选
class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3)
    content: str | None = None

# 3. Response Schema - 返回数据
class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    
    class Config:
        from_attributes = True  # 允许从 ORM 对象创建
```

**验证规则常用参数：**
- `min_length`, `max_length`: 字符串长度
- `ge`, `le`: 数字范围（greater/less than or equal）
- `regex`: 正则表达式验证
- `...`: 表示必填

---

### **Phase 4: 依赖注入层**

#### Step 4.1: 创建依赖函数 (`dependency.py`)

**关键要素：**
1. 数据库会话依赖
2. 外部服务依赖（如天气 API）
3. 类型别名简化使用

```python
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

# 1. Database session dependency
DBSession = Annotated[Session, Depends(get_session)]

# 2. External service dependency
class ForecastClient:
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def fetch_data(self):
        # Implementation
        pass

_forecast_client = None

def get_forecast_client() -> ForecastClient:
    global _forecast_client
    if _forecast_client is None:
        _forecast_client = ForecastClient()
    return _forecast_client

ForecastClientDep = Annotated[ForecastClient, Depends(get_forecast_client)]
```

**要点：**
- 使用 `Annotated` 创建类型别名
- 单例模式避免重复创建实例
- 依赖注入使代码更易测试

---

### **Phase 5: 路由层（核心 CRUD）**

#### Step 5.1: 实现 CRUD 操作 (`routers/resource.py`)

**CRUD 完整实现模板：**

##### **C - CREATE (创建)**
```python
@router.post('/', response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: DBSession
):
    """
    Steps:
    1. Validate related resources (e.g., user exists)
    2. Create model instance
    3. Add to session
    4. Commit transaction
    5. Refresh to get generated fields
    6. Return created resource
    """
    # 1. Validate
    user = db.get(User, task.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    # 2. Create instance
    db_task = Task(
        title=task.title,
        content=task.content,
        user_id=task.user_id
    )
    
    # 3. Add to session
    db.add(db_task)
    
    # 4. Commit
    db.commit()
    
    # 5. Refresh
    db.refresh(db_task)
    
    # 6. Return
    return db_task
```

##### **R - READ (读取)**

**读取多个（带过滤）：**
```python
@router.get('/', response_model=list[TaskResponse])
def get_tasks(
    db: DBSession,
    user_id: int | None = Query(None),
    status: str | None = Query(None)
):
    """
    Steps:
    1. Build base query
    2. Apply filters conditionally
    3. Execute query
    4. Return results
    """
    # 1. Base query
    statement = select(Task)
    
    # 2. Apply filters
    if user_id:
        statement = statement.where(Task.user_id == user_id)
    if status:
        statement = statement.where(Task.status.ilike(status))
    
    # 3. Execute
    tasks = db.exec(statement).all()
    
    # 4. Return
    return tasks
```

**读取单个：**
```python
@router.get('/{task_id}', response_model=TaskResponse)
def get_task(
    task_id: int,
    db: DBSession
):
    """
    Steps:
    1. Get resource by ID
    2. Check if exists
    3. Return resource or 404
    """
    task = db.get(Task, task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    return task
```

##### **U - UPDATE (更新)**
```python
@router.put('/{task_id}', response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: DBSession
):
    """
    Steps:
    1. Get existing resource
    2. Check if exists
    3. Validate related resources if updated
    4. Get update data (only provided fields)
    5. Apply updates
    6. Update timestamp
    7. Commit and return
    """
    # 1-2. Get and check
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    # 3. Validate (if foreign key updated)
    if task_update.user_id:
        user = db.get(User, task_update.user_id)
        if not user:
            raise HTTPException(404, "User not found")
    
    # 4. Get only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    
    # 5. Apply updates
    for key, value in update_data.items():
        setattr(task, key, value)
    
    # 6. Update timestamp
    task.updated_at = datetime.now()
    
    # 7. Commit
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task
```

##### **D - DELETE (删除)**
```python
@router.delete('/{task_id}', status_code=204)
def delete_task(
    task_id: int,
    db: DBSession
):
    """
    Steps:
    1. Get resource
    2. Check if exists
    3. Delete from database
    4. Commit
    5. Return None (204 No Content)
    """
    task = db.get(Task, task_id)
    
    if not task:
        raise HTTPException(404, "Task not found")
    
    db.delete(task)
    db.commit()
    
    return None
```

---

### **Phase 6: 主应用组装**

#### Step 6.1: 创建 FastAPI 应用 (`main.py`)

```python
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routers.tasks import router, user_router

# 1. Create database tables
SQLModel.metadata.create_all(engine)

# 2. Initialize FastAPI app
app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

# 3. Register routers
app.include_router(user_router)
app.include_router(router)

# 4. Root endpoint
@app.get('/')
def home():
    return {'message': 'API is running'}

# 5. Health check
@app.get('/health')
def health():
    return {'status': 'ok'}
```

---

### **Phase 7: 数据初始化（可选）**

#### Step 7.1: 创建初始数据 (`data_init.py`)

```python
from sqlmodel import SQLModel, Session, select
from app.database import engine
from app.models import User, Task

# Create tables
SQLModel.metadata.create_all(engine)

# Insert initial data
with Session(engine) as session:
    # Check if data exists
    statement = select(User)
    existing = session.exec(statement).all()
    
    if not existing:
        # Create test data
        user = User(name="Test User")
        session.add(user)
        session.commit()
        session.refresh(user)
        
        task = Task(title="Test Task", user_id=user.id)
        session.add(task)
        session.commit()
        
        print("Data initialized!")
```

---

## 🎯 关键概念总结

### **1. 数据流向**

```
Request → Schema Validation → Route Handler → Database → Response Schema → Response
   ↓           ↓                    ↓              ↓            ↓
 JSON      TaskCreate          db.add()      Task Model   TaskResponse
```

### **2. 层级职责**

| 层级 | 文件 | 职责 |
|------|------|------|
| **Database** | `database.py` | 数据库连接、会话管理 |
| **Model** | `models.py` | 表结构定义、关系定义 |
| **Schema** | `schemas.py` | 输入验证、输出格式 |
| **Dependency** | `dependency.py` | 依赖注入、资源管理 |
| **Router** | `routers/*.py` | 路由逻辑、CRUD 操作 |
| **Main** | `main.py` | 应用组装、路由注册 |

### **3. CRUD 操作模式**

| 操作 | HTTP 方法 | 路径 | 状态码 | 返回值 |
|------|----------|------|--------|--------|
| **Create** | POST | `/resources` | 201 | 创建的资源 |
| **Read All** | GET | `/resources` | 200 | 资源列表 |
| **Read One** | GET | `/resources/{id}` | 200 | 单个资源 |
| **Update** | PUT/PATCH | `/resources/{id}` | 200 | 更新的资源 |
| **Delete** | DELETE | `/resources/{id}` | 204 | None |

### **4. 常见查询模式**

```python
# 1. Get by ID
resource = session.get(Model, id)

# 2. Get all
statement = select(Model)
resources = session.exec(statement).all()

# 3. Filter
statement = select(Model).where(Model.field == value)
resources = session.exec(statement).all()

# 4. Case-insensitive filter
statement = select(Model).where(Model.field.ilike(value))

# 5. Multiple filters
statement = select(Model).where(
    Model.field1 == value1,
    Model.field2.ilike(value2)
)
```

### **5. 错误处理模式**

```python
from fastapi import HTTPException, status

# 404 - Resource not found
if not resource:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found"
    )

# 400 - Bad request
if invalid_data:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid data"
    )

# 500 - Internal error
try:
    # operation
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )
```

---

## 🚀 运行流程

```bash
# 1. 创建数据库
createdb myapp_db

# 2. 初始化数据（可选）
python -m app.data_init

# 3. 启动服务器
uvicorn app.main:app --reload

# 4. 访问文档
# http://127.0.0.1:8000/docs

# 5. 测试 API
curl -X POST http://127.0.0.1:8000/resources \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

---

## 📝 开发检查清单

- [ ] 数据库连接配置正确
- [ ] 所有模型定义完整（字段、关系、约束）
- [ ] Schema 包含 Create/Update/Response
- [ ] 依赖注入函数已创建
- [ ] CRUD 路由全部实现
- [ ] 错误处理完整（404, 400, 500）
- [ ] 外键验证（创建/更新时）
- [ ] 响应模型正确（`response_model`）
- [ ] 状态码正确（201, 200, 204）
- [ ] 过滤功能实现（Query 参数）
- [ ] 文档字符串完整
- [ ] 代码注释清晰

---

## 🎓 核心知识点

1. **SQLModel = SQLAlchemy + Pydantic**
   - 既是数据库模型又是验证模型

2. **依赖注入 (Depends)**
   - 自动管理资源生命周期
   - 代码更易测试和维护

3. **Schema 分离**
   - 输入验证（Create/Update）
   - 输出格式（Response）
   - 数据库模型（Model）

4. **异步支持**
   - 路由函数可以是 `async def`
   - 适用于 I/O 密集操作（API 调用）

5. **关系映射**
   - `Relationship()` 建立 ORM 关系
   - `cascade_delete` 级联操作

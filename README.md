# 社区生鲜配送管理系统（Python + MySQL 实战项目）

一个基于 Python + MySQL 的控制台业务管理系统，覆盖**商品管理、配送员管理、订单管理**三大核心模块，含完整的三表外键关联、事务处理与参数化查询。适合展示 Python 编程、MySQL 数据库设计、面向过程模块化与工程化编码能力。

## ✨ 功能特性

### 🛒 商品管理
- 添加商品（单价>0、库存≥0 校验）
- 查询商品：按ID精确 / 按名称模糊 / 查询全部，库存≤5 自动标红提醒
- 修改商品、删除商品（有关联订单时禁止删除）

### 🚚 配送员管理
- 添加配送员（11位手机号校验、手机号唯一）
- 查询：按ID / 按姓名 / 在岗 / 休息
- 一键切换在岗 / 休息状态

### 📦 订单管理
- 创建订单：自动校验商品存在、库存充足、配送员在岗 → 计算总价 → 扣减库存（事务）
- 查询订单：按ID / 按状态，JOIN 关联显示商品名与配送员名
- 修改订单状态（待配送 → 配送中 → 已完成）
- 取消订单：仅【待配送】可取消，并自动恢复库存（事务）

## 🛠 技术要点

- **MySQL 数据库设计**：三表 + 外键关联（`product`、`deliveryman`、`order_info`）
- **参数化查询**：全程 `%s` 占位符，防 SQL 注入
- **事务处理**：`commit` / `rollback` 保证下单扣库存、取消恢复库存的原子性
- **模块化分层**：配置 / 建表 / 业务逻辑分离
- **自动建库建表**：`init_tables()` 启动时自动创建数据库与数据表

## 🚀 运行方法

### 环境要求
- Python 3.8+
- MySQL 5.7+（本地需已启动）

### 步骤
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置数据库（重要）
# 复制 db_config.example.py 为 db_config.py，填入你的 MySQL 账号密码
cp db_config.example.py db_config.py

# 3. 启动系统（首次运行自动创建数据库和数据表）
python main.py
```

> ⚠️ 数据库配置文件 `db_config.py` 含密码，已被 `.gitignore` 排除，不会提交到仓库。请勿把真实密码写入示例文件。

## 📂 文件结构

```
fresh-delivery-system/
├── main.py               # 主程序入口（菜单交互）
├── db_config.py          # 数据库配置（本地，不入库）
├── db_config.example.py  # 配置示例模板
├── db_init.py            # 数据库连接与自动建表
├── product_service.py    # 商品管理业务
├── delivery_service.py   # 配送员管理业务
├── order_service.py      # 订单管理业务
├── requirements.txt      # 依赖
└── README.md
```

## 📌 数据表设计

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| product | 生鲜商品 | id, name, price, stock, create_time |
| deliveryman | 配送员 | id, name, phone(唯一), status |
| order_info | 订单 | id, product_id(FK), delivery_id(FK), amount, total, address, status, order_time |

## 📌 学习收获

- Python 与 MySQL 的连接与增删改查
- 外键约束、JOIN 多表联查、事务与回滚
- 参数化查询防注入、异常处理
- 模块化文件组织与工程规范

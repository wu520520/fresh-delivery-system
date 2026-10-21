# 数据库连接、建表初始化

import pymysql
from db_config import *


def get_connection():
    """
    获取数据库连接（先连接服务器，不存在库则创建）
    :return: 数据库连接对象
    """
    # 先连接MySQL服务器
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset=DB_CHARSET
    )
    cursor = connection.cursor()

    # 创建数据库（不存在则创建）
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET {DB_CHARSET}")
    connection.commit()
    cursor.close()
    connection.close()

    # 连接到目标库
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    return conn


def init_tables():
    """
    初始化三张数据表：商品表、配送员表、订单表（带外键关联）
    不存在则自动创建，已存在则不执行
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. 商品表
    sql_product = """
    CREATE TABLE IF NOT EXISTS product (
        id INT PRIMARY KEY AUTO_INCREMENT COMMENT '商品ID',
        name VARCHAR(50) NOT NULL COMMENT '商品名称',
        price DECIMAL(6,2) NOT NULL COMMENT '单价(元/斤)',
        stock INT NOT NULL DEFAULT 0 COMMENT '库存(斤)',
        create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='生鲜商品表';
    """

    # 2. 配送员表
    sql_delivery = """
    CREATE TABLE IF NOT EXISTS deliveryman (
        id INT PRIMARY KEY AUTO_INCREMENT COMMENT '配送员ID',
        name VARCHAR(20) NOT NULL COMMENT '姓名',
        phone VARCHAR(11) NOT NULL UNIQUE COMMENT '手机号',
        status INT NOT NULL DEFAULT 1 COMMENT '状态 0休息 1在岗'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配送员表';
    """

    # 3. 订单表（外键关联商品、配送员）
    sql_order = """
    CREATE TABLE IF NOT EXISTS order_info (
        id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID',
        product_id INT NOT NULL COMMENT '商品ID',
        delivery_id INT NOT NULL COMMENT '配送员ID',
        amount INT NOT NULL COMMENT '购买数量',
        total DECIMAL(8,2) NOT NULL COMMENT '总金额',
        address VARCHAR(100) NOT NULL COMMENT '配送地址',
        status INT NOT NULL DEFAULT 0 COMMENT '0待配送 1配送中 2已完成 3已取消',
        order_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
        FOREIGN KEY (product_id) REFERENCES product(id),
        FOREIGN KEY (delivery_id) REFERENCES deliveryman(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配送订单表';
    """

    # 执行建表
    cursor.execute(sql_product)
    cursor.execute(sql_delivery)
    cursor.execute(sql_order)
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ 数据库与数据表初始化完成！")

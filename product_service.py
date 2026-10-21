# 商品管理功能

from db_init import get_connection

def add_product():
    """添加商品：验证单价、库存为正数"""
    try:
        name = input("请输入商品名称：").strip()
        price = float(input("请输入商品单价（元/斤）：").strip())
        stock = int(input("请输入初始库存（斤）：").strip())

        if price <= 0 or stock < 0:
            print("❌ 单价必须大于0，库存不能为负数！")
            return

        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO product(name, price, stock) VALUES(%s, %s, %s)"
        cursor.execute(sql, (name, price, stock))
        conn.commit()
        print("✅ 商品添加成功！")
    except ValueError:
        print("❌ 输入格式错误！单价必须是数字，库存必须是整数！")
    except Exception as e:
        print(f"❌ 添加失败：{e}")
    finally:
        cursor.close()
        conn.close()

def query_product():
    """商品查询：ID精确/名称模糊/全部（库存≤5标红）"""
    print("\n===== 商品查询方式 =====")
    print("1. 按商品ID查询")
    print("2. 按商品名称模糊查询")
    print("3. 查询所有商品")
    choice = input("请选择：").strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if choice == "1":
            pid = input("请输入商品ID：").strip()
            sql = "SELECT * FROM product WHERE id=%s"
            cursor.execute(sql, (pid,))
        elif choice == "2":
            name = input("请输入商品名称关键词：").strip()
            sql = "SELECT * FROM product WHERE name LIKE %s"
            cursor.execute(sql, (f"%{name}%",))
        elif choice == "3":
            sql = "SELECT * FROM product"
            cursor.execute(sql)
        else:
            print("❌ 输入错误！")
            return

        res = cursor.fetchall()
        if not res:
            print("📛 未查询到商品信息")
            return

        print("\n===== 商品列表 =====")
        for item in res:
            pid, name, price, stock, ctime = item
            tip = "【库存不足！】" if stock <= 5 else ""
            print(f"ID：{pid} | 名称：{name} | 单价：{price} | 库存：{stock} {tip}| 创建时间：{ctime}")
    except Exception as e:
        print(f"❌ 查询失败：{e}")
    finally:
        cursor.close()
        conn.close()

def update_product():
    """修改商品：单价、库存（非负）"""
    try:
        pid = input("请输入要修改的商品ID：").strip()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product WHERE id=%s", (pid,))
        if not cursor.fetchone():
            print("❌ 该商品不存在！")
            return

        price = float(input("请输入新单价：").strip())
        stock = int(input("请输入新库存：").strip())
        if price <= 0 or stock < 0:
            print("❌ 单价>0，库存≥0！")
            return

        sql = "UPDATE product SET price=%s, stock=%s WHERE id=%s"
        cursor.execute(sql, (price, stock, pid))
        conn.commit()
        print("✅ 商品信息修改成功！")
    except ValueError:
        print("❌ 输入格式错误！")
    except Exception as e:
        print(f"❌ 修改失败：{e}")
    finally:
        cursor.close()
        conn.close()

def delete_product():
    """删除商品：必须无关联订单"""
    pid = input("请输入要删除的商品ID：").strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 检查是否存在
        cursor.execute("SELECT id FROM product WHERE id=%s", (pid,))
        if not cursor.fetchone():
            print("❌ 商品不存在！")
            return

        # 检查是否有关联订单
        cursor.execute("SELECT id FROM order_info WHERE product_id=%s", (pid,))
        if cursor.fetchone():
            print("❌ 该商品存在关联订单，无法删除！")
            return

        cursor.execute("DELETE FROM product WHERE id=%s", (pid,))
        conn.commit()
        print("✅ 商品删除成功！")
    except Exception as e:
        print(f"❌ 删除失败：{e}")
    finally:
        cursor.close()
        conn.close()


# 订单管理功能
from db_init import get_connection

def create_order():
    """创建订单：验证商品、库存、配送员在岗 → 扣库存 → 生成订单"""
    try:
        pid = int(input("商品ID：").strip())
        did = int(input("配送员ID：").strip())
        amount = int(input("购买数量（斤）：").strip())
        address = input("配送地址：").strip()

        if amount <= 0:
            print("❌ 数量必须大于0！")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # 1 验证商品与库存
        cursor.execute("SELECT price, stock FROM product WHERE id=%s", (pid,))
        prod = cursor.fetchone()
        if not prod:
            print("❌ 商品不存在！")
            return
        price, stock = prod
        if stock < amount:
            print("❌ 库存不足！")
            return

        # 2 验证配送员在岗
        cursor.execute("SELECT status FROM deliveryman WHERE id=%s", (did,))
        deli = cursor.fetchone()
        if not deli:
            print("❌ 配送员不存在！")
            return
        if deli[0] != 1:
            print("❌ 该配送员休息中，无法接单！")
            return

        # 3 计算总价
        total = price * amount

        # 4 插入订单
        sql = """INSERT INTO order_info(product_id,delivery_id,amount,total,address)
                 VALUES(%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (pid, did, amount, total, address))

        # 5 扣减库存
        cursor.execute("UPDATE product SET stock=stock-%s WHERE id=%s", (amount, pid))
        conn.commit()
        print(f"✅ 订单创建成功！总金额：{total} 元")

    except ValueError:
        print("❌ 输入格式错误！")
    except Exception as e:
        conn.rollback()
        print(f"❌ 下单失败：{e}")
    finally:
        cursor.close()
        conn.close()

def query_order():
    """订单查询：ID/状态，关联显示商品名、配送员名"""
    print("\n===== 订单查询 =====")
    print("1. 按订单ID查询")
    print("2. 按状态查询 0待配送 1配送中 2已完成")
    choice = input("请选择：").strip()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT o.id,p.name,d.name,o.amount,o.total,o.address,o.status,o.order_time
            FROM order_info o
            JOIN product p ON o.product_id=p.id
            JOIN deliveryman d ON o.delivery_id=d.id
        """
        if choice == "1":
            oid = input("输入订单ID：").strip()
            sql += " WHERE o.id=%s"
            cursor.execute(sql, (oid,))
        elif choice == "2":
            status = input("输入状态码(0/1/2)：").strip()
            sql += " WHERE o.status=%s"
            cursor.execute(sql, (status,))
        else:
            print("❌ 输入错误！")
            return

        res = cursor.fetchall()
        if not res:
            print("📛 无订单信息")
            return

        status_map = ["待配送", "配送中", "已完成", "已取消"]
        print("\n===== 订单详情 =====")
        for item in res:
            oid, pname, dname, amt, total, addr, status, otime = item
            print(f"订单ID：{oid} | 商品：{pname} | 配送员：{dname} | 数量：{amt} | 总价：{total}")
            print(f"地址：{addr} | 状态：{status_map[status]} | 时间：{otime}\n")
    except Exception as e:
        print(f"❌ 查询失败：{e}")
    finally:
        cursor.close()
        conn.close()

def update_order_status():
    """修改订单状态：支持流转"""
    oid = input("请输入订单ID：").strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM order_info WHERE id=%s", (oid,))
        res = cursor.fetchone()
        if not res:
            print("❌ 订单不存在！")
            return

        print("状态：0待配送 1配送中 2已完成 3已取消")
        new_status = int(input("请输入目标状态：").strip())
        cursor.execute("UPDATE order_info SET status=%s WHERE id=%s", (new_status, oid))
        conn.commit()
        print("✅ 订单状态修改成功！")
    except Exception as e:
        print(f"❌ 修改失败：{e}")
    finally:
        cursor.close()
        conn.close()

def cancel_order():
    """取消订单：仅待配送可取消 → 恢复库存"""
    oid = input("请输入要取消的订单ID：").strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 查询订单状态与商品信息
        sql = """SELECT status,product_id,amount FROM order_info WHERE id=%s"""
        cursor.execute(sql, (oid,))
        res = cursor.fetchone()
        if not res:
            print("❌ 订单不存在！")
            return

        status, pid, amount = res
        if status != 0:
            print("❌ 只有【待配送】订单可取消！")
            return

        # 取消订单 + 恢复库存
        cursor.execute("UPDATE order_info SET status=3 WHERE id=%s", (oid,))
        cursor.execute("UPDATE product SET stock=stock+%s WHERE id=%s", (amount, pid))
        conn.commit()
        print("✅ 订单已取消，库存已恢复！")

    except Exception as e:
        conn.rollback()
        print(f"❌ 取消失败：{e}")
    finally:
        cursor.close()
        conn.close()
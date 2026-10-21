# 配送员管理功能
from db_init import get_connection

def add_deliveryman():
    """添加配送员：验证11位手机号"""
    name = input("请输入配送员姓名：").strip()
    phone = input("请输入11位手机号：").strip()

    if len(phone) != 11 or not phone.isdigit():
        print("❌ 手机号必须是11位数字！")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO deliveryman(name, phone) VALUES(%s, %s)"
        cursor.execute(sql, (name, phone))
        conn.commit()
        print("✅ 配送员添加成功！")
    except Exception as e:
        print(f"❌ 添加失败（手机号重复）：{e}")
    finally:
        cursor.close()
        conn.close()

def query_deliveryman():
    """配送员查询：ID/姓名/在岗/休息"""
    print("\n===== 配送员查询 =====")
    print("1. 按ID查询")
    print("2. 按姓名模糊查询")
    print("3. 查询所有在岗")
    print("4. 查询所有休息")
    choice = input("请选择：").strip()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        if choice == "1":
            did = input("输入配送员ID：").strip()
            sql = "SELECT * FROM deliveryman WHERE id=%s"
            cursor.execute(sql, (did,))
        elif choice == "2":
            name = input("输入姓名关键词：").strip()
            sql = "SELECT * FROM deliveryman WHERE name LIKE %s"
            cursor.execute(sql, (f"%{name}%",))
        elif choice == "3":
            sql = "SELECT * FROM deliveryman WHERE status=1"
            cursor.execute(sql)
        elif choice == "4":
            sql = "SELECT * FROM deliveryman WHERE status=0"
            cursor.execute(sql)
        else:
            print("❌ 输入错误！")
            return

        res = cursor.fetchall()
        if not res:
            print("📛 无配送员信息")
            return

        print("\n===== 配送员信息 =====")
        for item in res:
            did, name, phone, status = item
            s = "在岗" if status == 1 else "休息"
            print(f"ID：{did} | 姓名：{name} | 手机：{phone} | 状态：{s}")
    except Exception as e:
        print(f"❌ 查询失败：{e}")
    finally:
        cursor.close()
        conn.close()

def change_delivery_status():
    """切换配送员状态：休息 ↔ 在岗"""
    did = input("请输入配送员ID：").strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT status FROM deliveryman WHERE id=%s", (did,))
        res = cursor.fetchone()
        if not res:
            print("❌ 配送员不存在！")
            return

        new_status = 0 if res[0] == 1 else 1
        cursor.execute("UPDATE deliveryman SET status=%s WHERE id=%s", (new_status, did))
        conn.commit()
        print(f"✅ 状态已切换为：{'休息' if new_status == 0 else '在岗'}")
    except Exception as e:
        print(f"❌ 修改失败：{e}")
    finally:
        cursor.close()
        conn.close()
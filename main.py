# 主程序入口（菜单）

"""
社区生鲜配送管理系统
功能：商品管理、配送员管理、订单管理
"""
from db_init import init_tables
from product_service import *
from delivery_service import *
from order_service import *


def main():
    # 系统启动时自动初始化数据库和表
    init_tables()
    print("\n===== 欢迎使用社区生鲜配送管理系统 =====")

    while True:
        print("\n===== 主菜单 =====")
        print("1. 商品管理")
        print("2. 配送员管理")
        print("3. 订单管理")
        print("0. 退出系统")
        choice = input("请输入功能编号：").strip()

        if choice == "1":
            while True:
                print("\n===== 商品管理 =====")
                print("1. 添加商品")
                print("2. 查询商品")
                print("3. 修改商品")
                print("4. 删除商品")
                print("0. 返回主菜单")
                c = input("请选择：").strip()
                if c == "1":
                    add_product()
                elif c == "2":
                    query_product()
                elif c == "3":
                    update_product()
                elif c == "4":
                    delete_product()
                elif c == "0":
                    break
                else:
                    print("❌ 输入错误！")

        elif choice == "2":
            while True:
                print("\n===== 配送员管理 =====")
                print("1. 添加配送员")
                print("2. 查询配送员")
                print("3. 修改配送员状态")
                print("0. 返回主菜单")
                c = input("请选择：").strip()
                if c == "1":
                    add_deliveryman()
                elif c == "2":
                    query_deliveryman()
                elif c == "3":
                    change_delivery_status()
                elif c == "0":
                    break
                else:
                    print("❌ 输入错误！")

        elif choice == "3":
            while True:
                print("\n===== 订单管理 =====")
                print("1. 创建订单")
                print("2. 查询订单")
                print("3. 修改订单状态")
                print("4. 取消订单")
                print("0. 返回主菜单")
                c = input("请选择：").strip()
                if c == "1":
                    create_order()
                elif c == "2":
                    query_order()
                elif c == "3":
                    update_order_status()
                elif c == "4":
                    cancel_order()
                elif c == "0":
                    break
                else:
                    print("❌ 输入错误！")

        elif choice == "0":
            print("\n👋 系统已退出，感谢使用！")
            break

        else:
            print("❌ 请输入正确编号！")


if __name__ == "__main__":
    main()

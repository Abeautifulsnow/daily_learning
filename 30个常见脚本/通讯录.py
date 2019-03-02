# 通讯录
telbook = {}
print("欢迎使用XXX的通讯录，请输入您想要进行的操作")
flag = "C"
while flag == "C" or "D" or "U" or "R" or "E":
    m = input("1.输入C为通讯录添加联系人和相应手机号.\n2.输入D删除通讯录里的联系人.\n3.输入U修改通讯录里联系人手机号.\n4.输入R查询通讯录里的所有用户.\n5.输入E根据姓名查找响应联系人手机号.\n")
    if m == "C":
        username = input("请输入联系人姓名：")
        telnumber = input("请输入联系人电话：")
        telbook[str(username)] = str(telnumber)
        print("添加成功,通讯录中现有联系人为：", end=" ")
        print(telbook)
        n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录:")
        if n == "N":
            print("您已经退出通讯录")
            break
        else:
            continue
    elif m == "D":
        # print("您是否想删除通讯录里联系人")
        # deusername = input("请输入要删除的联系人名字:")
        # del telbook[deusername]
        # print("删除成功，删除后的通讯录内容为", telbook, end=" ")
        # n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录")
        # if n == "N":
        #     print("您已经退出通讯录")
        #     break
        # else:
        #     continue
        l = input("您是否想删除通讯录里联系人?如果是，请输入Y；否则任意键继续:")
        if l == "Y":
            deusername = input("请输入要删除的联系人名字:")
            del telbook[deusername]
            print("删除成功，删除后的通讯录内容为", telbook, end=" ")
            n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录:")
            if n == "N":
                print("您已经退出通讯录")
                break
            else:
                continue
        else:
            continue
    elif m == "U":
        mousername = input("请输入要修改的联系人姓名:")
        for key in sorted(telbook.keys()):
            if str(mousername) == key:
                motelnumber = input("联系人存在，请输入修改后的新号码:")
                telbook[str(key)] = str(motelnumber)
                print("修改成功,修改后的通讯录为", telbook)
                break
            n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录:")
            if n == "N":
                print("您已经退出通讯录")
                break
            else:
                continue
    elif m == "R":
        print(list(telbook.keys()))
        n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录:")
        if n == "N":
            print("您已经退出通讯录")
            break
        else:
            continue
    elif m == "E":
        searchname = input("请输入您想查询响应手机号的联系人姓名:")
        for key2 in sorted(telbook.keys()):
            if str(searchname) == key2:
                print(key2, telbook[key2])
            else:
                print("没有您输入的联系人信息，请重新输入或添加后输入")
        n = input("您是否想继续操作刘宇宸通讯录？任意键为继续，N为退出通讯录:")
        if n == "N":
            print("您已经退出通讯录")
            break
        else:
            continue
    else:
        print("您的输入有误")

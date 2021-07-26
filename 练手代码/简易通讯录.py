import re

phone_dict = {}
input_content = str(input("欢迎使用通讯录，请点击任意键查看您想要进行的操作"))
flag = 'a'

while flag == 'a' or 'b' or '#':
    m = input("1.输入a为通讯录添加联系人和相应的手机号.\n2.输入ｂ为查询相关信息.\n3.输入#为退出.\n")
    if m == 'a':
        input_content = str(input("请输入姓名和手机号，并以空格间隔:"))
        # 判断中文正则模板
        chinese_pat = re.compile(r"[\u4e00-\u9fa5]+")
        # 判断手机号是否合法正则模板
        mobile_pat = re.compile(r"^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$")
        
        phone_name = "".join(re.findall(chinese_pat, input_content))
        phone_num = "".join(re.findall(r"\d+", input_content))
        result = re.search(mobile_pat, phone_num)
        # 判断输入的手机号是否合法
        if result:
            phone_dict[phone_name] = phone_num
            print("{0}的手机号：{1}已经保存完毕.".format(phone_name, phone_num), end="\n==============\n")
            print(phone_dict)
            n = str(input("请是否还想继续操作通讯录?如果是，请按y继续；否则，按n退出通讯录："))
            if n == 'n':
                print("您已退出通讯录")
                break
            else:
                continue
        else:
            print("手机号码不合法，请重新输入.\n")
            continue
    elif m == 'b':
        search_input = str(input("请输入信息：\n0：机主姓名\n1：手机号\n"))
        if search_input == '0':
            name = str(input("请输入机主姓名："))
            if name in phone_dict.keys():
                name_phone = phone_dict[name]
                print(f"{name}的手机号为：{name_phone}")
            else:
                print("不存在")
        elif search_input == '1':
            phone = str(input("请输入手机号："))
            if phone in phone_dict.values():
                for key, value in phone_dict.items():
                    if phone in value:
                        print(f"{phone}的机主为{key}")
            else:
                print("陌生号码.")
    elif m == '#':
        break

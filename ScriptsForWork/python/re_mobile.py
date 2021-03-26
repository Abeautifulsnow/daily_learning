import re

input_content = str(input("请输入姓名和手机号，并以空格间隔:"))

# 判断中文正则模板
chinese_pat = re.compile(r"[\u4e00-\u9fa5]+")
# 判断手机号是否合法正则模板
mobile_pat = re.compile("^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$")

phone_name = "".join(re.findall(chinese_pat, input_content))
phone_num = "".join(re.findall(r"\d+", input_content))

if re.search(mobile_pat, phone_num):
    print(phone_num)
else:
    print("手机号码不合法")

print(phone_name, end="\n")

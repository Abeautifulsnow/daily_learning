"""
判断手机号/座机号的正则判断函数。
"""

import re


# 正则定义
# 11位手机号验证
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
# 座机号验证
REGEX_LIND_LINE = "^([0-9]{3,4}-)?[0-9]{7,8}$"
# 企业直线号码
REGEX_ENTERPRISE_NUMBER = "^\d{3,4}-\d{3,4}-\d{3,4}$"


def judge_phone(phone):

    if re.match(REGEX_LIND_LINE, phone):
        print(f"{phone}匹配成功！")
    elif re.match(REGEX_MOBILE, phone):
        print(f"{phone}匹配成功！")
    elif re.match(REGEX_ENTERPRISE_NUMBER, phone):
        print(f"{phone}匹配成功！")
    else:
        print(f"所输入的号码：{phone}不存在！")


if __name__ == '__main__':
    phone = str(input("请输入手机号码："))
    judge_phone(phone)

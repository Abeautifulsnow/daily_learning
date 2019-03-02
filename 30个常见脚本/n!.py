"""
f(n)=n*f(n-1)
"""
def factorial():
    num = int(input("请输入一个数字："))
    fac = 1

    if num < 0:
        print("抱歉，负数没有阶乘！")
    elif num == 0:
        print("0的阶乘为1.")
    else:
        for i in range(1, num + 1):
            fac = fac * i
        print("%d 的阶乘为 %d" % (num, fac))

# 实例化
factorial()

"""===================其余条件不全方法==================
def fact(n):
    result = n
    for i in range(1, n):
        result *= i
    return result

print(fact(n))

======================================================
def fact(n):
    if n == 0 or n == 1:
        return 1
    return n * fact(n - 1)

print(fact(n))
"""
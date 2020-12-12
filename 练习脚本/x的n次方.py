"""
x**n：1*x*x*x*x*...*x
"""


def cal(x, n):
    s = 1
    while n > 0:
        n -= 1
        s *= x
    return s


print(cal(4, 3))

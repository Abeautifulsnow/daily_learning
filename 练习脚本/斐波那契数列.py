"""# 第一种
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
        print(b)"""

# 第二种,yield更节省存储空间
import sys


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if counter >= n:
            return
        yield b
        a, b = b, a+b
        counter += 1


num = int(input("请输入一个整数："))
f = fibonacci(num)  # f实例化，它是一个迭代器，由生成器生成
while True:
    try:
        print(next(f), end=' ')
    except StopIteration:
        sys.exit()

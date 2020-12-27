# -*- coding:utf-8 -*-
# 斐波那契数列生成
# def fbnq(x):
# 	a, b, c = 0, 0, 1
# 	fbnqlist = []
# 	while a < x:
# 		fbnqlist.append(c)
# 		b, c = c, b+c
# 		a += 1
# 	return fbnqlist

# print(fbnq(8))


# yield方式
import sys

def fib(n):
	a, b, count = 0, 1, 0
	while True:
		if count >= n:
			return
		else:
			yield b
			a, b = b, a + b
			count += 1


n = int(input('请输入一个整数：'))
f = fib(n)
while True:
	try:
		print(next(f), end=' ')
	except StopIteration:
		sys.exit()
"""
十进制转二进制、八进制、十六进制
"""
decimal = int(input("请输入数字："))

print("十进制数为：", decimal)
print("转换为二进制为：", bin(decimal))
print("转换为八进制为：", oct(decimal))
print("转换为十六进制为：", hex(decimal))
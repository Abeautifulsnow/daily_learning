def calc(*numbers):
    sum = 0
    for x in numbers:
        sum = sum + x*x
    return sum

print(calc(1, 2 ,3))
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment


for i in frange(1, 6, 1):
    print(i)

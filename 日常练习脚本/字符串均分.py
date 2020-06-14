# 方法一:列表推导式
# a = '001234567890'
# step = 4
# b = [a[i:i+step] for i in range(0, len(a), step)]
# print(b)

# 方法二:装饰器和生成器


def segmented(iterable):
    def _seg(width):
        it = iterable
        while len(it) > width:
            yield it[:width]
            it = it[width:]
        yield it
    return _seg


a = '001234567890'
split_every = segmented(a)
print(list(split_every(15)))
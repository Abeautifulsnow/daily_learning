import matplotlib.pyplot as plt

ip = {}
with open('access.log') as f:
    for i in f.readlines():
        s = i.strip().split()[0]
        length = len(ip.keys())

        # 统计ip访问量并以字典存储
        if s in ip.keys():
            ip[s] += 1
        else:
            ip[s] = 1


# ip出现的次数排序返回对象为list
ip = sorted(ip.items(), key=lambda e: e[1], reverse=True)
# 取列表前十
newip = ip[0:10]
tu = dict(newip)
print(tu)

x, y = [], []
for k in tu:
    x.append(k)
    y.append(tu[k])

plt.title('ip_access')
plt.xlabel('ip address')
plt.ylabel('PV')

# x轴的翻转角度
plt.xticks(rotation=70)

# 显示每个柱状图的值
for a, b in zip(x, y):
    plt.text(a, b, '%.0f' % b, ha='center', va='bottom', fontsize=7)

plt.bar(x, y)
plt.legend()
plt.show()
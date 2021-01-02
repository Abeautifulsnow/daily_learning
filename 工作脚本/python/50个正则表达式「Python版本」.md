# 50个正则表达式「Python版本」

正则表达式(Regular Expression)通常被用来检索、替换那些符合某个模版(规则)的文件。

以下案例包括**「邮箱、身份证号、手机号码、固定电话、域名、IP地址、日期、邮编、密码、中文字符、数字、字符串等」**

> 1. 邮箱

邮箱包含大小写字母、数字、下划线、点号、短横线

**表达式：**

```shell
[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)
```

**案例：**

```python
# match mail
import re

mail_pattern = r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)'
strs = "我的私人邮箱是zhjhfsjk@yahho.com，公司邮箱是123456qq@qq.cn"
re.findall(mail_pattern, strs)

# result
['zhjhfsjk@yahho.com', '123456qq@qq.cn']
```

> 2. 身份证号

xxxxxx yyyymmdd oooo 总共18位

**表达式：**

```shell
- 地区：[1-9]{6}
- 年份前两位：(17|18|19|([23]\d))
- 年份后两位：\d{2}
- 月份：((0[1-9])|(10|11|12))
- 天数：(([0-2][1-9])|10|20|30|31)
- 三位顺序码：\d{3}
- 校验码：[0-9Xx]

[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]
```

**案例：**

```python
# ID number
import re

id_pattern = r"[1-9]\d{5}(?:[0-9]{2}|(?:[0-9]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]"
strs = '小明的身份证号是31032419991231321X，手机号码是13579246801'
re.findall(id_pattern, strs)

# result
['31032419991231321X']
```

> 3. 国内手机号码

手机号码都是11位数字，且都是以1开头，后面跟上10位数字。

**表达式：**

```shell
1(3|4|5|6|7|8|9)\d{9}
```

**案例：**

```python
# mobile number
import re

phone_pattern = r'1[3-9]\d{9}'
strs = '我的手机号码是13579246801'
re.findall(phone_pattern, strs)

# result
['13579246801']
```

> 4. 国内固定电话

区号一般3-4位，号码7-8位

**表达式：**

```shell
\d{3,4}-\d{7,8}
```

**案例：**

```python
# phone number
import re

phone_pattern = r'\d{3,4}-\d{7,8}'
strs = '我的座机电话是0371-86624508，公司总部电话是010-85554666'
re.findall(phone_pattern, strs)

# result
['0371-86624508', '010-85554666']
```

> 5. 域名

域名包含：http:// 或者 https://

**表达式：**

```shell
(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)
```

**案例：**

```python
# domain name
import re

domain_pattern = r'(?:(?:http:\/\/)|(?:https:\/\/))?(?:[\w](?:[\w\-]{0,61}[\w])?\.)+[a-zA-Z]{2,6}(?:\/)'
strs = 'Python的官网地址是：https://www.python.org/'
re.findall(domain_pattern, strs)

# result
['https://www.python.org/']
```

> 6. IP地址

ip地址的长度是32位，分为4段，每段8位，范围是0～255，段与段之间用句点隔开

**表达式：**

```shell
((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?;25[0-5]|2[0-4]\d|[01]?\d?\d))
```

**案例：**

```python
# ip
import re

ip_pattern = r'((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))'
strs = '''请输入合法地址:
192.168.1.1
192.168.8.85
0.0.0.1
255.255.255.0
256.1.1.1
aa.bb.cc.dd
'''
re.findall(ip_pattern, strs)

# result
['192.168.1.1', '192.168.8.85', '0.0.0.1', '255.255.255.0', '56.1.1.1']
```

> 7. 日期

常见的日期格式有：yyyyMMdd、yyyy-MM-dd、yyyy/MM/dd、yyyy.MM.dd

**表达式：**

```shell
\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}
```

**案例：**

```python
# date match
import re

date_pattern = r"\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}"
strs = '今天是2021/01/02，去年的今天是2020.1.2，明年的今天是2022-01-02，明天是20200102.'

re.findall(date_pattern, strs)

# result
['2021/01/02', '2020.1.2', '2022-01-02', '20200102']
```

> 8. 国内邮政编码

**表达式：**

```bash
[1-9]\d{5}(?!\d)
```

**案例：**

```python
# postal code match
import re

code_pattern = r'[1-9]\d{5}(?!\d)'
strs = '杭州西湖区邮编是310012'

re.findall(code_pattern, strs)

# result
['310012']
```

> 9. 密码

密码(字母开头，长度在6-18之间，只能包含数字、字母、下划线)

强密码(字母开头，必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间)

**表达式：**

```bash
[a-zA-Z]\w{5,17}
```

**案例：**

```python
# cypher match

# weak cypher
import re

cypher_pattern = r'[a-zA-Z]\w{5,17}'
strs = '密码：q123456_abc'

re.findall(cypher_pattern, strs)

# result
['q123456_abc']


# strong cypher
import re

cypher_pattern = r'[a-zA-Z](?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}'
strs = '强密码：q123456ABc，弱密码：q123456abc'

re.findall(cypher_pattern, strs)

# result
['q123456ABc，']
```

> 10. 中文字符

**表达式：**

```bash
[\u4e00-\u9fa5]
```

**案例：**

```python
# Chinese match
import re

chinese_pattern = r'[\u4e00-\u9fa5]'
strs = 'apple：苹果'

re.findall(chinese_pattern, strs)

# result
['苹', '果']
```


import urllib.request
import re
import sys


def ISIP(s):
    # 判断是不是ip
    # 将ip字符串转换为列表
    len_ip = [i for i in s.split(".") if (0 <= int(i) <= 255)]
    return len(len_ip) == 4

def URL(ip):
    uip = urllib.request.urlopen('http://wap.ip138.com/ip.asp?ip=%s'%ip)
    fip = uip.read()
    rip = re.compile(r"<br/><b>查询结果：(.*)</b><br/>")
    result = rip.findall(fip.decode("utf-8"))
    print("URL_result:", result)
    print("%s\t %s" % (ip, result[0]))

def DO(domain):
    url = urllib.request.urlopen('http://wap.ip138.com/ip.asp?ip=%s'%domain)
    f = url.read()
    r=re.compile(r'&gt; (.*)<br/><b>查询结果：(.*)</b><br/>')
    result=r.findall(f.decode("utf-8"))
    print("DOMAIN_result", result)
    for i in result:
        print("%s\t %s\t %s\t" %(domain, i[0], i[1]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("sys.arg[0]：", sys.argv[0])
        print("请输入IP地址或者域名（如：192.168.0.1 / www.baidu.com）")
        sys.exit()
    # 获取输入的ip地址，可替代input()用法
    INPUT = sys.argv[1]
    # if not re.findall(r'(\d{1,3}\.){3}\d{1,3}', INPUT):
    if not re.findall(r'(\d{1,3}\.)(\d{1,3}\.)(\d{1,3}\.)(\d{1,3})', INPUT):
        if re.findall(r'(\w+\.)?(\w+)(\.\D+){1,2}', INPUT) :
            DOMAIN = INPUT
            DO(DOMAIN)
        else:
            print("输入的IP地址和域名格式不对！")
    else:
        if ISIP(INPUT)  :
            IPADDRESS = INPUT
            URL(IPADDRESS)
        else:
            print("IP 地址不合法，请重新输入！")

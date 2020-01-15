def f1vsf2(name1,name2):
    f1 = open(name1)
    f2 = open(name2)
    count = 1
    msg=[]
    for line1 in f1:
        line2 = f2.readline()
        if(line1!=line2):
            msg.append("第%d行不一样"%count)
        count+=1
    f1.close()
    f2.close()
    return msg


if __name__ == "__main__":
    isbool = True
    while isbool:
        fname1 = input("请输入要比较的文件1路径及文件名:")
        if fname1 =='':
            print("文件名不能为空，请重新输入")
            continue;
        fname2 = input("请输入要比较的文件2路径及文件名:")
        if fname2 =='':
            print("文件名不能为空，请重新输入")
            continue;
        result = f1vsf2(fname1,fname2)
        if len(result)==0:
            print("两个文件完全一致")
        else:
            print("两个文件共有【%d】行不同"%len(result))
            for msg in result:
                print(msg)
        isbool = False

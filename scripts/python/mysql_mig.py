import os

#from pathlib import Path
import sys

import paramiko
import pymysql

#每次只能迁移一个DB下的表，到指定DB
#GRANT SELECT, CREATE, RELOAD, ALTER, LOCK TABLES ON *.* TO 'data_migration'@'192.168.%' IDENTIFIED BY 'data_migration@123';
tables='sqlauto_cluster,sqlauto_user'    #以，分割的字符串，如a,b,c
tableList = tables.split(',')
sourceIp = '192.168.1.101'
sourceDataBase = '/data/mysql/3306/data'
sourceDbName = 'inception_web'
sourceDataDir = os.path.join(sourceDataBase,sourceDbName)
desIp = '192.168.1.102'
desDataBase = '/data/mysql/3306/data'
desDbName = 'inception_web'
desDataDir = os.path.join(desDataBase,desDbName)
 
comUser = 'data_migration'
comPwd = 'data_migration@123'
comPort = 3306
 
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
def table_judge():
    print("table_judge")
    sourceTableExist = pymysql.connect(sourceIp,comUser,comPwd,sourceDbName,comPort,charset='utf8')
    desTableExist = pymysql.connect(desIp,comUser,comPwd,desDbName,comPort,charset='utf8')
    sourceTables = []
    desTables = []
    cursor_source = sourceTableExist.cursor()
    cursor_des = desTableExist.cursor()
    
    for table in tableList:
        #print(table)
        cursor_source.execute("select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (sourceDbName,table))
        sourceTable_tmp = cursor_source.fetchall()
        cursor_des.execute("select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s';" % (desDbName,table))
        desTable_tmp = cursor_des.fetchall()
        #print(desTable_tmp)
        if sourceTable_tmp is ():
        sourceTables.append(table)
        if desTable_tmp is not ():
        desTables.append(desTable_tmp[0][0])
    sourceTableExist.close()
    desTableExist.close()
    
    s=d=0
    if sourceTables != []:
        print('迁移源不存在将要迁移的表：',sourceIp,sourceDbName, sourceTables,' 请检查')
        s=1
    if desTables != []:
        print('目标库存在将要迁移的表：',desIp,desDbName,desTables,' 请移除')
        d=1
    if s == 1 or d == 1:
        sys.exit()
 
def data_sync():
    print('data_sync')
    db_source = pymysql.connect(sourceIp,comUser,comPwd,sourceDbName,comPort,charset='utf8')
    db_des = pymysql.connect(desIp,comUser,comPwd,desDbName,comPort,charset='utf8')
    cursor_db_source = db_source.cursor()
    cursor_db_des = db_des.cursor()
    
    for table in tableList:
        print("正在同步表：",table)
        cursor_db_source.execute("show create table %s;" % (table))
        createTableSQL = cursor_db_source.fetchall()[0][1]
        print(createTableSQL)
        try:
        cursor_db_des.execute(createTableSQL)
        except Exception as error:
        print(error)
        cursor_db_source.execute("flush table %s with read lock;" % (table))
        cursor_db_des.execute("alter table %s discard tablespace;" % (table))
    
        client.connect(sourceIp, 22, 'root')
        stdin1, stdout1, stderr1 = client.exec_command("scp %s %s:%s " % (sourceDataDir+"/"+table+".ibd", desIp, desDataDir))
        stdin2, stdout2, stderr2 = client.exec_command("scp %s %s:%s " % (sourceDataDir+"/"+table+".cfg", desIp, desDataDir))
        a_e_1 = stderr1.readlines()
        a_e_2 = stderr2.readlines()
        if a_e_1 != [] or a_e_2 != []:
        print(a_e_1,a_e_2)
        sys.exit()
        client.close()
    
        client.connect(desIp, 22, 'root')
        stdin3, stdout3, stderr3 = client.exec_command("chown -R mysql.mysql %s*" % (desDataDir+"/"+table))
        a_e_3 = stderr3.readlines()
        if a_e_3 != []:
        print(a_e_1, a_e_2)
        sys.exit()
        client.close()
        #cursor_db_source.execute("select sleep(10);")
        cursor_db_source.execute("unlock tables;")
        cursor_db_des.execute("alter table %s import tablespace;" % (table))
        print("同步完成")
    
    cursor_db_source.close()
    cursor_db_des.close()
 
def data_checksum():
    print('data_checksum')
    db_source = pymysql.connect(sourceIp,comUser,comPwd,sourceDbName,comPort,charset='utf8')
    db_des = pymysql.connect(desIp,comUser,comPwd,desDbName,comPort,charset='utf8')
    cursor_db_source = db_source.cursor()
    cursor_db_des = db_des.cursor()

    for table in tableList:
    print("正在校验表：", table)
    cursor_db_source.execute("checksum table %s;" % (table))
    ck_s = cursor_db_source.fetchall()[0][1]
    cursor_db_des.execute("checksum table %s;" % (table))
    ck_d = cursor_db_des.fetchall()[0][1]
    if ck_s != ck_d:
        print("表不一致：",table)
    else:
        print("表一致：",table)

    cursor_db_source.close()
    cursor_db_des.close()
 
if __name__ == "__main__":
    table_judge()
    data_sync()
    data_checksum()
    print('haha')
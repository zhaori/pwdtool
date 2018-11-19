import os,sys
import sqlite3
from model import *
#创建数据库，如果没有的话就会自己创建，有的话就跳过
class sql_data(object):

    def new_data(self,md):
        # 数据库创建、插入表
        #md是model.py里的模板
        count = sqlite3.connect(db_path)
        con = count.cursor()
        con.execute(md)
        con.close()
        print("Create a successfully")


    def add_data(self,sql,num,username,password,email,url,note):
        add_data = {"id": num, "username": username, "password": password,"email": email,"url":url,"note": note}
        #数据库增添数据
        count = sqlite3.connect(db_path)
        con = count.cursor()
        con.execute(sql,add_data) #1
        count.commit()
        con.close()
        print("add a successfully")

    def search_data(self,query,table):
        #查询数据
        connt=sqlite3.connect(db_path)
        con=connt.cursor()
        sql_data=con.execute("select "+query+" from "+table)
        all_table=sql_data.fetchall()
        print(all_table)
        connt.close()

    def update_data(self,table,commod,num):
        #更新数据
        connt = sqlite3.connect(db_path)
        con = connt.cursor()
        sql_data = con.execute("update "+table+" set "+commod+" where id="+num)
        connt.commit()
        connt.close()
        print("update a successfully")

    def delete_data(self,table,element):
        #删除数据table,element,num
        connt=sqlite3.connect(db_path)
        con=connt.cursor()
        del_data=con.execute("delete from "+table+" where "+element)
        connt.commit()
        connt.close()
        print("delete a successfully")

if __name__ == '__main__':

    Help="""
        -help       显示帮助列表
        -n          创建新的数据库及表
        -a          插入数据
        -u          更新数据
        -d          删除数据
        -p          查看密码
        -s          查询数据
        -del        删除数据库（慎用）
        -open       查看原密码
        查询元素是指id,username,password这类变量
    """
    s=sql_data()
    if sys.argv[1] == "-help":
        print(Help)

    elif sys.argv[1]=="-del":
        os.system("del Note.db")

    elif sys.argv[1]=="-n":
        s.new_data(md=sql_mode)

    elif sys.argv[1]=="-a":
        id = input("id:")
        user_name = input("username:")
        pass_word = input("password:")
        email_ = input("Email:")
        url_ = input("url:")
        note_ = input("note:")
        pwd_hash = ha_hash(password=pass_word, salt=salt)
        dict_li={
            "username":{
                user_name
            },
            pwd_hash:{
                    pass_word
                }
        }
        with open("pwd.json","a+",encoding="utf-8") as f:
            f.write(str(dict_li))
        s.add_data(sql=data_1,num=id,username=user_name,password=ha_hash(password=pass_word,salt=salt),email=email_,url=url_,note=note_)

    elif sys.argv[1]=="-s":
        comd=input("输入查询元素：")
        table_1=input("输入表：")
        s.search_data(query=comd,table=table_1)

    elif sys.argv[1]=="-p":
        connt = sqlite3.connect(db_path)
        con = connt.cursor()
        sql_data = con.execute("select password from Windows")
        all_table = sql_data.fetchall()
        for i in all_table:
            with open("pwd","w",encoding="utf-8") as f:
                f.write(str(i[0]+"\n"))
        connt.close()
    elif sys.argv[1]=="-open":
        with open("pwd.json","r",encoding="utf-8") as f1:
            print(f1.read())

    elif sys.argv[1]=="-u":
        windows=input("表名：")
        commod=input("更新元素：")
        id=input("id:")
        s.update_data(table=windows,commod=commod,num=id)

    elif sys.argv[1]=="-d":
        table_2 = input("表名：")
        name=input("制定元素删除：")
        s.delete_data(table=table_2,element=name)

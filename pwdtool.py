import os
import sqlite3
import sys
from config import *
from safety import *


class Save_Password(object):

    def __init__(self, table, mode, sql, path):
        self.table = table  # 表名
        self.mode = mode  # 插入表
        self.sql = sql  # 插入数据
        self.dbpath = path  # 数据库存储路径

    def new_sql(self):
        # 数据库创建、插入表
        # md是model.py里的模板
        with sqlite3.connect(self.dbpath) as con:
            con.execute(self.mode)
            print('Start database successfully')

    def add_sql(self, add_data):
        # 增添数据
        with sqlite3.connect(self.dbpath) as con:
            #con.text_factory = str      #处理SQLite数据库的中文字符存储编码问题
            con.execute(self.sql, add_data)
            print(add_data, 'Add data successfully')

    def delete_sql(self, element):
        # 删除表里的某一项数据table,element
        with sqlite3.connect(self.dbpath) as con:
            con.execute(
                "delete from " + self.table + " where " + element
            )
            print("delete a %s successfully" % element)

    def delete_table(self, table_name):
        # 删除表
        with sqlite3.connect(self.dbpath) as con:
            con.execute("drop table " + table_name)
            print('database %s delete successfully' % table_name)

    def search_sql(self, query):
        # 查询数据
        with sqlite3.connect(self.dbpath) as con:
            sql_data = con.execute(
                "select " + query + " from " + self.table
            )
            all_table = sql_data.fetchall()

        for i in all_table:
            dict_data = {
                'id': i[0],
                '用户名': i[1],
                '密码': i[2],
                '邮箱': i[3],
                '网址': i[4],
                '备注': bytes(i[5]).decode()
            }
            print(dict_data)

    def update_sql(self, table, value, data, id):
        # 更新数据
        with sqlite3.connect(self.dbpath) as con:
            con.execute(
                "update %s set %s = '%s' where id = %d"
                % (table, value, data, id)
            )
            # con.execute('update pwd set username = "zzg" where id = 1')
        print('update %s \'s %s successfully ' % (table, value))


if __name__ == '__main__':

    Help = """
            -help        显示帮助列表
            -n           创建新的数据库及表
            -a           添加数据
            -u           更新数据
            -s           查看数据
            -table       查看数据库已有表名
            -del         删除数据库（慎用） 
            -del -data   删除表某个数据
            -del -table  删除表
            -o           查看原密码
            查询元素是指id,username,password这类变量

    """
    # 程序开始begin，初始化
    sha = SHA3()
    s = Save_Password('pwd', sql_mode, sql_data, db_path)
    ss = Save_Password('supper', sql_mode_two, sql_data_two, db_path)
    aes = database_safe(db_path)
    if not os.path.exists('data'):
        os.mkdir('data')

    def str_to_tuple(n):
        # 这个函数是处理从数据库读取后将格式转化为元祖用于读取
        return tuple(eval(str(n).strip('[]')))


    if sys.argv[1] == "-help":
        print(Help)

    elif sys.argv[1] == "-del":
        if os.uname() == 'win':
            os.system("del %s" % db_path)
        else:
            os.system('rm %s ' % db_path)

    elif sys.argv[1] == '-del' and sys.argv[2] == '-data':
        #删除表里的某项数据
        data = input('Please input your hope delete data:')
        s.delete_sql(data)

    elif sys.argv[1] == '-del' and sys.argv[2] == 'table':
        #删除数据库里的某个表
        table = input('Please input you hope delete table name')
        s.delete_table(table)

    elif sys.argv[1] == "-n":
        #第一步 创建数据库并生成对应的加密秘钥
        s.new_sql()
        ss.new_sql()
        aes.endb()

    elif sys.argv[1] == "-a":
        aes.dedb()
        user_name = input("username:")
        pass_word = input("password:")
        email_ = input("Email:")
        url_data = input("url:")
        note_data = input("note:")
        pwd_hash = sha.cal(pass_word)

        data = {
            'username': user_name,
            "password": sha.cal(pass_word),
            'email': email_,
            'url': url_data,
            'note': note_data.encode('utf-8')
        }

        data_supper = {
            'username': user_name,
            'SHA': sha.cal(pass_word),
            'password': pass_word,
        }
        s.add_sql(data)
        ss.add_sql(data_supper)
        aes.endb()

    elif sys.argv[1] == "-s":
        aes.dedb()
        print(s.search_sql(search_sql))
        aes.endb()

    elif sys.argv[1] == '-u':
        # 如果更新的元素是password即密码，
        # 则supper表里的元素都要随着pwd表的更新而更新
        aes.dedb()
        tb = input('输入更新table：')
        id = input('输入id：')
        value = input('输入更新列：')
        data = input('输入更新数据：')
        s.update_sql(tb, value, sha.cal(data), int(id))
        if value == 'password':
            sql = sha.cal(data)
            ss.update_sql('supper', 'password', data, int(id))
            ss.update_sql('supper', 'SHA', sha.cal(data), int(id))
        aes.endb()

    elif sys.argv[1] == '-o':
        #查看密码
        aes.dedb()
        with sqlite3.connect(db_path) as con:
            sql_data_pwd = con.execute(
                'select url,username,password from pwd'
            )
            sql_d = con.execute(
                'select username,SHA,password from supper'
            )
            data = sql_data_pwd.fetchall()
            pwd_data = sql_d.fetchall()
            #print(pwd_data)
            print_data = {
                '网址': str_to_tuple(data)[0],
                '用户名': str_to_tuple(data)[1],
                '加密密码': str_to_tuple(data)[2],
                '真实密码': str_to_tuple(pwd_data)[2]
            }
            """
            for i in range(0, len(str_to_tuple(data))):
                print_data = {
                    '网址': str_to_tuple(data)[int(i)][0],
                    '用户名': str_to_tuple(str_to_tuple(data))[int(i)][1],
                    '加密密码': str_to_tuple(str_to_tuple(data))[int(i)][2],
                    '真实密码': str_to_tuple(pwd_data)[int(i)][2]
                    # '真实密码' : str_to_tuple(pwd_data[1])
                }
             """
            print(print_data)
           
        aes.endb()
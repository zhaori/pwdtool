import hashlib
sql_mode="""create table Windows(
           id int,
           username text,
           password text,
           email text,
           url text,
           note text
           )
        """

db_path=r"./Note.db"

data_1="""insert into Windows
        (id,username,password,email,url,note) 
        values
        (:id,:username, :password,:email,:url,:note)"""

def ha_hash(password,salt):
    data = password + salt
    text=hashlib.md5(data.encode("utf8"))
    return text.hexdigest()


"""
#SQLite3数据库操作： 建库,建表,添加,查询,修改,删除

 
#C:\>sqlite3 mydatabase.db 
#sqlite> create table user(id integer,username text,password text); 
#sqlite> insert into user values(1,'king','king'); 
#sqlite> select * from user; 
#sqlite> update user set username='kong',password='kong' where id=1; 
#sqlite> delete from user where username='kong';
"""

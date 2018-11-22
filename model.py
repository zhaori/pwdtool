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
sql_mode可以自己修改，相应的data_1也要修改
"""

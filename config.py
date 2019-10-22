sql_mode = """create table pwd(
           [id] integer PRIMARY KEY AUTOINCREMENT,
           username text,
           password text,
           email text,
           url text,
           note text
           )
        """
sql_mode_two = """
            create table supper(
            [id] integer PRIMARY KEY AUTOINCREMENT,
            username text,
            SHA text,
            password text
            )
            
"""
#数据库路径
db_path = r"Note.db"

sql_data = """insert into pwd
        (username,password,email,url,note) 
        values
        (:username, :password,:email,:url,:note)"""

sql_data_two = """
        insert into supper
        (username, SHA, password)
        values 
        (:username, :SHA, :password)

"""

search_sql = 'id,username,password,email,url,note'

"""
sql_mode可以自己修改，相应的data也要修改
"""

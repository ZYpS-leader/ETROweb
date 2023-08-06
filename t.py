import pymysql as sql
connect=sql.connect(host="127.0.0.1",port=3306,user="root",password="Eto20230403",charset="utf8")
cursor=connect.cursor()
cursor.execute("use etroweb");connect.commit()

cursor.execute("select %s",("Hello world!"))
print(cursor.fetchall())
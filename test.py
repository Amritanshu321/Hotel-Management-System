import pymysql
conn=pymysql.connect(host='localhost',user='root',db='myhotel')
print("connection established")
mycursor=conn.cursor()
que= 'select item_name from itemlist'
mycursor.execute(que)
conn.commit()
l=[]
'''
l.append(mycursor.fetchall())
print(l)
'''
def d():
        for row in mycursor.fetchall():
                l.append(row[0])
                print(row[0])
        return l
d()
print("l=",l)
print(l)
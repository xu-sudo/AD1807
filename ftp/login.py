from def_sql import Mysqlpython
from hashlib import sha1

name=input('请输入用户名：')
pwd=input('请输入密码：')
#sha1加密
s1=sha1()
s1.update(pwd.encode("utf8"))#指定编码
pwd2=s1.hexdigest()
a=Mysqlpython("stu")
sql="select password from user where username=%s;"
ret=a.all(sql,[name])
if len(ret)==0:	
	print("用户名错误")
elif ret[0][0]==pwd2:
	print("登录成功")

	
from socket import *
import signal
from time import sleep
import os,sys


#客户端处理函数
def client_hangdler(c):
	print('处理子进程请求',c.getpeername())
	try:
		while True:
			data=c.recv(1024)
			if not data:
				break
			print(data.decode())
			c.send('收到服务器消息'.encode())
	except (KeyboardInterrupt,SystemError):
		sys.exit('客户端退出')
	except Exception as e:
		print(e)
	c.close()
	sys.exit()
s=socket(AF_INET,SOCK_STREAM)
s.bind(('0.0.0.0',8888))
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.listen(5)
print('等待%s客户端连接'%os.getpid())
#父进程忽略子进程状态改变，子进程退出自动由系统处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
while True:	
	try:
		c,addr=s.accept()
		
	except KeyboardInterrupt:
		sys.exit('服务器退出')
		
	except Exception as e:
		print('异常',e)
		continue


	pid=os.fork()
	if pid==0:
		s.close()
		client_hangdler(c)		
	else:
		c.close()
		continue

			
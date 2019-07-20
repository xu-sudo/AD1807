from socket import *

sockfd=socket(AF_INET,SOCK_STREAM)
#发起连接
ser_addr=('127.0.0.1',8888)
sockfd.connect(ser_addr)
while True:    	
	data=input('发送>>')
	sockfd.send(data.encode())
	if not data:
		break
	data=sockfd.recv(1024)
	print('收到消息',data.decode())
sockfd.close()
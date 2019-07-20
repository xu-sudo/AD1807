from socket import *
import signal
from time import sleep
import os,sys


class FtpClient():
	"""docstring for FtpServer"""
	def __init__(self, sockfd):
		self.sockfd=sockfd
	def do_list(self):
		self.sockfd.send(b'L') #发送请求
        #等待回复
		data = self.sockfd.recv(1024).decode()		
		if data == 'OK':
			print(data)
			data = self.sockfd.recv(4096).decode()
			files = data.split('#')
			for file in files:
				print(file)
			print("文件列表展示完毕\n")
		else:
            #由服务器发送失败原因
			print(data)
	#下载文件
	def do_get(self,filename):
		self.sockfd.send(('G '+filename).encode()) #发送请求
        #等待回复
		data = self.sockfd.recv(1024).decode()		
		if data == 'OK':
		    fd=open(filename,'wb')
		    while True:
		    	data=self.sockfd.recv(1024)
		    	if data==b'##':
		    		break
		    	fd.write(data)
		    fd.close()
		    print('下载完毕')
		else:
			print(data)
	def do_put(self,filepath):

		try:
			fd=open(filepath,'rb')
		except:
			print('文件不存在,请重新输入')
			return
		self.sockfd.send(('P '+filepath).encode()) #发送请求
        #等待回复
		data = self.sockfd.recv(1024).decode()		
		if data == 'OK':			
			while True:
				data=fd.read(1024)
				if not data:
					#防止粘连
					sleep(0.1)
					self.sockfd.send(b'##')
					break
				self.sockfd.send(data)
		fd.close()
		print('文件发送完毕')
	def do_quit(self):
		self.sockfd.send('Q'.encode())
		
def main():	
	sockfd=socket(AF_INET,SOCK_STREAM)
	#发起连接
	ser_addr=('127.0.0.1',8888)
	try:
		sockfd.connect(ser_addr)
	except:
		print('连接服务器失败')
		return
	ftp=FtpClient(sockfd)
	while True:    	
		print("==========命令选项=========")
		print("**********list************")
		print("********get file**********")
		print("********put file**********")
		print("**********quit************")
		print("==========================")
		data=input('请输入选项:')
		if data.strip() == 'list':
			ftp.do_list()
		elif data[:3]=='get':
			filename=data.split(' ')[-1]
			ftp.do_get(filename)
		elif data[:3]=='put':
			filepath=data.split(' ')[-1]
			ftp.do_put(filepath)
		elif data.strip()=='quit':			
			ftp.do_quit()
			sockfd.close()
			sys.exit('谢谢使用')
		else:
			print('请输入正确命令')
if __name__ == '__main__':
			main()
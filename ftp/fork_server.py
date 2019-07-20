from socket import *
import signal
from time import sleep
import os,sys

FILE_PATH='/home/yuanchao/phase2/mysql/day05/'
#客户端处理函数
class ftp_server():
	"""docstring for ftp_server"""
	def __init__(self, connfd):		
		self.connfd=connfd
	def do_list(self):
		print('客户端进入xu')
		file_list=os.listdir(FILE_PATH)
		
		if not file_list:
			self.connfd.send('文件为空'.encode())
		else:
			self.connfd.send(b'OK')
			sleep(0.1)
		files = ''
		
		for file in file_list:	
			files = files + file + '#'
			print('files')	
		self.connfd.sendall(files.encode())
	def do_get(self,filename):
			path=FILE_PATH+filename
			try:
				fd=open(path,'rb')
			except:
				self.connfd.send('文件不存在'.encode())
				return
			self.connfd.send(b'OK')
			sleep(0.1)
			while True:
				data=fd.read(1024)
				if not data:
					#防止粘连
					sleep(0.1)
					self.connfd.send(b'##')
					break
				self.connfd.send(data)
			print('文件发送完毕')
	def do_put(self,filename):
		
		path=FILE_PATH+filename
		fd=open(path,'wb')
		self.connfd.send(b'OK')

		while True:
		   	data=self.connfd.recv(1024)	
		   	if data==b'##':
		   		break
		   	fd.write(data)
		fd.close()
		print('上传完毕')
		

def main():	
	s=socket(AF_INET,SOCK_STREAM)
	s.bind(('0.0.0.0',8888))
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.listen(5)
	print('等待%s客户端连接'%os.getpid())
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)
	while True:	
		try:
			connfd,addr=s.accept()
			print('客户端进入',addr)			
		except KeyboardInterrupt:
			sys.exit('服务器退出')			
		except Exception as e:
			print('异常',e)
			continue
		pid=os.fork()
		if pid==0:
			s.close()
			ftp=ftp_server(connfd)
			while True:
				data=connfd.recv(1024).decode()
				print(data)
				if not data:
					connfd.close()
					sys.exit()
				elif data[0]=='L':
					print('xu')
					ftp.do_list()
				elif data[0]=='G':
					print('G')
					filename=data.split(' ')[-1]
					print(filename)
					ftp.do_get(filename)
				elif data[0]=='P':
					print('P')
					data=data.split(' ')[-1]
					ftp.do_put(data)
		else:
			connfd.close()
			continue

if __name__ == '__main__':
			main()		
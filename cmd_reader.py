# coding=utf8
'''
此脚本实现了一个类：command_reader
当不断通过feedData喂数据是，此类可以解析出符合条件的命令，然后通过回调函数通知
'''
def printHex(cmd):
	for c in cmd:
		print(r'{:02x} '.format(c),end=r'')
	print()
class command_reader:
	def __init__(self,callback):
		self.__buffer=[]
		self.__callback=callback
		self.__header=[0xfe]
		self.__state = 0 #0 finding header , 1 finding end
		self.__lenCMD = 8
	def __call__(self,data):
		self.feedData(data)
	def feedData(self,data):
		for c in data:
			if self.__state == 0:
				#print(r'aa')
				if c == self.__header[0]:
					self.__state = 1
					self.__buffer=[c,]
			elif self.__state == 1:
				#print(self.__buffer)
				if c == self.__header[0]:
					self.__buffer=[c,]
				else:
					self.__buffer += [c,]
					if len(self.__buffer) == self.__lenCMD:
						self.__state = 0
						if self.__checkSum(self.__buffer):
							self.__callback(self.__buffer)
							self.__buffer=[]
						else:
							#checksum fail
							print(f'{self.__buffer} is invalid command')
	def __checkSum(self,cmd):
		return cmd[-1] == ( sum(cmd[:-1])&0xff )

if __name__ == "__main__":
	def callback(cmd):		
		print(f'command arrived: ',end='')
		printHex(cmd)
	reader=command_reader(callback)
	dat=[0xfe,0xfe,0,0,0,0,1,0x1f,0x1e,0xfe,1,0,0,0,0,0,0xff,0xfe]
	reader(dat)
	reader([0x02,0,0,0,0,0,3])
				
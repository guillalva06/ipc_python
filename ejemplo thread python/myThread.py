import time
import threading

class myThread (threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		self.account = 1
		print(self.running)
	def run(self):
		print('Running a little Thread')
		while(self.running):
			print('Thread '+self.name+' va en el conteo '+str(self.account))
			self.account = self.account + 1
			time.sleep(3)
	def stop_run(self):
		self.running = False



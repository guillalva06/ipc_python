import threading

class listenerDaemon(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.running = True
		self.queue = queue

	def run(self):
		print('Run Daemon Listener')
		while self.running:
			answer, _ = self.queue.receive()
			print('Answer Receive '+ answer)
			if answer == 'EXIT':
				self.running = False
		self.queue.close()
		self.queue.unlink()
		print('Exit Daemon Listener')

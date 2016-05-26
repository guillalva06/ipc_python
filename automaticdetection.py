import threading
import random
import time
import cv2

class automaticDetection(threading.Thread):
	def __init__(self, name,queue, lock):
		threading.Thread.__init__(self)
		self.name = name
		self.running = True
		self.queue = queue
		self.lock = lock
	def run(self):
		cont = 0
		print ('RUN Daemon')
		self.queue.send('First Message Daemon');
		while cont < 1:
			self.lock.acquire()
			cap = cv2.VideoCapture(0)
			cont = cont + 1
			while(True):
				# Capture frame-by-frame
				ret, frame = cap.read()
				# Our operations on the frame come here
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				# Display the resulting frame
				cv2.imshow('Frame Daemon',gray)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			# When everything done, release the capture
			cap.release()
			cv2.destroyAllWindows()
			self.lock.release()
			time.sleep(2)
		self.queue.send('EXIT\0')
		print ('EXIT Daemon')

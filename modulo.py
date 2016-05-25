from sys import stdin
from automaticdetection import automaticDetection
import posix_ipc
import threading
import cv2

#Import modules
config_file = open('config_file.txt','r')
import_modules = dict()
for line in config_file:
	data = line.strip().split(' ')
	import_modules[data[0]] = data[1]
deteccion = __import__(import_modules['deteccion'])
distancia = __import__(import_modules['distancia'])
orders_queue = posix_ipc.MessageQueue('/my_orders_queue', posix_ipc.O_CREAT)
answers_queue = posix_ipc.MessageQueue('/my_answers_queue', posix_ipc.O_CREAT)
async_queue = posix_ipc.MessageQueue('/my_async_queue', posix_ipc.O_CREAT)
lock = threading.Lock()
daemon = automaticDetection('Daemon',async_queue,lock)
daemon.start()
wait_data = True
while(wait_data):
	receive, _ = orders_queue.receive()
	receive = receive.replace('\n','').strip()
	print('Recibido: '+ receive)
	if receive == 'DETECCION\0':
		answer = deteccion.message()
		answers_queue.send(answer)
	elif receive == 'DISTANCIA\0':
		answer = distancia.message()
		answers_queue.send(answer)
	elif receive == 'EXIT\0':
		wait_data = False
		answers_queue.send(receive)
	elif receive == 'A\0':
		lock.acquire()
		cap = cv2.VideoCapture(0)
		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()
			# Our operations on the frame come here
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# Display the resulting frame
			cv2.imshow('Frame Principal',gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		lock.release()
	else:
		print('No es una opcion valida')
print('Exit main module')
orders_queue.close()
orders_queue.unlink()

	




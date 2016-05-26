from sys import stdin
from automaticdetection import automaticDetection
import posix_ipc
import threading
import cv2
import glob

def carga(img, objetivos):
    lista = glob.glob("*.jpg")
    for nom in lista:
        imagen = cv2.imread(nom)
        h1, w1, _ = img.shape
        h2, w2, _ = imagen.shape
        lim=cv2.resize(imagen, None,fx=(float(h1)/float(h2)), fy=(float(h1)/float(h2)), interpolation = cv2.INTER_CUBIC)
        objetivos[nom]=lim

#Import modules
config_file = open('config_file.txt','r')
import_modules = dict()
for line in config_file:
	data = line.strip().split(' ')
	import_modules[data[0]] = data[1]
deteccion = __import__(import_modules['deteccion'])
distancia = __import__(import_modules['distancia'])
#Add the objects to recognize
objetivos = {}
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
carga(frame, objetivos)
cap.release()
#Open the Queues
orders_queue = posix_ipc.MessageQueue('/my_orders_queue')
answers_queue = posix_ipc.MessageQueue('/my_answers_queue')
async_queue = posix_ipc.MessageQueue('/my_async_queue')
lock = threading.Lock()
#Create the Async Process
daemon = automaticDetection('Daemon',async_queue,lock)
answers_queue.send('First Answer Message')
daemon.start()
#Main loop
wait_data = True
while(wait_data):
	receive, _ = orders_queue.receive()
	receive = receive.replace('\n','').strip()
	print('Recibido: '+ receive)
	if receive == 'DETECCION\0':
		lock.acquire()
		cap = cv2.VideoCapture(0)
		ret, frame = cap.read()
		answer = deteccion.deteccion(frame,objetivos['72.jpg'])
		answers_queue.send(str(answer[0])+' '+str(answer[1])+' '+ str(answer[1])+'\0')
		cap.release()
		lock.release()
	elif receive == 'DISTANCIA\0':
		lock.acquire()
		cap = cv2.VideoCapture(0)
		answer = str(distancia.estimate_distance(cap))+'\0'
		answers_queue.send(answer)
		cap.release()
		lock.release()
	elif receive == 'EXIT\0':
		wait_data = False
		answers_queue.send(receive)
	else:
		answers_queue.send('No es una opcion valida\0')
print('Exit main module')
orders_queue.close()
async_queue.close()
answers_queue.close()


	




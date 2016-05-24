import posix_ipc
from sys import stdin
from listener import listenerQueue
from listenerdaemon import listenerDaemon

print('Consumer Client')

orders_queue = posix_ipc.MessageQueue('/my_orders_queue')
answers_queue = posix_ipc.MessageQueue('/my_answers2_queue')
async_queue = posix_ipc.MessageQueue('/my_async_queue')
listener = listenerQueue(answers_queue)
listener.start()
listenerdaemon = listenerDaemon(async_queue)
listenerdaemon.start()
send_data = True
while send_data:
	data = stdin.readline().strip()
	orders_queue.send(data)
	if data=='EXIT':
		send_data = False


	

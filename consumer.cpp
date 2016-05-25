#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <mqueue.h>

#include <iostream>
#include <cstdlib>
#include <pthread.h>

#include "common.h"

void *listener1(void *threadid)
{
	long tid;
	tid = (long)threadid;
	printf("Hello World 1! Thread ID");
	mqd_t answers_queue;
	char buffer[100];
	struct mq_attr attr;
	/* initialize the queue attributes */
	attr.mq_flags = 0;
	attr.mq_maxmsg = 10;
	attr.mq_msgsize = 100;
	attr.mq_curmsgs = 0;
	int cont = 0;
	answers_queue = mq_open("/my_answers_queue",O_CREAT | O_RDONLY, 0644, &attr);
	while(cont < 10){
		cont = cont + 1;
		int message_len = 0;
		message_len = mq_receive(answers_queue, buffer, 100, NULL);
		//puts(buffer);
		printf("Received: %s\n", buffer);
	}
	mq_close(answers_queue);
	pthread_exit(NULL);

}

void *listener2(void *threadid){
	long tid;
	tid = (long)threadid;
	printf("Hello World 2! Thread ID");
	mqd_t async_queue;
	char buffer[100];
	struct mq_attr attr;
	/* initialize the queue attributes */
	attr.mq_flags = 0;
	attr.mq_maxmsg = 10;
	attr.mq_msgsize = 100;
	attr.mq_curmsgs = 0;
	int cont = 0;
	async_queue = mq_open("/my_async_queue",O_CREAT | O_RDONLY, 0644, &attr);
	while(cont < 10){
		cont = cont + 1;
		int message_len = 0;
		message_len = mq_receive(async_queue, buffer, 100, NULL);
		//puts(buffer);
		printf("Received: %s\n", buffer);
	}
	mq_close(async_queue);
	pthread_exit(NULL);
}

int main(){
	mqd_t orders_queue;
	char buffer[101];
	orders_queue = mq_open("/my_orders_queue",O_WRONLY);
	pthread_t listener_answer;
	pthread_t listener_async;
	long i = 101;
	pthread_create(&listener_answer, NULL, listener1, (void *)i);
	i = 102;
	pthread_create(&listener_async, NULL, listener2, (void *)i);	
	while(true){		
		memset(buffer, ' ', 100);
		fgets(buffer, 100, stdin);
		mq_send(orders_queue, buffer, 100, 0);
	}
	printf("Hola Mundo");
	pthread_exit(NULL);
}

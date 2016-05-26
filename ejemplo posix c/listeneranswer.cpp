#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <mqueue.h>

#include "common.h"

int main(){
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
}

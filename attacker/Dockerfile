# Distribution usually used with HiBench

FROM ubuntu:latest

ADD atomicLocking.c /root/atomicLocking.c
ADD llcCleansing.c  /root/llcCleansing.c

RUN apt update && apt upgrade 
RUN echo Y | apt install gcc 
RUN echo Y | apt install nano

RUN cd /root && gcc atomicLocking.c -o atomicLocking && rm atomicLocking.c
RUN cd /root && gcc llcCleansing.c -o llcCleansing && rm llcCleansing.c



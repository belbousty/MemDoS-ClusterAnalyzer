#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE  10000000

int main() {
    int* array = malloc(ARRAY_SIZE * sizeof(int));
    while(1) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            array[i] = i;
        }

        clock_t start_time = clock();

        for (int i = 0; i < ARRAY_SIZE; i++) {
            int value = array[i];
        }
        clock_t end_time = clock();

        double elapsed_time = (double)(end_time - start_time) * 1000.0 / CLOCKS_PER_SEC;
        printf("Time to read from LLC: %.2f milliseconds\n", elapsed_time);
    }

    free(array);
    return 0;
}
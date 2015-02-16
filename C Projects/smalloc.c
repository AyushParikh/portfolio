/*

This program acts as a simple malloc function. Managing block of memory
    and ensure no leaks along the way.

*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include "smalloc.h"



void *mem;
struct block *freelist;
struct block *allocated_list;


void *smalloc(unsigned int nbytes) {
    struct block *memblock = freelist;
    struct block *prevblock = (struct block*)malloc(sizeof(struct block));
    prevblock->addr = NULL;
    prevblock->next = NULL;
    // find a block that is at least as large as the required byte size
    while (memblock->size <= nbytes){
        // if we can't find one, return NULL
        if (memblock->next == NULL){
            return NULL;
        }
        else{
            prevblock = memblock;
            memblock = memblock->next;
        }
    }
    struct block *alloblock;
    // if the allocated_list doesn't have a block in it yet
    if (allocated_list->size == 0){
        alloblock = allocated_list;
        allocated_list->addr = memblock->addr;
        allocated_list->size = nbytes;
    }
    else{
        alloblock = allocated_list;
        // move alloblock to the end of the allocated list
        while (alloblock->next != NULL){
            alloblock = alloblock->next;
        }
        // create a new block to append
        struct block *newblock = (struct block*)malloc(sizeof(struct block));
        newblock->addr = memblock->addr;
        newblock->size = nbytes;
        newblock->next = NULL;
        // append the new block to the end of the allocated list and move alloblock to it.
        alloblock->next = newblock;
        alloblock = alloblock->next;
    }
    // if the block we chose from the free list was larger than what we needed
    if((memblock->size - nbytes) != 0){
        // move its address to the new start point
        memblock->addr = ((char*)(memblock->addr)) + nbytes;
        // reduce its size to the remaining bytes
        memblock->size = memblock->size - nbytes;
    }
    // if it was the same size
    else{
        // if the block we used wasn't the first element of freelist
        if (prevblock->addr != NULL){
            // take the previous item and have it skip over our memblock
            prevblock->next = memblock->next;
        }
        else{
            // start the freelist past memblock
            freelist = memblock->next;
        }
        // in this case, memblock in no longer in either list, so free it
        free(memblock);
    }
    return alloblock->addr;
}


int sfree(void *addr) {
    struct block *presblock = allocated_list;
    struct block *prevblock = (struct block*)malloc(sizeof(struct block));
    prevblock->addr = NULL;
    prevblock->next = NULL;
    // find the block we want to free in the allocated list
    while(presblock->addr != addr){
        // if we can't find it return -1
        if (presblock->next == NULL){
            return -1;
        }
        prevblock = presblock;
        presblock = presblock->next;
    }
    // note the address where the block we are freeing begins and ends
    char *front,*back;
    front = (char*)presblock->addr;
    back = front + presblock->size;

    struct block *freeblock = freelist;
    // go through the free list and check to see if any of the blocks should be connected to our presblock
    while ((freeblock->next != NULL)&&((char*)freeblock->addr != back)&&((char*)freeblock->addr + freeblock->size != (front))) {
        freeblock = freelist->next;
    }
    // if we found a block whose start is our presblock's end
    if((char*)freeblock->addr == (back)){
        // move this freeblock's address back to include our block and increase the size accordingly
        freeblock->addr = (void*)((char*)freeblock->addr - presblock->size);
        freeblock->size = freeblock->size + presblock->size;
        // if our presblock wasn't at the begining of the allocated list
        if(prevblock->addr != NULL){
            // skip over it
            prevblock->next = presblock->next;
        }
        else{
            // bump the allocated list forward and past it.
            allocated_list = presblock->next;
        }
        // this block is no longer in use
        free(presblock);
    }
    // if we found a block whose end is the start of our presblock
    else if((char*)freeblock->addr + freeblock->size == (front)){
        // increase the size of the freeblock to include our presblock
        freeblock->size = freeblock->size + presblock->size;
        struct block *nextblock = freeblock->next;
        // if this larger freeblock stretches to the next block in the freelist
        if((char*)freeblock->addr + freeblock->size == (char*)nextblock->addr){
            // again, increase freeblock's size to include it and skip over the included block
            freeblock->size = freeblock->size + nextblock->size;
            freeblock->next = nextblock->next;
            // we no longer use this block
            free(nextblock);
        }
        // if our presblock wasn't at the begining of the allocated list
        if(prevblock->addr != NULL){
            // skip over it
            prevblock->next = presblock->next;
        }
        else{
            // bump the allocated list forward and past it.
            allocated_list = presblock->next;
        }
        // this block is no longer in use
        free(presblock);
    }
    // if our presblock doesn't share an edge with any other block in freelist
    else if(freeblock->next == NULL){
        struct block *nextblock = freelist;
        struct block *lastblock = (struct block*)malloc(sizeof(struct block));
        lastblock->next = NULL;
        lastblock->addr = NULL;
        // find the point in freelist where presblock's address fits
        while((presblock->addr > nextblock->addr)&&(nextblock->next != NULL)) {
            lastblock = nextblock;
            nextblock = nextblock->next;
        }

        /* HERE WE DIGRESS TO DEAL WITH THE ALLOCATED LIST */
        // if our presblock wasn't at the begining of the allocated list
        if(prevblock->addr != NULL){
            // skip over it
            prevblock->next = presblock->next;
        }
        else{
            // bump the free list forward and past it.
            allocated_list = presblock->next;
        }
        /* BACK TO ADDING OUR BLOCK INTO THE FREELIST */
        // if the presblock has an address larger than all the rest in the freelist
        if((nextblock->next == NULL)&&(presblock->addr > nextblock->addr)){
            // append it to the end
            nextblock->next = presblock;
        }
        // if the presblock has a smaller address than the freelist

        else if((presblock->addr < nextblock->addr)&&(lastblock->next == NULL)){
            // append it to the front
            presblock->next = nextblock;
            freelist = presblock;
        }
        // if presblock's address is somewhere in between
        else if((presblock->addr < nextblock->addr)&&(lastblock->next != NULL)){
            // insert it between the blocks
            presblock->next = nextblock;
            lastblock->next = presblock;
        }
        /* NOTE: we can't free presblock in this case because it hasn't been absorbed into another block */
    }
    // let's really hope this never happens
    else{
        return -1;
    }
    // everything turned out alright
    return 0;
}

void mem_init(int size) {
    mem = mmap(NULL, size,  PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    if(mem == MAP_FAILED) {
         perror("mmap");
         exit(1);
    }
    // initialize the free and allocated block lists
    allocated_list = (struct block*)malloc(sizeof(struct block));
    // I use NULL address and next pointers as a termination indication for my while loops
    allocated_list->addr = NULL;
    allocated_list->next = NULL;
    freelist = (struct block*)malloc(sizeof(struct block));
    freelist->addr = mem;
    freelist->size = size;    
    freelist->next = NULL;
}

void mem_clean(){
    struct block *freeblock = freelist;
    struct block *freeblocknext;
    // free all the blocks in the freelist
    while((freeblocknext = freeblock->next) != NULL){
        free(freeblock);
        freeblock = freeblocknext;
    }
    free(freeblock);
    struct block *alloblock = allocated_list;
    struct block *alloblocknext;
    // free all the blocks in the allocated list
    while((alloblocknext = alloblock->next) != NULL){
        free(alloblock);
        alloblock = alloblocknext;
    }
    free(alloblock);
}


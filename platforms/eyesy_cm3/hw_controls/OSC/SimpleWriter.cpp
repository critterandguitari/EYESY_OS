#include "SimpleWriter.h"
#include <stdio.h>

void SimpleWriter::start(void){
    bufferIndex = 0;
}

void SimpleWriter::end(void){
    length = bufferIndex;
}

void SimpleWriter::write(uint8_t b){
//    printf("%x ", b);

    buffer[bufferIndex] = b;
    bufferIndex++;
}

void SimpleWriter::write(const uint8_t *buffer, int size) {  while(size--) write(*buffer++); }



#ifndef SimpleWriter_h
#define SimpleWriter_h


#include <stdint.h> 


class SimpleWriter
{

public:
    uint8_t buffer[256];
    uint8_t bufferIndex;
    uint8_t length;
    void start(void);
    void end(void);
	void write(uint8_t b);
    void write(const uint8_t *buffer, int size);

};
#endif

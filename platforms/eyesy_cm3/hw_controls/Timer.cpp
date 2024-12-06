#include "Timer.h"
#include <stdio.h>

Timer::Timer() {
    gettimeofday(&start, NULL);
}

Timer::~Timer() {

}

void Timer::reset(void) {
    gettimeofday(&start, NULL);
}


// time in ms
float Timer::getElapsed(void) {  
    gettimeofday(&stop, NULL);
    long elapsed_sec = stop.tv_sec - start.tv_sec;
    long elapsed_usec = stop.tv_usec - start.tv_usec;
    float e = (float)elapsed_sec + (float)elapsed_usec / 1000000.f;
    return e * 1000.f;
}

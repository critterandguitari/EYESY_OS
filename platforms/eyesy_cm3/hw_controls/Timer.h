#ifndef TIMER_H
#define TIMER_H

#include <sys/time.h>

/*

Timer 

(c) 2016 Owen Osborn, Critter & Guitari

*/

class Timer
{
 public:
  
  Timer ();

  // destructor
  ~Timer();

   void reset(void);

   float getElapsed(void); 
    
   struct timeval start, stop;

};


#endif

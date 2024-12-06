#ifndef CM3GPIO_H
#define CM3GPIO_H

#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <wiringShift.h>
#include <stdio.h>  
#include <stdlib.h>  
#include <stdint.h>
#include <string.h>
#include <time.h>
#include "../OSC/OSCMessage.h"
#include "../OSC/SimpleWriter.h"

class CM3GPIO
{
    public:
        CM3GPIO();
        void init();
        void poll();
        void pollKnobs();
        //void updateOLED(OledScreen &s);
        void ping();
        void shutdown();
        void setLED(unsigned c);
        void clearFlags();

        uint32_t encBut;
        uint32_t encButFlag;
        uint32_t encTurn;
        uint32_t encTurnFlag;
        uint32_t knobFlag;
        uint32_t adcs[8];
        uint32_t footswitch;
        uint32_t footswitchFlag;
        uint32_t keyStates;
        uint32_t keyStatesLast;
        uint32_t keyFlag;
        
        // organelle m specific stuff
        uint32_t pwrStatus;
        uint32_t micSelSwitch;
	    float batteryVoltage;
	    uint32_t batteryBars;
        bool lowBatteryShutdown;

    private:        
        uint32_t shiftRegRead();
        void getEncoder();
        void getKeys();
        uint32_t adcRead(uint8_t adcnum);
        void displayPinValues();
	void checkFootSwitch ();
        
        uint32_t pinValues;
        uint32_t pinValuesLast;
};


#endif

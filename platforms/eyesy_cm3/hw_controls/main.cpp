#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <sys/stat.h>

#include "OSC/OSCMessage.h"
#include "OSC/SimpleWriter.h"
#include "UdpSocket.h"
#include "Timer.h"

#include "hw_interfaces/CM3GPIO.h"

#define OSC_IN_PORT 4001
#define OSC_OUT_PORT 4000

// knob stuff
void knobsInput(void);
void sendKnobs(void);
void keysInput(void);
static const unsigned int MAX_KNOBS = 6;
static int16_t knobs_[MAX_KNOBS];
static const int8_t EXPR_KNOB = 5;

// OSC callbacks
void setLED(OSCMessage &msg);
void flashLED(OSCMessage &msg);

// buffer for sending OSC messages 
SimpleWriter oscBuf;

// hardware interface controls
CM3GPIO controls;

// socket for OSC com
UdpSocket udpSock(OSC_IN_PORT);

// exit flag
int quit = 0;

int main(int argc, char* argv[]) {
    printf("build date " __DATE__ "   " __TIME__ "/n");
    uint32_t seconds = 0;
    char udpPacketIn[2048];
    int i = 0;
    int len = 0;
    int page = 0;

    Timer knobPollTimer, pingTimer, upTime;

    knobPollTimer.reset();
    pingTimer.reset();
    upTime.reset();

    udpSock.setDestination(OSC_OUT_PORT, "localhost");
    OSCMessage msgIn;

    controls.init();

    quit = 0;

    for (;;) {
        // receive udp osc messages
        len = udpSock.readBuffer(udpPacketIn, 2048, 0);
        if (len > 0) {
            msgIn.empty();
            for (i = 0; i < len; i++) {
                msgIn.fill(udpPacketIn[i]);
            }
            if (!msgIn.hasError()) {
                //char buf[128];
                //msgIn.getAddress(buf,0,128);
                //printf("osc message received %s %i\n",buf,msgIn.size());
                // or'ing will do lazy eval, i.e. as soon as one succeeds it will stop
                bool processed =
                    msgIn.dispatch("/led", setLED, 0)
                    || msgIn.dispatch("/led/flash", flashLED, 0)
                    ;
                if (!processed) {
                    char buf[128];
                    msgIn.getAddress(buf,0,128);
                    fprintf(stderr, "unrecognised osc message received %s %i\n",buf,msgIn.size());
                }
            }
            else {
                fprintf(stderr, "osc message has error \n ");
            }
            msgIn.empty();
        }

        // check for events from hardware controls
        controls.poll();

        // handle events
        if (controls.knobFlag) knobsInput();
        if (controls.keyFlag) keysInput();

        // clear the flags for next time
        controls.clearFlags();     

        // every 1 second do slow periodic tasks
        if (pingTimer.getElapsed() > 1000.f) {
            // printf("pinged the MCU at %f ms.\n", upTime.getElapsed());
            // send a ping in case MCU resets
            pingTimer.reset();
            controls.ping();
            sendKnobs();
        }

        // poll knobs every 40 ms
        if (knobPollTimer.getElapsed() > 20.f) {
            knobPollTimer.reset();
            controls.pollKnobs();
        }

        // check exit flag
        if (quit) {
            printf("quitting\n");
            return 0;
        }

        // main polling loop delay
        // slow it down for cm3 cause all the bit banging starts to eat CPU
        usleep(2000);
    } // for;;
}

/** OSC messages received internally (from PD or other program) **/

void setLED(OSCMessage &msg) {
    if (msg.isInt(0)) {
//        app.ledColor = msg.getInt(0);
        controls.setLED(msg.getInt(0));
    }
}

void flashLED(OSCMessage &msg) {
//    if (msg.isInt(0)){
//        app.ledFlashCounter = msg.getInt(0);
//        controls.setLED(7);
//    }
}


void knobsInput() {
    bool changed = false;
    // knob 1-4 + volume + expr , all 0-1023
    for(unsigned i = 0; i < MAX_KNOBS;i++) {
        int v = controls.adcs[i];

        if(v==0 || v==1023) {
            // allow extremes
            changed |= v != knobs_[i];
            knobs_[i] = v;
        } else {
            // 75% new value, 25% old value
            int16_t nv = (v >> 1) + (v >> 2) + (knobs_[i] >> 2);
            int diff = nv - knobs_[i];
            if(diff>2 || diff <-2) {
                changed = true;
                knobs_[i] = nv;
            }
        }
    }
    if(changed) {
        OSCMessage msgOut("/knobs");
        for(unsigned i = 0; i < MAX_KNOBS;i++) {
            msgOut.add(knobs_[i]);
        }
        msgOut.send(oscBuf);
        udpSock.writeBuffer(oscBuf.buffer, oscBuf.length);        
    }
}

void sendKnobs() {
    OSCMessage msgOut("/knobs");
    for(unsigned i = 0; i < MAX_KNOBS;i++) {
        msgOut.add(knobs_[i]);
    }
    msgOut.send(oscBuf);
    udpSock.writeBuffer(oscBuf.buffer, oscBuf.length);        
}

void keysInput(void) {
    uint8_t kmap[10] = {1,7,5,8, 4,9,6,10, 3,2};
    for (int i = 0; i < 10; i++){
        if(((controls.keyStates >> i) & 1) != ((controls.keyStatesLast >> i) & 1)){
            OSCMessage msgOut("/key");
            msgOut.add(kmap[i%10]);
            msgOut.add(((controls.keyStates >> i) & 1) * 100);
            msgOut.send(oscBuf);
            udpSock.writeBuffer(oscBuf.buffer, oscBuf.length);        
        }
    }
    controls.keyStatesLast = controls.keyStates;
}

/* helpers */

/* end helpers */



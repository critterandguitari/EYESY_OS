# EYESY_OS

The operating system for the EYESY video synthesizer device.

The system contains three main components: 

* engines, generally a video engine takes audio, midi, and control messages as input and outputs video
* pd, a Pd patch for controlling the video engine 
* web, a web based editor and file manager

Multiple video engines are supported as long as they respond to the messages sent by the controller. The controller is a Pd patch that reads the hardware knobs and buttons, handles MIDI and LINK connections and fowards all this to the video engine as Open Sound Control messages.

Other random commands are in the system folder and platform specific files and services are in the platforms folder. Eventually other platforms may be supported, but currently it is all designed to run on the Raspberry Pi based EYESY hardware.  

/*
 * Copyright (c) 2020 Owen Osborn, Critter & Gutiari, Inc.
 *
 * BSD Simplified License.
 * For information on usage and redistribution, and for a DISCLAIMER OF ALL
 * WARRANTIES, see the file, "LICENSE.txt," in this distribution.
 *
 */
#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup() {
    
    // listen on the given port
    cout << "listening for osc messages on port " << PORT << "\n";
    receiver.setup(PORT);    
    
    ofSetVerticalSync(true);
    ofSetFrameRate(60);
    ofSetLogLevel("ofxLua", OF_LOG_VERBOSE);

    ofHideCursor();

    ofSetBackgroundColor(0,0,0);
        
    // setup audio
    soundStream.printDeviceList();
    
    int bufferSize = 256;

    left.assign(bufferSize, 0.0);
    right.assign(bufferSize, 0.0);
    
    bufferCounter    = 0;

    ofSoundStreamSettings settings;
    
    // device by name
    auto devices = soundStream.getMatchingDevices("default");
    if(!devices.empty()){
        settings.setInDevice(devices[0]);
    }

    settings.setInListener(this);
    settings.sampleRate = 11025;
    settings.numOutputChannels = 0;
    settings.numInputChannels = 2;
    settings.bufferSize = bufferSize;
    soundStream.setup(settings);    

    //some path, may be absolute or relative to bin/data
    string path = "/sdcard/Modes/oFLua"; 
    ofDirectory dir(path);
    dir.listDir();

    //go through and print out all the paths
    for(int i = 0; i < dir.size(); i++){
        ofLogNotice(dir.getPath(i) + "/main.lua");
        scripts.push_back(dir.getPath(i) + "/main.lua");
    }
        
    // scripts to run
    currentScript = 0;
    
    // init the lua state
    lua.init(true); // true because we want to stop on an error
    
    // listen to error events
    lua.addListener(this);
    
    // run a script
    // true = change working directory to the script's parent dir
    // so lua will find scripts with relative paths via require
    // note: changing dir does *not* affect the OF data path
    lua.doScript(scripts[currentScript], true);
    
    // call the script's setup() function
    lua.scriptSetup();

	// clear main screen
	ofClear(0,0,0);
}

//--------------------------------------------------------------
void ofApp::update() {

    // check for waiting messages
    while(receiver.hasWaitingMessages()){
        // get the next message
        ofxOscMessage m;
        receiver.getNextMessage(m);
        //cout << "new message on port " << PORT << m.getAddress() << "\n";
        if(m.getAddress() == "/key") {   
            if (m.getArgAsInt32(0) == 4 && m.getArgAsInt32(1) > 0) {
                cout << "back" << "\n";
                prevScript();
            }
            if (m.getArgAsInt32(0) == 5 && m.getArgAsInt32(1) > 0) {
                cout << "fwd" << "\n";
                nextScript();
            }
            if (m.getArgAsInt32(0) == 9 && m.getArgAsInt32(1) > 0) {
                img.grabScreen(0,0,ofGetWidth(),ofGetHeight());
                string fileName = "snapshot_"+ofToString(10000+snapCounter)+".png";
                cout << "saving " + fileName + "...";
                img.save("/sdcard/Grabs/" + fileName);
                cout << "saved\n";
                snapCounter++;
            }
            if (m.getArgAsInt32(0) == 10 && m.getArgAsInt32(1) > 0) {
                cout << "trig" << "\n";
                lua.setBool("trig", true);
            }
			if (m.getArgAsInt32(0) == 3 && m.getArgAsInt32(1) > 0) {
            	cout << "change persist" << "\n";
            } 
        }
        if(m.getAddress() == "/knobs") {
            lua.setNumber("knob1", (float)m.getArgAsInt32(0) / 1023);
            lua.setNumber("knob2", (float)m.getArgAsInt32(1) / 1023);
            lua.setNumber("knob3", (float)m.getArgAsInt32(2) / 1023);
            lua.setNumber("knob4", (float)m.getArgAsInt32(3) / 1023);
            lua.setNumber("knob5", (float)m.getArgAsInt32(4) / 1023);
        }
        if(m.getAddress() == "/reload") {
            cout << "reloading\n";
            reloadScript();
        }
    }
    
    // call the script's update() function
    lua.scriptUpdate();

}

//--------------------------------------------------------------
void ofApp::draw() {
    
    lua.setNumberVector("inL", left);
    lua.setNumberVector("inR", right);
   
    lua.scriptDraw();
 
    //ofDrawBitmapString(scripts[currentScript], 10, ofGetHeight()-10);
    
    // clear flags    
    lua.setBool("trig", false);
}

//--------------------------------------------------------------
void ofApp::audioIn(ofSoundBuffer & input){
    
    for (size_t i = 0; i < input.getNumFrames(); i++){
        left[i]        = input[i*2]*0.5;
        right[i]    = input[i*2+1]*0.5;
    }
    
    bufferCounter++;
    
}

//--------------------------------------------------------------
void ofApp::exit() {
    // call the script's exit() function
    lua.scriptExit();
    
    // clear the lua state
    lua.clear();
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key) {
    
    switch(key) {
    
        case 'r':
            reloadScript();
            break;
    
        case OF_KEY_LEFT:
            prevScript();
            break;
            
        case OF_KEY_RIGHT:
            nextScript();
            break;
            
        case ' ':
            lua.doString("print(\"this is a lua string saying you hit the space bar!\")");
            cout << "fps: " << ofGetFrameRate() << "\n";    
            break;
    }
    
    lua.scriptKeyPressed(key);
}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y) {
    lua.scriptMouseMoved(x, y);
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button) {
    lua.scriptMouseDragged(x, y, button);
}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button) {
    lua.scriptMousePressed(x, y, button);
}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button) {
    lua.scriptMouseReleased(x, y, button);
}

//--------------------------------------------------------------
void ofApp::errorReceived(std::string& msg) {
    ofLogNotice() << "got a script error: " << msg;
}

//--------------------------------------------------------------
void ofApp::reloadScript() {
    // exit, reinit the lua state, and reload the current script
    lua.scriptExit();
    
    // init OF
    ofSetupScreen();
    ofSetupGraphicDefaults();
    ofSetBackgroundColor(0,0,0);

    // load new
    lua.init();
    lua.doScript(scripts[currentScript], true);
    lua.scriptSetup();
}

void ofApp::nextScript() {
    currentScript++;
    if(currentScript > scripts.size()-1) {
        currentScript = 0;
    }
    reloadScript();
}

void ofApp::prevScript() {
    if(currentScript == 0) {
        currentScript = scripts.size()-1;
    }
    else {
        currentScript--;
    }
    reloadScript();
}

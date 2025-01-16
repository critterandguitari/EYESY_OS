import sys
import liblo

etc = None 
osc_server = None
osc_target = None

# OSC callbacks
def fallback(path, args):
    pass

def set_callback(path, args):
    global etc
    name = args[0]
    etc.set_mode_by_name(name)
    print("set patch to: " + str(etc.mode) + " with index " + str(etc.mode_index))
 
def new_callback(path, args):
    global etc
    name = args[0]
    etc.load_new_mode(name)
   
def reload_callback(path, args):
    global etc
    print("reloading: " + str(etc.mode))
    etc.reload_mode()

def knobs_callback(path, args):
    global etc
    k1, k2, k3, k4, k5, k6 = args
    #print ("received message: " + str(args))
    etc.knob_hardware[0] = float(k1) / 1023
    etc.knob_hardware[1] = float(k2) / 1023
    etc.knob_hardware[2] = float(k3) / 1023
    etc.knob_hardware[3] = float(k4) / 1023
    etc.knob_hardware[4] = float(k5) / 1023

def keys_callback(path, args) :
    global etc
    k, v = args
    etc.dispatch_key_event(k,v)

def init (etc_object) :
    global osc_server, osc_target, etc
    etc = etc_object
    
    # OSC init server and client
    try:
        osc_target = liblo.Address(4001)
    except liblo.AddressError as err:
        print(err)

    try:
        osc_server = liblo.Server(4000)
    except liblo.ServerError as err:
        print(str(err))
    osc_server.add_method("/knobs", 'iiiiii', knobs_callback)
    osc_server.add_method("/key", 'ii', keys_callback)
    osc_server.add_method("/reload", 'i', reload_callback)
    osc_server.add_method("/set", 's', set_callback)
    osc_server.add_method("/new", 's', new_callback)
    osc_server.add_method(None, None, fallback)

def recv() :
    global osc_server
    while (osc_server.recv(1)):
        pass

def send(addr, args) :
    global osc_target
    liblo.send(osc_target, addr, args)

def close():
    global osc_server
    if osc_server:
        osc_server.free()  # Free the resources used by the OSC server
        osc_server = None
        print("OSC server closed successfully.")


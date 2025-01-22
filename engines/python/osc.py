import sys
import liblo

eyesy = None 
osc_server = None
osc_target = None

# OSC callbacks
def fallback(path, args):
    pass

def set_callback(path, args):
    global eyesy
    name = args[0]
    eyesy.set_mode_by_name(name)
    print("set patch to: " + str(eyesy.mode) + " with index " + str(eyesy.mode_index))
 
def new_callback(path, args):
    global eyesy
    name = args[0]
    eyesy.load_new_mode(name)
   
def reload_callback(path, args):
    global eyesy
    print("reloading: " + str(eyesy.mode))
    eyesy.reload_mode()

def knobs_callback(path, args):
    global eyesy
    #print ("received message: " + str(args[0]))
    for i,v in enumerate(eyesy.knob_last):
        if args[i] != eyesy.knob_last[i]:
            eyesy.knob_last[i] = args[i]
            eyesy.knob_hardware[i] = float(args[i] / 1023)
            #print(f"knob {i} {eyesy.knob_hardware[i]}")

def keys_callback(path, args) :
    global eyesy
    k, v = args
    eyesy.dispatch_key_event(k,v)

def init (eyesy_object) :
    global osc_server, osc_target, eyesy
    eyesy = eyesy_object
    
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


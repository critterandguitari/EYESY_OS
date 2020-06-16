import subprocess

def run_cmd(cmd) :
    ret = False
    try:
        ret = subprocess.check_output(['bash', '-c', cmd], close_fds=True)
    except: 
        pass
    return ret

# get midi devices ignoring the Midi Through device
devices = run_cmd("aplaymidi -l")
midiDevices = [ x for x in devices.split("\n") if not len(x)==0 and x != ' 14:0    Midi Through                     Midi Through Port-0']

# connect first one found
if len(midiDevices)>1 : 
    midiDevices.pop(0)
    midiDevice = (midiDevices[0][9:42].strip() + ":" + midiDevices[0][4:8].strip())
    print "found device: " + midiDevice
    run_cmd('aconnect "'+midiDevice+'" "Pure Data:0"')

else:
    print ""


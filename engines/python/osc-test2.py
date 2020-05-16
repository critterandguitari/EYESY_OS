from liblo import *
import sys
import time

class MyServer(ServerThread):
    osc_msgs_recv = 0
    def __init__(self):
        ServerThread.__init__(self, 4000)
    
    @make_method('/foo', 'ifs')
    def foo_callback(self, path, args):
        i, f, s = args
        self.osc_msgs_recv += 1
        #print "received message '%s' with arguments: %d, %f, %s" % (path, i, f, s)

    @make_method(None, None)
    def fallback(self, path, args):
        self.osc_msgs_recv += 1
        #print "received unknown message '%s'" % path

try:
    server = MyServer()
except ServerError, err:
    print str(err)
    sys.exit()

server.start()

last_time = time.time()
this_time = 0


while True :
    this_time = time.time()
    elapsed_time = this_time - last_time
    last_time = this_time
    osc_msgs_recv = server.osc_msgs_recv
    osc_msgs_per_sec = osc_msgs_recv / elapsed_time
    txt = str('osc: ' + str(osc_msgs_recv) + ', osc / sec: ' + str(osc_msgs_per_sec) + ', elp: ' + str(elapsed_time) )
    print txt
    server.osc_msgs_recv = 0
    time.sleep(1)


raw_input("press enter to quit...\n")

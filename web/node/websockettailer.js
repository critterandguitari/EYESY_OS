



// Node.js WebSocket server script
const http = require('http');
const WebSocketServer = require('websocket').server;
const server = http.createServer();
server.listen(9898);
const wsServer = new WebSocketServer({
	httpServer: server
});

Tail = require('tail').Tail;
tail = new Tail("/tmp/video.log");

wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
	connection.on('message', function(message) {
	console.log('Received Message:', message.utf8Data);
	connection.sendUTF('connected to websocket server');
	
//    const interval = setInterval(function ping() {
//	    console.log('sending to browser');
//	    connection.sendUTF('Hi stuff from server');
//    }, 1000);
     
    tail.on("line", function(data) {
      //console.log(data);
	    connection.sendUTF(data);
    });

   
    });
	connection.on('close', function(reasonCode, description) {
		console.log('Client has disconnected.');
	});
});

wsServer.on('connection', function(ws) {
    console.log('connection !');

    connection.sendUTF('Hi SERVER here');

    //ws.timer=setInterval(function(){pingpong(ws);},1000);

});

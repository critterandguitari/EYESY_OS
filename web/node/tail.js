Tail = require('tail').Tail;

tail = new Tail("testtail.txt");

tail.on("line", function(data) {
  console.log(data);
});

tail.on("error", function(error) {
  console.log('ERROR: ', error);
});



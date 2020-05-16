#wget http://www.thepeacetreaty.org/ping/ping.php

killall node
cd nodething
node websockettailer.js &
cd ..
cherryd -i cpapp -c prod.conf 


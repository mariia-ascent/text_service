#!/bin/bash



# start JS proxy-server
node proxy.js&

# start Python server
python3 server.py


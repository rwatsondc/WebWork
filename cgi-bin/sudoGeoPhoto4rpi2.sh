#!/bin/bash
echo Content-type: text/plain
echo ""

echo "Daisy-chaining shell scripts..."

echo "Killing off existing process instances"
sudo ./killImagerLoop.sh

echo "Starting imager loop..."

sudo ./geoPhoto4rpi2.sh

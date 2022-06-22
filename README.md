arduino-cli compile --fqbn arduino:avr:micro boat-monitor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:micro boat-monitor
sudo screen /dev/ttyACM0 9600
ctrl + a, k, y
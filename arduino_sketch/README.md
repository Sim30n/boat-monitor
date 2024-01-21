arduino-cli compile --fqbn arduino:avr:micro arduino_sketch
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:micro arduino_sketch
sudo screen /dev/ttyACM0 9600
ctrl + a, k, y

# compile and create profile 
arduino-cli compile --fqbn arduino:avr:micro--dump-profile

# compile with profile file
arduino-cli compile --profile arduino_sketch

Serial interface:

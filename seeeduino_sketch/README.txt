# instll core for seeed_XIAO_m0
arduino-cli core install Seeeduino:samd --additional-urls https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json

# also required for raspberry pi 3
sudo apt install libfl2

# list all boards attached
arduino-cli board list

# compile
arduino-cli compile --fqbn Seeeduino:samd:seeed_XIAO_m0 seeeduino_sketch

# compile with profile
arduino-cli compile --profile seeeduino_sketch

arduino-cli upload -p /dev/ttyACM1 --fqbn Seeeduino:samd:seeed_XIAO_m0 seeeduino_sketch

sudo screen /dev/ttyACM1 9600

ctrl + a, k, y
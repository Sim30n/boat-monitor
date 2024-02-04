import subprocess

def find_usb_ports():
    run_command = subprocess.Popen("/home/pi/arduino-cli/bin/arduino-cli board list", shell=True, stdout=subprocess.PIPE).stdout.read()
    arduino_micro = None
    seeeduino_xiao = None
    for line in run_command.decode().splitlines():
        if "Arduino Micro" in line:
            arduino_micro = line[:12]
        elif "Seeeduino XIAO" in line:
            seeeduino_xiao = line[:12]
    return arduino_micro, seeeduino_xiao

arduino_usb=find_usb_ports()[0]
seeeduino_usb=find_usb_ports()[1]

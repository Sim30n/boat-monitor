*** Settings ***
Library   Process
Library   String

*** Variables ***
${seeeduino_sketch_path} =    ${boat_app_path}/seeeduino_sketch
${flash_path} =    ${boat_app_path}

# Run with command: robot --variable boat_app_path:/home/pi/projects/boat/boat-monitor --outputdir test_output build_arduino_tests.robot
*** Test Cases ***
Build Seeeduino Sketch
    ${result} =    Run Process    arduino-cli     compile    --profile
    ...    seeeduino_sketch    cwd=${seeeduino_sketch_path}
    Should Be Equal As Integers    ${result.rc}    0
    Should Be Empty    ${result.stderr}

Flash Seeeduino Board
    ${result} =    Run Process    arduino-cli    upload    -p     ${seeeduino_usb}
    ...    --fqbn    Seeeduino:samd:seeed_XIAO_m0    seeeduino_sketch    cwd=${flash_path}
    Should Be Equal As Integers    ${result.rc}    0
    Sleep    2

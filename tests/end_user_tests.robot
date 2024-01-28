*** Settings ***
Library   Process
Library   String

*** Variables ***
${python_bin} =    ${venv_bin}/python
${boat_app} =    ${boat_app_path}/boat_app/boat_app_lite.py


# Run with command: robot --variable boat_app_path:/home/pi/projects/boat/boat-monitor --outputdir test_output end_user_tests.robot
*** Test Cases ***
Get SW Version
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    get_sw_version
    ${board_init} =    Get Line    ${result.stdout}    0
    ${sw_version} =     Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Log To Console    ${sw_version}
    #Should Be True	${battery_voltage} >= 0

Get Battery Voltage
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    battery_voltage
    ${board_init} =    Get Line    ${result.stdout}    0
    ${battery_voltage} =     Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Should Be True	${battery_voltage} >= 0

Get Electric Load
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    get_electric_load
    ${board_init} =     Get Line    ${result.stdout}    0
    ${electric_load} =  Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Should Be True	${electric_load} > -5
    Should Be True	${electric_load} < 5

Get Water Temperature
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    get_water_temperature
    ${board_init} =     Get Line    ${result.stdout}    0
    ${water_temperature_value} =  Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Should Be True	${water_temperature_value} > -50
    Should Be True	${water_temperature_value} < 50

Get Inside Humidity
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    get_humidity_temperature
    ${board_init} =     Get Line    ${result.stdout}    0
    ${humidity_value} =  Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Should Be True	${humidity_value} > 20

Get Inside Temperature
    ${result} =    Run Process    ${python_bin}    ${boat_app}
    ...    --get_value    get_inside_temperature
    ${board_init} =     Get Line    ${result.stdout}    0
    ${water_temperature_value} =  Get Line    ${result.stdout}    -1
    Should Be Equal    ${board_init}    Arduino initialized.
    Should Be True    ${water_temperature_value} > -50
    Should Be True    ${water_temperature_value} < 50

Start Main App
    ${result} =    Start Process    ${python_bin}    ${boat_app}
    ...    --main_app
    Sleep    5
    Process Should Be Running    ${result}
    Terminate All Processes

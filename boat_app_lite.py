import serial
import time
import os
import datetime
from dotenv import load_dotenv
import logging
import sys
import telegram_send

# load env variables
load_dotenv()

class ArduinoBoard:
    ser = serial.Serial(os.environ["SERIAL"], 9600)
    time.sleep(2)
    print("Arduino initialized.")

    def __init__(self):
        self.time_stamp = None
        self.electric_load = None
        self.battery_voltage = None
        self.water_temperature = None
        self.inside_temperature = None
        self.humidity_temperature = None
        self.bilge_water_level = None

    def get_data(self):
        """"
        This method will ask the latest sensor values from arduino board.
        """
        self.ser.write(str.encode("get_data"))
        time.sleep(2)
        result = self.ser.readline().decode("utf-8")
        #import pdb; pdb.set_trace()
        strip_result = result.strip()
        split_result = strip_result.split(";")
        self.time_stamp = datetime.datetime.now()
        self.electric_load = split_result[0]
        self.battery_voltage = split_result[1]
        self.water_temperature = split_result[2]
        self.inside_temperature = split_result[3]
        self.humidity_temperature = split_result[4]
        self.bilge_water_level = split_result[5]
        print(split_result)
        return split_result

    def close_serial(self):
        """
        Close the serial connection when no longer needed.
        """
        self.ser.close()

class SeeeduinoBoard:
    def __init__(self) -> None:
        self.ser = serial.Serial(os.environ["SEEED_SERIAL"], 9600)
        time.sleep(2)
        print("Seeeduino initialized.")

    def read_serial(self):
        voltage = float(self.ser.readline().decode("utf-8").strip())
        return voltage

    def close_serial(self):
        """
        Close the serial connection when no longer needed.
        """
        self.ser.close()

if __name__ == "__main__":
    logging.basicConfig(filename="app.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    boat = ArduinoBoard()
    seeed_board = SeeeduinoBoard()
    bilge_pump_timeout = 120 # measure this
    send_interval = datetime.datetime.now() + datetime.timedelta(0,0,0,0,10)
    duration_seconds = 0
    print(f"Log loop started: {datetime.datetime.now()}")
    while True:
        try:
            time_now = datetime.datetime.now()
            bilge_pump_voltage = seeed_board.read_serial()
            if bilge_pump_voltage > 10:
                bilge_pump_start_time = datetime.datetime.now()
                print(f"Bilge pump started: {bilge_pump_start_time}")
                while seeed_board.read_serial() > 10:
                    duration = datetime.datetime.now() - bilge_pump_start_time
                    duration_seconds = duration.total_seconds()
                    if bilge_pump_timeout <= duration_seconds:
                        bilge_timeout = f"*BILGE PUMP OPERATED OVER {bilge_pump_timeout}s*"
                        print(bilge_timeout)
                        telegram_send.send(messages=[bilge_timeout], parse_mode="markdown")
                        break
                    print(duration_seconds)
                boat_data = boat.get_data()
                data = {
                    u'time_stamp': boat.time_stamp,
                    u'electric_load': boat.electric_load,
                    u'battery_voltage': boat.battery_voltage,
                    u'water_temperature': boat.water_temperature,
                    u'inside_temperature': boat.inside_temperature,
                    u'humidity_temperature': boat.humidity_temperature,
                    u'bilge_water_level': boat.bilge_water_level,
                    u'bilge_pump_run_time': duration_seconds
                }
                logging.info(f"{time_now}: {data}")
                bilge_message = f"Bilge pump operated {bilge_pump_timeout}s"
                telegram_send.send(messages=[bilge_message], parse_mode="markdown")
            if time_now > send_interval:
                boat_data = boat.get_data()
                data = {
                    u'time_stamp': boat.time_stamp,
                    u'electric_load': boat.electric_load,
                    u'battery_voltage': boat.battery_voltage,
                    u'water_temperature': boat.water_temperature,
                    u'inside_temperature': boat.inside_temperature,
                    u'humidity_temperature': boat.humidity_temperature,
                    u'bilge_water_level': boat.bilge_water_level,
                    u'bilge_pump_run_time': duration_seconds
                }
                logging.info(f"{time_now}: {data}")
                send_interval = send_interval + datetime.timedelta(0,0,0,0,10)
        except KeyboardInterrupt:
            seeed_board.close_serial()
            boat.close_serial()
            print("Closing serial")
            sys.exit(1)

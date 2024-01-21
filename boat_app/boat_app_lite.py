import serial
import time
import os
import datetime
from dotenv import load_dotenv
import logging
import sys
import telegram_send
import argparse

# load env variables
load_dotenv()


class ArduinoBoard:
    def __init__(self):
        self.ser = serial.Serial(os.environ["SERIAL"], 9600)
        time.sleep(2)
        print("Arduino initialized.")

        self.data = {
            "time_stamp":           None,
            "electric_load":        None,
            "battery_voltage":      None,
            "water_temperature":    None,
            "inside_temperature":   None,
            "humidity_temperature": None,
            "bilge_water_level":    None,
            "bilge_pump_run_time":  None,
            }

    def get_data(self, node: str = "all"):
        """"
        This method will ask the latest sensor values from arduino board.
        """
        if node == "all":
            self.ser.write(str.encode("get_data"))
            time.sleep(2)
            result = self.ser.readline().decode("utf-8")
            #import pdb; pdb.set_trace()
            strip_result = result.strip()
            split_result = strip_result.split(";")
            self.data["time_stamp"] = datetime.datetime.now()
            self.data["electric_load"] = split_result[0]
            self.data["battery_voltage"] = split_result[1]
            self.data["water_temperature"] = split_result[2]
            self.data["inside_temperature"] = split_result[3]
            self.data["humidity_temperature"] = split_result[4]
            self.data["bilge_water_level"] = split_result[5]
            print(split_result)
            return split_result
        else:
            self.ser.write(str.encode(node))
            time.sleep(0.5)
            result = self.ser.readline().decode("utf-8")
            strip_result = result.strip()
            print(strip_result)
            return strip_result

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


def main_app():
    logging.basicConfig(filename=f"{os.environ['LOG_FILE']}", filemode="a", format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    boat = ArduinoBoard()
    seeed_board = SeeeduinoBoard()
    bilge_pump_timeout = 120  # measure this
    send_interval = datetime.datetime.now() + datetime.timedelta(0,0,0,0,10)
    duration_seconds = 0
    print(f"Log loop started: {datetime.datetime.now()}")
    telegram_send.send(messages=["Boat monintor app started"], parse_mode="markdown")
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
                boat.data["bilge_pump_run_time"] = duration_seconds
                logging.info(f"{time_now}: {boat.data}")
                bilge_message = f"Bilge pump operated {duration_seconds}s"
                telegram_send.send(messages=[bilge_message], parse_mode="markdown")
            if time_now > send_interval:
                boat_data = boat.get_data()
                boat.data["bilge_pump_run_time"] = 0
                logging.info(f"{time_now}: {boat.data}")
                send_interval = send_interval + datetime.timedelta(0,0,0,0,10)
        except KeyboardInterrupt:
            seeed_board.close_serial()
            boat.close_serial()
            print("Closing serial")
            sys.exit(1)
        if os.environ["STOP_SIGNAL"] == "1":
            seeed_board.close_serial()
            boat.close_serial()
            print("Closing serial")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--read_values", help="Read values from Arduino board.",
                    action="store_true")
    parser.add_argument("-m", "--main_app", help="Start main application.",
                    action="store_true")
    parser.add_argument("-g", "--get_value", help="Read individual node value.", type=str)
    args = parser.parse_args()

    if args.read_values:
        boat = ArduinoBoard()
        boat.get_data()
        boat.close_serial()

    if args.main_app:
        main_app()

    if args.get_value:
        boat = ArduinoBoard()
        boat.get_data(args.get_value)
        boat.close_serial()


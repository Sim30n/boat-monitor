import serial
import time
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import logging

# load env variables
load_dotenv()

class ArduinoBoard:
    ser = serial.Serial(os.environ["SERIAL"], 9600)
    time.sleep(2)

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
        self.time_stamp = datetime.now()
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

if __name__ == "__main__":

    # firebase stuff
    cred = credentials.Certificate(os.environ["FIREBASE"])
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    logging.basicConfig(filename="app.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)

    boat = ArduinoBoard()
    boat_data = boat.get_data()
    boat.close_serial()
    data = {
        u'time_stamp': boat.time_stamp,
        u'electric_load': boat.electric_load,
        u'battery_voltage': boat.battery_voltage,
        u'water_temperature': boat.water_temperature,
        u'inside_temperature': boat.inside_temperature,
        u'humidity_temperature': boat.humidity_temperature,
        u'bilge_water_level': boat.bilge_water_level
    }
    logging.info(f"{boat_data}")

    doc_ref = db.collection(u"boat_data").document()
    doc_ref.set(data)



   
        
    

    
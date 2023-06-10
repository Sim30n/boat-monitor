import datetime
import sys
import os
import pandas as pd
import telegram_send
from dotenv import load_dotenv

# load env variables
load_dotenv()


def read_log_file():
    log_file = os.environ["LOG_FILE"]
    file1 = open(log_file, "r")
    count = 0
    lines = []
    while True:
        count += 1
        line = file1.readline()
        if not line:
            break
        lines.append(line.strip("\n"))
    file1.close()
    return lines


# --------- Convert to dict -------------
lines = read_log_file()
log_items = []
for line in lines:
    dictitem = line.split("{")
    dict_string = "{"+f"{dictitem[1]}"
    to_dict = eval(dict_string)
    log_items.append(to_dict)

# --------------- pandas stuff ------------------------
df = pd.DataFrame(log_items)
df["electric_load"] = pd.to_numeric(df["electric_load"], downcast="float")
df["battery_voltage"] = pd.to_numeric(df["battery_voltage"], downcast="float")
df["water_temperature"] = pd.to_numeric(df["water_temperature"], downcast="float")
df["inside_temperature"] = pd.to_numeric(df["inside_temperature"], downcast="float")
df["humidity_temperature"] = pd.to_numeric(df["humidity_temperature"], downcast="float")
df["bilge_pump_run_time"] = pd.to_numeric(df["bilge_pump_run_time"], downcast="float")


# Set the 'date' column as the index
df.set_index("time_stamp", inplace=True)
# Define your desired date range
current_datetime = pd.to_datetime(pd.Timestamp.now())
start_date = current_datetime - pd.Timedelta(days=1)
rows_between_dates = df.loc[start_date:current_datetime]

average_battery_voltage = rows_between_dates["battery_voltage"].mean()
average_electric_load = rows_between_dates["electric_load"].mean()
average_water_temperature = rows_between_dates["water_temperature"].mean()
average_inside_temperature = rows_between_dates["inside_temperature"].mean()
average_humidity_temperature = rows_between_dates["humidity_temperature"].mean()
average_bilge_pump_run_time = rows_between_dates["bilge_pump_run_time"].mean()
send_info = f"""*Past 24h averages*
Battery voltage: {average_battery_voltage}
Electric load: {average_electric_load}
Water temperature: {average_water_temperature}
Inside temperature: {average_inside_temperature}
Inside humidity: {average_humidity_temperature}
Average bilge pump run time: {average_bilge_pump_run_time}"""
print(send_info)
telegram_send.send(messages=[send_info], parse_mode="markdown")


# ---- print all -------------
#for log_item in log_items:
#    try:
#        print(log_item[sys.argv[1]])
#    except KeyError:
#        print("Give valid log item.")
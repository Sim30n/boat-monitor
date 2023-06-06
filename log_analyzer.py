import datetime


def read_log_file():
    file1 = open("app.log", "r")
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

for log_item in log_items:
    print(log_item["battery_voltage"])

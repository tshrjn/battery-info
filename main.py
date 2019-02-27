import subprocess, re

def battery_info():
    ioreg = subprocess.check_output(
            ['ioreg', '-r', '-w0', '-cAppleSmartBattery']
        ).decode("utf-8").split("\n")
    d = dict()
    for line in ioreg:
        match = re.match(r'^ *"(.+)" = ("?)(.+)\2$', line)
        if match is None:
            continue
        (key, val) = (match.group(1), match.group(3))
        try:
            d[key] = int(val)
        except ValueError:
            if val == 'Yes':
                d[key] = True
            elif val == 'No':
                d[key] = False
            else:
                d[key] = val
    return d

keys = ['CurrentCapacity','DesignCapacity','IsCharging','MaxCapacity']
d = battery_info()
keys.append('Health')
d[keys[-1]] = str(round(d['MaxCapacity']/d['DesignCapacity']*100,2)) + '%'

for key in keys:
    print ("{}: {}".format(key, d[key]))
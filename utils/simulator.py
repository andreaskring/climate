import random
import requests
import time


INSTANCE = '50:02:91:C9:AF:83'
PUSHGW_URL = 'http://localhost:9091/metrics/job/climate/instance/' + INSTANCE


random.seed()

while True:
    temp = 20 + 3*random.random()
    rh = 40 + 3*random.random()

    r_temp = requests.post(PUSHGW_URL, 'temp %s\n' % temp)
    r_rh = requests.post(PUSHGW_URL, 'rh %s\n' % rh)
    print('HTTP status (temp = {}): {}'.format(temp, r_temp.status_code))
    print('HTTP status (rh = {})  : {}'.format(rh, r_rh.status_code))
    print(35*'-')

    time.sleep(1)

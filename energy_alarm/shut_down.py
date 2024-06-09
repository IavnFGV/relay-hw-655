#!/usr/bin/env python3
from cmd_actions import ping, shut_down
from datetime import datetime
import time
import os


PLUG_KITHEN_IP='192.168.0.152'
PLUG_COMPUTER_IP='192.168.0.151'

def check():
    ping1 =  ping(PLUG_KITHEN_IP)

    if(ping1):
        log('PLUG_IS_ONLINE')
        return
    if(not ping1):
        print('no answer from plug in Kitchen. Waiting 5 secs')
        time.sleep(5)
        ping2 =  ping(PLUG_KITHEN_IP)
        if(ping2):
            log('PLUG_IS_ONLINE')
            return
        elif (os.environ.get('ENERGY_ALARM_CHECK_ANOTHER_ONE','FALSE')== 'TRUE'):
            log('Still not online. Going to check another one')
            ping_another_one=ping(PLUG_COMPUTER_IP)
            if(ping_another_one):
                log('ANOTHER PLUG_IS_ONLINE')
                return
            else:
                log('BOTH_PLUGS_ARE_NOT_ACCESSIBLE')
                c = datetime.now()
                log('SHUTTING_DOWN')
                shut_down()
                return
        else:
            log('PLUG_IS_NOT_ACCESIBLE')
            log('SHUTTING_DOWN')
            shut_down()
            return


def log(message):
    c = datetime.now()
    print(f'{c}:{message}')


check()

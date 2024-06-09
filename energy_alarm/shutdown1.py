#!/usr/bin/env python3
import json

from cmd_actions import ping, shut_down
from datetime import datetime
import time

PLUG_KITHEN_IP = '192.168.0.152'
PLUG_COMPUTER_IP = '192.168.0.151'


def disable_for_next_start():
    with open('config.json', 'rw') as openfile:
        temp_config = json.load(openfile)
        temp_config['IS_ENABLED'] = False
        json.dump(temp_config, openfile)


def check(config):
    ping1 = ping(PLUG_KITHEN_IP)

    if (ping1):
        log('PLUG_IS_ONLINE')
        return
    if (not ping1):
        print('no answer from plug in Kitchen. Waiting 5 secs')
        time.sleep(5)
        ping2 = ping(PLUG_KITHEN_IP)
        if (ping2):
            log('PLUG_IS_ONLINE')
            return
        elif (config.get('CHECK_ANOTHER_ONE_PLUG', False)):
            log('Still not online. Going to check another one')
            ping_another_one = ping(PLUG_COMPUTER_IP)
            if (ping_another_one):
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
            disable_for_next_start()
            log('SHUTTING_DOWN')
            shut_down()
            return


def log(message):
    c = datetime.now()
    print(f'{c}:{message}')


with open('config.json', 'r') as openfile:
    config = json.load(openfile)


def enable_check_when_both_are_accessible():
    ping = ping(PLUG_KITHEN_IP)
    ping_another = ping(PLUG_COMPUTER_IP)
    if (ping and ping_another):
        with open('config.json', 'rw') as openfile:
            temp_config = json.load(openfile)
            temp_config['IS_ENABLED'] = True
            json.dump(temp_config, openfile)


if (config.get('IS_ENABLED', False)):
    log("IS_ENABLED is TRUE")
    check(config)
else:
    enable_check_when_both_are_accessible()


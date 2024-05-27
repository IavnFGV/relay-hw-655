# relay-hw-655


base instruction

https://www.da-share.com/misc/esp8266-relay-board-mod/

telegram,ping, rebuild 

https://www.juliogonzalez.es/watchdog-for-network-devices-with-tasmota-and-sonoff-s26/508

how to build locally

https://tasmota.github.io/docs/PlatformIO/#download-platformio

problem with tmsend

https://github.com/arendst/Tasmota/discussions/15499

workaround 
use tasmota 13.0.4 
SetOption132 1 in console  
or define  in user_config_override.h 

```
#ifdef MQTT_TLS_FINGERPRINT
#undef MQTT_TLS_FINGERPRINT
#endif
#define MQTT_TLS_FINGERPRINT   true
```

interesting 
https://github.com/arendst/Tasmota/issues/21464

webquery from console

```
20:50:04.548 CMD: webquery https://api.telegram.org/bot[mybottokenhere]/sendMessage?text=test&chat_id=[myprivatechatID]
20:50:04.551 SRC: WebConsole from 192.168.11.80
20:50:04.553 CMD: Grp 0, Cmd 'WEBQUERY', Idx 1, Len 113, Pld -99, Data 'https://api.telegram.org/bot[mybottokenhere]/sendMessage?text=test&chat_id=[myprivatechatID]'
20:50:04.665 RSL: RESULT = {"WebQuery":"Done"}
```

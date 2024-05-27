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

use tasmota 13.4.0 
in console  

```
SetOption132 1
```

or define  in user_config_override.h 

```
#ifdef MQTT_TLS_FINGERPRINT
#undef MQTT_TLS_FINGERPRINT
#endif
#define MQTT_TLS_FINGERPRINT   true
```

interesting 
https://github.com/arendst/Tasmota/issues/21464
https://github.com/arendst/Tasmota/issues/15505

webquery from console

```
20:50:04.548 CMD: webquery https://api.telegram.org/bot[mybottokenhere]/sendMessage?text=test&chat_id=[myprivatechatID]
20:50:04.551 SRC: WebConsole from 192.168.11.80
20:50:04.553 CMD: Grp 0, Cmd 'WEBQUERY', Idx 1, Len 113, Pld -99, Data 'https://api.telegram.org/bot[mybottokenhere]/sendMessage?text=test&chat_id=[myprivatechatID]'
20:50:04.665 RSL: RESULT = {"WebQuery":"Done"}
```

brssl 

https://github.com/arendst/Tasmota/discussions/15499


example of rule

```
Rule2
ON system#boot DO Var1 3 ENDON
ON system#boot DO Var2 0 ENDON
ON system#boot DO tmchatid 874778749 ENDON
ON system#boot DO tmstate 1 ENDON
ON system#boot DO tmtoken 7003711115:AAEvezz75tx4iSkqk3dG94ztSyz4c24oKbk ENDON
ON system#boot DO tmsend Router booted up ENDON
ON Var1#State>1439 DO Var1 1439 ENDON
ON Time#Minute|%var1% DO Ping4 192.168.0.1 ENDON
ON Ping#192.168.0.1#Success==0 DO backlog; tmsend Router: Device is unresponsive...; Add2 1 ENDON
ON Ping#192.168.0.1#Success>0 DO backlog; Var1 3; Var2 0 ENDON
ON Var2#State > 1 DO backlog Mult1 3; tmsend Router: Device is unresponsive, restarting power; Power1 0; Delay 10; Power1 1; Var2 0 ENDON
```

vital rule to activate controller on HW-655 board

````
Rule1
on System#Boot do Baudrate 9600 endon on Power1#State=1 do SerialSend5 A00101A2 endon on Power1#State=0 do SerialSend5 A00100A1 endon
````

something wromg with asus DHCP and esp-01 - workaround- bind address in DHCP and setup via tasmota console

```
ipaddress1 192.168.0.171
```

also logging level setup

```
weblog 4
weblog 2 <- default 
```


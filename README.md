# relay-hw-655


base instruction

https://www.da-share.com/misc/esp8266-relay-board-mod/

alternative firmware 

https://github.com/sololko/ESP-01-relay-HW-655/blob/master/relayonoff.ino

telegram,ping, rebuild 

https://www.juliogonzalez.es/watchdog-for-network-devices-with-tasmota-and-sonoff-s26/508

user_config_override.h content is in file of current repo


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

cron job on server 

```
sudo crontab -u root -e
```
inside of file  also see energy_alarm folder in current repository
```
* * * * * sudo /opt/energy_alarm/shutdown2.py >> /opt/energy_alarm/logs/out.log
```

Communication scheme is 
![image](https://github.com/IavnFGV/relay-hw-655/assets/11654266/1e16f586-1145-4afc-b218-1c5faa939cbc)


# Steps to init modules

1. compile tasmota 13.4.0 with ping and telegram - see user_config_override.h
2. in console of each module - run one by one
  ```
  Backlog SetOption132 1; Latitude 50.46493503945635; Longitude 30.410156250000004; TimeDST 0,0,3,1,1,180; TimeSTD 0,0,10,1,1,120; TimeZone 99
  ```
3. configure both device templates in web_ui to this
  ![image](https://github.com/IavnFGV/relay-hw-655/assets/11654266/d8d74963-2587-4fa8-8303-04802278b07a)
4. in console of PC-relay
  ```
    Rule1
  on System#Boot do Baudrate 9600 endon 
  on Power1#State=1 do SerialSend5 A00101A2 endon 
  on Power1#State=0 do SerialSend5 A00100A1 endon
  ```
  ```
    rule1 1
  ```
5. in console of UPS-relay
  ```
  Rule1
  ON system#boot DO backlog; Var1 0; var5 0 ENDON
  ON system#boot DO tmchatid 874778749 ENDON
  ON system#boot DO tmstate 1 ENDON
  ON system#boot DO tmtoken TOKEN_HERE ENDON
  on System#Boot do Baudrate 9600 endon 
  on Power1#State=1 do SerialSend5 A00101A2 endon 
  on Power1#State=0 do SerialSend5 A00100A1 endon
  ```
  ```
  Rule2
  ON Time#Minute|1 DO Ping 192.168.0.151 ENDON
  on Ping#192.168.0.151#reachable=true DO add5 1 endon
  on var5#state==10 do var5 2 endon
  on var5#state==1 do backlog; var1 1; power 1; RuleTimer1 60; add2 1 endon
  on Rules#timer=1 do Ping 192.168.0.171 endon
  on Ping#192.168.0.171#reachable=false do RuleTimer1 1 endon
  on Ping#192.168.0.171#reachable=true DO backlog; websend [192.168.0.171]Power ON ; RuleTimer2 60; var1 2; add2 1 ENDON
  on Rules#timer=2 do backlog; Ping 192.168.0.17  endon
  on Ping#192.168.0.17#reachable=false DO backlog; RuleTimer2 10 ENDON
  on Ping#192.168.0.17#reachable=true DO backlog; var1 3; add2 1  ENDON
  on var1#state=3 do backlog; var5 0; var2 %var3%; var1 0; rule2 0; rule3 1 ENDON

  on var2#state==11 do tmsend UPS: plug is OK. Electricity is here. Turning on. endon
  on var2#state==12 do tmsend UPS: PC relay is on. Turning on PC. endon
  on var2#state==13 do tmsend UPS: PC is ok. Moving to Wait Electricity outage. endon
  ```
  ```
  Rule3
  ON Time#Minute|1 DO Ping 192.168.0.151 ENDON
  on Ping#192.168.0.151#reachable=false DO add5 1 endon
  on var5#state==10 do var5 2 endon
  on var5#state==1 do backlog; var1 1; RuleTimer1 60; add2 1 endon
  
  on Rules#timer=1 do Ping 192.168.0.17 endon
  on Ping#192.168.0.17#reachable=true do RuleTimer1 5 endon
  on Ping#192.168.0.17#reachable=false DO backlog; RuleTimer2 60; var1 2; add2 1 ENDON
  on Rules#timer=2 do backlog; power 1; RuleTimer3 60 endon
  on Rules#timer=3 do backlog; Ping 192.168.0.171 endon
  on Ping#192.168.0.171#reachable=true DO backlog; RuleTimer3 60 ENDON
  on Ping#192.168.0.171#reachable=false DO backlog; var1 3; add2 1  ENDON
  on var1#state=3 do backlog; var5 0; var2 %var3%; var1 0; rule3 0; rule2 1 ENDON
  
  on var2#state==11 do tmsend UPS: plug is NOT RESPONSIBLE. There is no Electricity. Monitoring PC. endon
  on var2#state==12 do tmsend UPS: PC is not responsible. Waiting 60 secs to shutdown UPS. endon
  on var2#state==13 do tmsend UPS: PC relay is down. Moving to Wait Electricity. endon
  ```
6. to enble sending telegram notification  please run this
  ```
  var3 =10
  ```
7. to start ensure that PC-relay has rule 1 activated; UPS-relay has rule1 active; and rule2 active/ rule3 inactive and vice versa






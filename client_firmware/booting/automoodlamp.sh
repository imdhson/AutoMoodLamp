#!/bin/bash
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 cd client_firmware/ ;
 python booting/updateService.py
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 sudo python client_firmware/mp_firmware.py

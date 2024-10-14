#!/bin/bash
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 source .venv/bin/activate
 cd client_firmware/ ;
 python booting/updateService.py
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 sudo python client_firmware/mp_firmware.py

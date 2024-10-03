#!/bin/bash
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 source venv-automoodlamp/bin/activate
 python client_firmware/booting/updateService.py
 ./mp_firmware
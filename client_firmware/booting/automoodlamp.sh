#!/bin/bash
 cd /home/imdhson/servers/AutoMoodLamp/ ;
 source .venv/bin/activate
 python client_firmware/booting/updateService.py
 ./mp_firmware

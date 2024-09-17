#!/bin/bash
 cd /home/imdhson/git/automoodlamp/ ;
 source venv-automoodlamp/bin/activate
 python audio_client/booting/updateService.py
 ./mp_firmware
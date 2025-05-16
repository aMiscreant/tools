#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

try:
    import os
except ImportError as error:
    print("\n[-]Failed To Import Module\n'")
    print(error)
    os = None
    sys.exit(1)


def print_banner():
    os.system("clear")
    print('''

 _______        .__  .__    _________                          .__  __          
 \      \  __ __|  | |  |  /   _____/ ____   ____  __ _________|__|/  |_ ___.__.
 /   |   \|  |  \  | |  |  \_____  \_/ __ \_/ ___\|  |  \_  __ \  \   __<   |  |
/    |    \  |  /  |_|  |__/        \  ___/\  \___|  |  /|  | \/  ||  |  \___  |
\____|__  /____/|____/____/_______  /\___  >\___  >____/ |__|  |__||__|  / ____|
        \/                        \/     \/     \/                       \/     
                                                     
                             [nullsecurity team]
 **********************************************************************************
      U3-Pwn  [*] Metasploit Payload Injection Tool For SanDisk Devices    [*] 
              [*] ESP32/ESP8266 Payload Injection Tool for SanDisk Devices [*] 
                           S[Codename: SanSubrosa]S 
 **********************************************************************************
''')



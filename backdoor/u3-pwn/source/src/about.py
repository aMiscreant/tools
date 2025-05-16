#!/usr/bin/env python3
################################################################################
#                ____                     _ __                                 #
#     ___  __ __/ / /__ ___ ______ ______(_) /___ __                           #
#    / _ \/ // / / (_-</ -_) __/ // / __/ / __/ // /                           #
#   /_//_/\_,_/_/_/___/\__/\__/\_,_/_/ /_/\__/\_, /                            #
#                                            /___/ team                        #
#                                                                              #
# U3-Pwn                                                                       #
#                                                                              #
# DATE                                                                         #
# 10/05/2013                                                                   #
#                                                                              #
# DESCRIPTION                                                                  #
# U3-Pwn is a tool designed to automate injecting executables to Sandisk       #
# smart usb devices with default U3 software install. This is performed by     #
# removing the original iso file from the device and creating a new iso        #
# with autorun features.                                                       #
#                                                                              #
# REQUIREMENTS                                                                  #
# - Metasploit                                                                 #
# - U3-Tool                                                                    #
# - Python-2.7                                                                 #
#                                                                              #
# AUTHOR                                                                       #
# Zy0d0x - http://www.nullsecurity.net/                                        #
#                                                                              #
################################################################################
import os
import sys

try:
    import banner
except ImportError as error:
    print('\n[-] Failed to import module\n')
    print(error)
    banner = None  # define banner as None to avoid NameError later
    sys.exit(1)

define_path = os.getcwd()
sys.path.append(f'{define_path}/src/')
banner.print_banner()

print('''
 U3-Pwn is a tool designed to automate injecting executables to SanDisk 
 smart USB devices with the default U3 software install. This is performed by 
 removing the original ISO file from the device and creating a new ISO 
 with autorun features.

 Written by: Michael Johnson (Zy0d0x) @ https://www.nullsecurity.net

 Submit Bugs: zy0d0x at nullsecurity.net

 DISCLAIMER: This is only for testing purposes and can only be used where
 strict consent has been given. Do not use this for illegal purposes. Period.
''')

input(''' Press any key to return to menu: ''')


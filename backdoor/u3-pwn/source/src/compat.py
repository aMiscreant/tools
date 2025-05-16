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

print(' Compatibility List of SanDisk U3 Devices')

print('''

 VendorID  |  ProductID  |         Device Name
-----------|-------------|--------------------------------------
  0x0781   |   0x5406    |   SanDisk Cruzer Micro
  0x0781   |   0x5408    |   SanDisk Cruzer Titanium
  0x0781   |   0x550a    |   SanDisk Cruzer Pattern
  0x0781   |   0x5151    |   SanDisk Cruzer Micro Skin 8GB
  0x0781   |   0x540e    |   SanDisk Cruzer Contour
  0x0781   |   0x5530    |   SanDisk Cruzer
  0x0781   |   0x5535    |   SanDisk Ultra Backup

''')

input(' Press Enter to return to menu...')



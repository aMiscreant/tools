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
import subprocess
import sys
import time

# Try importing optional banner module
try:
    import banner
except ImportError as error:
    print('\n[-] Failed to import "banner" module\n')
    print(error)
    banner = None  # Prevent NameError

define_path = os.getcwd()
sys.path.append('%s/src/' % define_path)

# Helper to safely print banner if available
def safe_banner():
    if banner:
        banner.print_banner()

try:
    safe_banner()
    print(' Detecting Device...\n')

    u3_ids = ['5406', '5408', '5151', '5530', '5535', '550a', '540e']
    vendor_id = '0781:'
    found_device = False
    deviceName = None

    # Search for SanDisk U3 devices
    for dev_id in u3_ids:
        try:
            device = subprocess.check_output(
                f"lsusb -d {vendor_id}{dev_id}",
                shell=True,
                stderr=subprocess.DEVNULL
            )
            print(' Device Found:', device.decode().strip())
            found_device = True
        except subprocess.CalledProcessError:
            pass  # Device not found, continue

    time.sleep(2)
    safe_banner()
    print(' Detecting Partitions...')
    time.sleep(2)

    with open("/proc/partitions") as partitionsFile:
        lines = partitionsFile.readlines()[2:]

    for line in lines:
        words = [x.strip() for x in line.split()]
        if len(words) < 4:
            continue

        minorNumber = int(words[1])
        devName = words[3]

        if minorNumber % 16 == 0:
            path = f"/sys/class/block/{devName}"
            if os.path.islink(path) and "/usb" in os.path.realpath(path):
                if devName.startswith("sd"):
                    deviceName = devName
                    print(f"\n Partition Found: /dev/{devName}1")
                    time.sleep(2)
                    break  # Stop at first match

except KeyboardInterrupt:
    print('\n[-] Keyboard Interrupt, Exiting')
    time.sleep(1)
    sys.exit(0)
except Exception as e:
    print('[-] Something went wrong, printing error message..')
    print(e)
    time.sleep(2)
    sys.exit(1)

# ========== Final Check ==========

try:
    if not deviceName:
        print('\n[-] No USB storage device found.')
        sys.exit(1)

    safe_banner()

    if deviceName.startswith('sda'):
        print('[-] Refusing to touch system drive (sda). No devices modified.')
        time.sleep(2)
    else:
        print('\n=================================')
        print(f'\n Device information for /dev/{deviceName}\n')
        print('=================================\n')
        subprocess.Popen(f'u3-tool -D /dev/{deviceName}', shell=True).wait()

    input('\nPress Enter To Continue..')  # Python 3
except Exception as error:
    print('[-] Something went wrong, printing error message..')
    print(error)
    time.sleep(2)
    sys.exit(1)

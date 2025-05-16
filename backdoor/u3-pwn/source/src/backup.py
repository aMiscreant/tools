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

import pexpect

try:
    import banner
except ImportError as error:
    print('\n[-] Failed to import module\n')
    print(error)
    banner = None  # define banner as None to avoid NameError later
    sys.exit(1)

define_path = os.getcwd()
src_path = os.path.join(define_path, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    banner.print_banner()
    print('Detecting Device...\n')
    u3 = ['5406', '5408', '5151', '5530', '5535', '550a', '540e']
    vendor_id = '0781:'
    device_found = False

    for id in u3:
        try:
            device = subprocess.check_output(f"lsusb -d {vendor_id}{id}", shell=True).decode()
            print(f'Device Found: {device.strip()}')
            device_found = True
        except subprocess.CalledProcessError:
            pass  # Device not found for this ID

    if not device_found:
        print('[-] No U3-compatible device found. Exiting.')
        sys.exit(1)

    time.sleep(2)
    banner.print_banner()
    print('Detecting Partitions...')
    time.sleep(2)

    with open("/proc/partitions") as partitionsFile:
        lines = partitionsFile.readlines()[2:]

    deviceName = None
    for line in lines:
        words = [x.strip() for x in line.split()]
        minorNumber = int(words[1])
        dev = words[3]
        if minorNumber % 16 == 0:
            path = f"/sys/class/block/{dev}"
            if os.path.islink(path) and "/usb" in os.path.realpath(path):
                if dev.startswith("sd"):
                    deviceName = dev
                    print(f"\nPartition Found: /dev/{dev}1")
                    time.sleep(2)

    if not deviceName:
        print("[-] No USB partitions found. Exiting.")
        sys.exit(1)

except KeyboardInterrupt:
    print('\n[-] Keyboard Interrupted. Exiting.')
    time.sleep(2)
    sys.exit(0)
except Exception as error:
    print('[-] Something went wrong. Error:')
    print(error)
    time.sleep(2)
    sys.exit(0)

# === Partition and ISO Replacement ===
try:
    banner.print_banner()

    if deviceName.startswith('sda'):
        print('No Devices Found or trying to overwrite primary disk. Returning to menu.')
        time.sleep(2)
    else:
        banner.print_banner()
        print(f'\nCreating a new partition of 8058880 bytes on /dev/{deviceName}\n')
        child1 = pexpect.spawn(f'u3-tool -v -p 8058880 /dev/{deviceName}')
        child1.sendline('y')
        time.sleep(5)

        print(f'\nPartitioning completed on /dev/{deviceName}')
        banner.print_banner()

        print(f'\nInserting new ISO to virtual ROM partition on /dev/{deviceName}\n')
        subprocess.run(
            f'u3-tool -l "backup/origU3/U3 System.iso" /dev/{deviceName}',
            shell=True,
            check=True
        )

        banner.print_banner()
        print(f'\nSuccessfully backed up /dev/{deviceName}')
        time.sleep(2)

except Exception as error:
    print('[-] Something went wrong during partition or ISO write:')
    print(error)
    time.sleep(2)
    sys.exit(0)
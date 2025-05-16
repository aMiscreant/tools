#!/usr/bin/env python3
import os
import sys

try:
    import banner
except ImportError:
    print("\n[-]Failed To Import Module")
    banner = None  # define banner as None to avoid NameError later



define_path = os.getcwd()
sys.path.append('%s/src/' % define_path)

banner.print_banner()

print("U3-Pwn Change Log")
print("""
===================================================================================
Rebuilt most of the tool, added more user input sanitization (cheers Shadow Master)
Recompiled shellcode exec to bypass av again.
===================================================================================
NEW CHANGES HERE by aMiscreant

===================================================================================

""")

raw_input('Press Enter To Return To Menu..')

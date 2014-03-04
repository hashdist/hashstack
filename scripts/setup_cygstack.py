#!/usr/bin/env python
"""
Install 64-bit Cygwin dependences needed by HashStack.

This utility script uses Cygwin's setup-x86_64.exe program to install
dependencies needed both to run HashStack as well as dependencies for
commonly installed packages within HashStack.  This script is mostly
scaffolding to get users up and running on HashStack and is a first
effort.  Improvements and suggestions welcome!
"""

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("CYGSTACK", nargs="?", default="cygstack.txt",
                    help="List of packages to install, use cygcheck -cd to generate")


args = parser.parse_args()

try:
    subprocess.check_call(['which', 'setup-x86_64.exe'])
except:
    sys.stderr.write('Unable to find setup-x86_64.exe, please put it on your PATH and re-execute this script.\n')
    sys.stderr.write('You could try: \n\nwget http://cygwin.com/setup-x86_64.exe -O /usr/bin/setup-x86_64.exe\n')
    sys.exit(1)

subprocess.check_call(['cygcheck','-c'])

def get_installed_packages():
    packages = subprocess.check_output(['cygcheck','-c', '-d'])
    # split lines on Windows carriage returns
    packages = packages.split('\r\n')
    # header_data
    packages = packages[2:]
    # package name
    packages = [p.split()[0] for p in packages if p]
    return packages

cygstack = args.CYGSTACK

print "Using %s as list of packages to install." % cygstack

with open(cygstack) as packages:
    # header_data
    packages.readline()
    packages.readline()

    for package_line in packages.readlines():
        installed_packages = get_installed_packages()
        package = package_line.split()[0]

        if package in installed_packages:
            print 'already installed', package_line
            continue

        print 'installing', package
        call = ['setup-x86_64.exe', '-q', '-P', package]
        subprocess.check_call(call)

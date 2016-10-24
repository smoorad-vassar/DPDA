#!/usr/bin/env python

'''
' dpda.py
'
' Python simulation of a DPDA according to a
' definition file. Tests strings for acceptance.
'
' Will Badart
' OCT 2016
'''

from getopt import getopt
import sys


#==================
# Class definition
#==================

class DPDA:

    def __initialize__(self, defn_fnmae):
        pass

    def test(self, test_fname):
        pass


#================
# Main execution
#================

if __name__ == '__main__':

    def usage():
        print >>sys.stderr, '''usage: {} DEFINITION_FILE TEST_FILE [ -h ]
    -h      Display this help message

    DEFINITION_FILE is the name of the file which has the specifications
    for the unit under test

    TEST_FILE is the name of the file with the list of test strings'''.format(sys.argv[0])
        sys.exit(0)
    
    DEFN_FNAME = 'M1.txt'
    TEST_FNAME = 'M1-Accept.txt'

    opts, args = getopt(sys.argv[1:], 'h')
    for o, a in opts:
        if o == '-h':
            usage()

    if args[0]:
        DEFN_FNAME = args[0]
    if args[1]:
        TEST_FNAME = args[1]

    uut = DPDA(DEFN_FNAME)
    uut.test(TEST_FNAME)

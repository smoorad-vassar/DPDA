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

    def __init__(self, defn_fnmae):

        # Parse file
        lines = [line.rstrip() for line in open(defn_fnmae)]

        # Set, echo name
        self.name = lines[0]
        print self.name

        # Set sigma, gamma, Q, q0, stack
        self.E  = lines[1].split(',')
        self.G  = lines[2].split(',')
        self.Q  = lines[3].split(',')
        self.q0 = lines[4]
        self.F  = lines[5].split(',')
        self.stack = []

        # Parse rules
        self.d = {}
        for n, line in enumerate(lines[6:]):

            lhs = tuple(line.split('|')[0].split(','))
            rhs = tuple(line.split('|')[1].split(','))

            print '{}: {}'.format(n + 1, line)
            self.d[lhs] = rhs

        self.reset()
        print


    def test_file(self, test_fname):
        print 'Testing file: {}\n'.format(test_fname)
        strings = [line.rstrip() for line in open(test_fname)]
        for string in strings:
            print 'Accepted' if self.test(string) else 'Rejected'
            print


    def test(self, string):

        print 'String: ', string
        self.reset()
        n = 1

        for char in string:

            if char not in self.E:
                return False

            # Check for epsilon rule
            rhs = self.d.get((self.q, char, '~'))

            # Check for stack rule
            if not rhs:
                rhs = self.d.get((self.q, char, self.stack[-1] if self.stack else '~'))

            # If rule found, perform pop, else string not accepted
            stack = None
            if rhs:
                stack = self.stack and self.stack.pop()
            else:
                return False

            print '{}#{}: {}, {}, {} | {}, {}'.format(n,\
                    self.d.keys().index((self.q, char, stack or '~')) + 1,\
                    self.q, char, stack or '~', rhs[0], rhs[1])

            self.q = rhs[0]
            if rhs[1] != '~':
                self.stack.append(rhs[1])
            n += 1

        return self.q in self.F

    def step(self):
        string = ''
        while string != 'quit':
            string = raw_input('> ')
            self.test(string)

    def reset(self):
        self.q = self.q0


#================
# Main execution
#================

if __name__ == '__main__':

    DEFN_FNAME  = 'M1.txt'
    TEST_FNAME  = 'M1-Accept.txt'
    INTERACTIVE = False

    def usage():
        print >>sys.stderr, '''usage: {} DEFINITION_FILE TEST_FILE [ -h ]
    -h      Display this help message

    DEFINITION_FILE is the name of the file which has the specifications
    for the unit under test

    TEST_FILE is the name of the file with the list of test strings'''.format(sys.argv[0])
        sys.exit(0)
    

    opts, args = getopt(sys.argv[1:], 'hi')
    for o, a in opts:
        if o == '-h':
            usage()
        if o == '-i':
            INTERACTIVE = True

    if args:
        if args[0]:
            DEFN_FNAME = args[0]
        if args[1]:
            TEST_FNAME = args[1]

    uut = DPDA(DEFN_FNAME)
    if INTERACTIVE:
        uut.step()
    else:
        uut.test_file(TEST_FNAME)

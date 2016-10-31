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

    def __init__(self, defn_fnmae, shell=False):

        stream = open('/dev/null', 'w') if shell else sys.stdout

        # Parse file
        lines = [line.rstrip() for line in open(defn_fnmae)]

        # Set, echo name
        self.name = lines[0]
        print >>stream, self.name

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

            print >>stream, '{}: {}'.format(n + 1, line)
            self.d[lhs] = rhs

        self.reset()
        print >>stream


    def test_file(self, test_fname, shell):

        stream = open('/dev/null', 'w') if shell else sys.stdout
        print >>stream, 'Testing file: {}\n'.format(test_fname)

        strings = [line.rstrip() for line in open(test_fname)]
        for string in strings:

            print >>stream, 'Accepted' if self.test(string, stream) else 'Rejected'
            print >>stream

            if 'Accept' in test_fname:
                if not self.test(string, stream):
                    sys.exit(1)
            else:
                if self.test(string, stream):
                    sys.exit(1)


    def test(self, string, stream=sys.stdout):

        print >>stream, 'String: ', string
        self.reset()

        for i, char in enumerate(string):

            rule, rhs  = self.getrule(self.q, char, self.stack[-1] if self.stack else '~')

            if char not in self.E or not rhs:
                return False

            print >>stream, '{}#{}: {}, {}, {} | {}, {}'.format(i + 1,\
                    self.d.keys().index(rule) + 1 if rule in self.d.keys() else 1,\
                    rule[0], rule[1], rule[2], rhs[0], rhs[1])

            self.transition(rule)

        return self.q in self.F and not self.stack

    def transition(self, rule):
        rhs       = self.getrule(*rule)[1]
        stackchar = self.stack.pop() if self.stack and rule[2] != '~' else None
        self.q    = rhs[0]
        if rhs[1] != '~':
            self.stack.append(rhs[1])

    def getrule(self, state, char, stackchar='~'):
        if self.d.get((state, char, '~')):
            return ((state, char, '~'), self.d.get((state, char, '~')))
        elif self.d.get((state, '~', '~')):
            return ((state, '~', '~'), self.d.get((state, char, '~')))
        elif self.d.get((state, '~', stackchar)):
            return ((state, '~', stackchar), self.d.get((state, '~', stackchar)))
        return ((state, char, stackchar), self.d.get((state, char, stackchar)))

    def step(self):
        string = ''
        while string != 'quit':
            string = raw_input('> ')
            self.test(string)

    def reset(self):
        self.stack = []
        self.q = self.q0


#================
# Main execution
#================

if __name__ == '__main__':

    DEFN_FNAME  = 'M1.txt'
    TEST_FNAME  = 'M1-Accept.txt'
    INTERACTIVE = False
    SHELL       = False

    def usage():
        print >>sys.stderr, '''usage: {} DEFINITION_FILE TEST_FILE [ -h ]
    -h      Display this help message

    DEFINITION_FILE is the name of the file which has the specifications
    for the unit under test

    TEST_FILE is the name of the file with the list of test strings'''.format(sys.argv[0])
        sys.exit(0)
    

    opts, args = getopt(sys.argv[1:], 'his')
    for o, a in opts:
        if o == '-h':
            usage()
        if o == '-i':
            INTERACTIVE = True
        if o == '-s':
            SHELL = True

    if args:
        if args[0]:
            DEFN_FNAME = args[0]
        if args[1]:
            TEST_FNAME = args[1]

    uut = DPDA(DEFN_FNAME, SHELL)
    if INTERACTIVE:
        uut.step()
    else:
        uut.test_file(TEST_FNAME, SHELL)

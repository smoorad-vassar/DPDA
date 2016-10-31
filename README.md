PDA
===

This program simulates a deterministic push-down automata. The simulation
tests strings to see whether or not they'd be accepted.

Usage
-----

First, please ensure that your computer is running Python 2.7.x (`python
--version`). Next, see below for command formatting.

```
$ ./dpda.py -h
usage: ./dpda.py DEFINITION_FILE TEST_FILE [ -s -i -h ]

    -s      Enable shell mode (disable output and communicate test status
via exit code)
    -i      Enable interactive mode (input individual strings for test)
    -h      Display this help message

    DEFINITION_FILE is the name of the file which has the specifications
    for the unit under test

    TEST_FILE is the name of the file with the list of test strings
```


Student test machine
--------------------

`M4.txt` is the definition file for the student-provided machine. The machine
accepts the language `{ a^n b^n | n > 1}`. Two test files are provided which
contain strings that should all be accepted or rejected by the machine
(`M4-Accept.txt` and `M4-Reject.txt` respectively).


Test script
-----------

`test.sh` tests each machine for the expected output of each test, including
M4, the student machine. Usage:

```
$ ./test.sh
Testing M1
Accept test for M1 PASSED
Reject test for M1 PASSED
# ...
```

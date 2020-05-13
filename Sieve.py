"""
Copyright (c) 2009 John Markus Bjoerndalen <jmb@cs.uit.no>,
      Brian Vinter <vinter@nbi.dk>, Rune M. Friborg <rune.m.friborg@gmail.com>.
See LICENSE.txt for licensing details (MIT License). 
"""

# from pycsp_import import *
from csp.csp import *

@process
def producer(cout, cnt):
    print("[INFO] Currently in producer...")
    for i in range(2,cnt):
        print("[INFO] Stuck in producer for loop...")
        cout.write(i)
    print("[INFO] Exited producer for loop...")
    cout.poison()
    
@process
def worker(cin, cout):
    print("[INFO] Currently in worker...")
    try:
        ccout = None
        my_prime = cin.read()
        cout.write(my_prime)
        child_channel = Channel()
        ccout = child_channel
        print("blah")
        Par(worker(child_channel, cout)).start()
        print("blah blah")
        while True:
            print("[INFO] Stuck in worker while loop...")
            new_prime = cin.read()
            print("New Prime: {}".format(new_prime))
            if new_prime%my_prime:
                print("[INFO] if condition inside while loop has been met...")
                ccout.write(new_prime)
                print("[INFO] Child channel wrote something prolly")
    except Exception:
        print("[ERROR] Poison exception occurred!")
        if ccout:
            ccout.poison()
        else:
            cout.poison()

    print("[INFO] Exited the worker...")

@process
def printer(cin):
    print("[INFO] Currently in printer...")
    while True:
        print("[INFO] Stuck in printer while loop...")
        print(cin.read())
    print("[INFO] Exited printer while loop...")

first = Channel()
outc = Channel()

Par(producer(first,2000), worker(first, outc), printer(outc)).start()

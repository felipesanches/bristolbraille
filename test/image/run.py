#!/usr/bin/env python
import feed
import time
import analyse
import os
import datetime

ensure_unlock = False

sequences = [ #black is true, white is false
    [False,False,False],
    [False,False,True],
    [False,True,False],
    [True,False,True],
    [False,True,True],
    [True,True,True],
    [True,True,False],
    [True,False,False],
    ]

#set up arduino feeder
feed.args = feed.get_args()
feed.serial_port = feed.setup_serial()

log_file = 'log.txt'
log = open(log_file,'w', 1) #line buffered

#how much we rotate by
one_step = 200/8
#steps to go back after moving to the right pos
correction = -6

log.write("started\n")
log.write("pos, date, expected, got, pass/fail\n")
failures = 0
while failures < 10:
    for i in range(8):
        response = feed.send_robot_commands(["s%d,0,0" % i])
        response = feed.send_robot_commands(["f%d" % correction])

        #take photo
        os.system("./takePhoto.sh")

        #analyse photo
        analyse.args = analyse.get_args()
        matches = analyse.analyse()

        result = False
        if matches == sequences[i]:
            result = True;
        else:
            failures += 1

        print "result: ", result

        if ensure_unlock:
            #turn back motor to ensure stopper is back
            print "unlock slider back"
            response = feed.send_robot_commands(["f%d" % -50])
            print "unlock slider forward"
            response = feed.send_robot_commands(["f%d" % 50])

        #reset the rotor by going back the same amount we shoudl have gone forward

        log.write( "%d, %s, %s, %s, %s\n" % (i, datetime.datetime.now(),sequences[i],matches,result))
    #    os.system("eog regions.jpg");

        print "reset"
        codes = ["f%d" % (-one_step * i)]
        response = feed.send_robot_commands(codes)


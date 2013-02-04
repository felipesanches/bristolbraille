import feed
import analyse
import os
import datetime

sequences = [ #black is true, white is false
    [False,False,False],
    [True,False,False],
    [True,True,False],
    [True,True,True],
    [False,True,True],
    [True,False,True],
    [False,True,False],
    [False,False,True],
    ]

#set up arduino feeder
feed.args = feed.get_args()
feed.serial_port = feed.setup_serial()

log_file = 'log.txt'
log = open(log_file,'w')

#how much we rotate by
r = 200/8;
codes=['f%d' %r]

log.write("started\n")

while True:
    for i in range(8):

        s = "rotor pos %d, time %s : " % (i, datetime.datetime.now())
        print s,
        log.write(s)

        #take photo
        os.system("./takePhoto.sh")

        #analyse photo
        analyse.args = analyse.get_args()
        matches = analyse.analyse()
        if matches == sequences[i]:
            print "pass"
            log.write("pass\n")
        else:
            print "fail"
            log.write("fail\n")

        #turn motor
        response = feed.send_robot_commands(codes)

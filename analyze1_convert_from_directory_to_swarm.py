#!/usr/bin/python
'''

First step to process the monitoring outputs.
This scripts converts from session directory structure format to session swarm format (one file per swarm).

'''
import sys, time, getopt, urllib, random, struct, commands, os, platform, operator, socket

from analyze0_main import *


PL_FILE_NAME = "00_data_source/servers_status.txt"

CONVERT_FROM_SWARM_TO_PEERS = True
PLOT_SCATTER_PEERS_OVER_TIME = True
SPLIT_MONITORS = True


delaDir = Dirs().delayed


def print_usage():
    print ""
    print "This script converts Tracker lens results from a dir (many files) to SWARM format (one file per swarm, one peerlist per line)"

    #print "This script first creates an output file for session given swarm from session set files (inside session chosen directory) from monitoring."
    #print "Then, the 'convert2' script converts the resulting file to session_line format."
    print ""
    print "USAGE:"
    print "-h --help show this usage help message"
    print "-f --file=[file] input file (html) with magnetlinks"
    print "-d --dir=[dir] list of directories ($dir) that contains monitoring outputs separated by ','. (find $dir -file_name_base '*.gz') "
    print "-p --pos=[number] position of the first swarm "
    print "-n --num=[number] number of swarms to analyze"
    print "-t --time=[epoch] monitoring start"
    print "-s --sort To sort or not to sort? default is not to sort"
    print "-l --peerlistSize max peer list Size. Value=0 means no limit. Default value=0 "
    print "-r --resolution. {0 .. 100}% Value=0 means none. Default value=100 (%, full resolution) "
    #print "-m --mon=[number] number of monitoring results to analyze 1<=x<=50"
    print ""


def is_float_try(str_):
    try:
        float(str_)
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    # HEADER
    print "\n"
    script_name = os.path.basename(__file__)
    print script_name.upper()
    print "-" * len(script_name)

    # INITIALIZE VARIABLES
    inputFileName = ""
    inputDirs = ""
    swarm_pos = 0
    swarm_number = 1
    monitoringStartEpoch = 0
    resolution = 100
    toSort = True

    maxPeerListSize=0
    #processa parametros
    try:

        optlist, args = getopt.gnu_getopt(sys.argv[1:], 'hf:d:p:n:t:sl:r:',
                                          ['help', 'file=', 'dir=', 'pos=', 'num=', 'time=', 'sort', 'peerListSize=', 'resolution='])
        for o, a in optlist:
            if o in ["-h", "--help"]:
                print_usage()
                sys.exit(0)

            elif o in ["-f", '--file']:
                inputFileName = a

            elif o in ["-d", '--dir']:
                inputDirs = a

            elif o in ["-p", '--pos']:
                swarm_pos = int(a)

            elif o in ["-n", '--num']:
                swarm_number = int(a)

            elif o in ["-t", '--time']:
                monitoringStartEpoch = int(a)

            elif o in ["-s", "--sort"]:
                toSort = True

            elif o in ["-l", "--peerListSize"]:
                maxPeerListSize = int(a)

            elif o in ["-r", "--resolution"]:
                resolution = int(a)

    except Exception, e:
        print "Exception:", e
        print "Please, use -h or --help for instructions on how to use this script."
        sys.exit(-1)

    if inputDirs == "" or inputFileName == "":
        print "input dir or output file is null."
        print "Please, use -h or --help for instructions on how to use this script."
        sys.exit(-1)


    #le arquivo
    countTorrents = 0
    countTorrentsTrackers = 0

    i = 0
    torrents = list();
    trackers = {};
    try:
        print "Opening_file:%s" % inputFileName
        fData = open(inputFileName, 'r')
        print "Loading_file:%s" % inputFileName
        sData = fData.read().split('\n')
        fData.close()
        for line in sData:

            print ""
            i = i + 1

            if line.partition('magnet:')[2] == '':
                pass
            #                    if debug:
            #                    print "blank_line..."
            else:
                print "line_being_processed:", line
                countTorrents += 1
                magnetlink = line.partition('magnet:')[2].partition('"')[0]
                #print magnetlink
                infohash_hex = magnetlink.partition('btih:')[2].partition('&')[0]
                torrent = Torrent(infohash_hex)

                print "infohash_hex:", infohash_hex
                #procura pelos enderecos de rastreadores
                it = 0
                while True:
                    it = it + 1
                    tracker = magnetlink.partition('&tr=')[2]
                    if tracker == '':
                        break
                    else:
                        countTorrentsTrackers += 1
                        magnetlink = tracker
                        tracker = tracker.partition('&')[0]
                        tracker = tracker.replace('%3A', ':').replace('%2F', '/')
                        #                            tracker = tracker.replace('udp:','http:')
                        print "tracker:", it, " end:", tracker
                        #                            tr = tr(infohash_url, tracker, 0)
                        #                            print tr
                        torrent.trackers.append(tracker)
                        tracker_ = None
                        if not tracker in trackers:
                            tracker_ = Tracker(tracker)
                        else:
                            tracker_ = trackers[tracker]
                        tracker_.torrents.append(infohash_hex)
                        trackers[tracker] = tracker_

                torrents.append(torrent)

    except Exception, e:
        print "error_during_file_processing:", inputFileName, " line:", i, " exception:", e
        sys.exit()

    print "file_processing_finish!"
    print "NUMBER_OF_TORRENTS:" + str(countTorrents) + " NUMBER_OF_TORRENTS_AND_TRACKERS:" + str(countTorrentsTrackers)

    for t in torrents:
        pass
        #print session_begin.infohash, " ", len(session_begin.trackers), " ", session_begin.trackers

    for t in trackers:
        tracker = trackers[t]
        #print session_begin, " ", len(tracker.torrents), " ", tracker.torrents

    if swarm_pos + swarm_number > countTorrents:
        print_usage()
        print "_-----_---_-_---_-_-__-_--_----_--_-_____---_"
        print " Swarm pos + number must be < ", countTorrents
        print " Swarm pos   : ", swarm_pos
        print " Swarm number: ", swarm_number
        sys.exit()

    print "\n\n\n"

    print "+-------------------------------------"
    print " SETTINGS"
    print "+-------------------------------------"
    print " SPLIT MONITORS       : ", SPLIT_MONITORS
    print ""
    print "+-------------------------------------"
    print " INPUT PARAMETERS"
    print "+-------------------------------------"
    print " Swarm Input file     : ", inputFileName
    print " Input dirs           : ", inputDirs
    print " Swarm position       : ", swarm_pos
    print " Swarm number         : ", swarm_number
    print " Resolution           : ", resolution
    #print " Swarms: ", torrents[swarm_pos:swarm_pos + swarm_number]
    print " To sort?             : ", toSort
    print ""
    print "+-------------------------------------"
    print " CALCULATED PARAMETERS"
    print "+-------------------------------------"

    monitors = []
    try:
        f = open(PL_FILE_NAME)

        sentinelsFileName = "01_data_servers/servers_sentinels.txt"
        monitorsFileName = "01_data_servers/servers_monitors.txt"
        f_sentinels = open(sentinelsFileName, 'w')
        f_monitors = open(monitorsFileName, 'w')

        for l in f:
            # print l
            monitor = Monitor(l)
            if SPLIT_MONITORS:
                monitors.append(monitor)

            if monitor.isSentinel:
                f_sentinels.write(monitor.host + "\n")
            else:
                f_monitors.write(monitor.host + "\n")

        if not SPLIT_MONITORS:
            monitor = Monitor()
            monitor.line = "all"
            monitor.startTimeEpoch = monitoringStartEpoch
            monitors.append(monitor)

        f.close()
        f_sentinels.close()
        f_monitors.close()

        monitoringStartEpoch = min(monitors, key=lambda m: m.startTimeEpoch).startTimeEpoch
        print " Sentinels file name  :", sentinelsFileName
        print " Monitors file name   :", monitorsFileName
        print " Start time epoch     :", monitoringStartEpoch

    except Exception as e:
        print "[Warning] some file with sentinel and/monitor were not found.", e

    print ""
    print "+-------------------------------------"
    print " PROCESSING DATA"
    print "+-------------------------------------"

    s = 0
    c = 0
    timec = 0
    times = 0
    sumSize_f = 0
    sumSize_s = 0

    count_torrent = 1

    for t in torrents[swarm_pos:swarm_pos + swarm_number]:

        print "\n TORRENT (%d/%d) : %s \n"%(count_torrent, len(torrents[swarm_pos:swarm_pos + swarm_number]), t)
        count_torrent += 1

        #temporary files
        tempName = t.tempFileName
        procName = t.procFileName
        sortName = t.get_swarm_file_name(resolution)

        cmd = "rm %s " %(tempName)
        run_cmd(cmd, 1)
        count_slot = -1

        hash_count_monitor = 0

        # this loop is necessary for correcting monitors clock delays
        for m in monitors:
            print "\n\tMONITOR:", m
            #pass
            #Compatibilidade Linux/MacOS
            #Linux
            tempName2 = delaDir + t.infohash + "_m_%02d.txt" % hash_count_monitor
            hash_count_monitor += 1
            cmd = "rm %s "%(tempName2)
            run_cmd(cmd, 2, False)

            gzcat = " zcat "
            if "Darwin" in platform.platform():
                #MacOS
                gzcat = " gzcat "

            for inputDir in inputDirs.split(','):
                #print "\session_begin\tMonitor:", m.monitorName
                #print "\session_begin\tDir    :", inputDir
                #print "\session_begin\tTorrent:", session_begin.infohash
                principal = " grep %s | " % t.infohash

                principal += " while read line; do peer_id=`echo $line | cut -d \" \" -f 6-`; session_begin=`echo $line | cut -d \" \" -f 4`; echo $session_begin $peer_id; done "
                if monitor.line == "all":
                    # TODO: FIX HACK FOR THE EXPERIMENT NAME
                    cmd = ' find ' + inputDir + ' -name "*%s*.gz"' % "2018-11-30_17-"
                else:
                    cmd = ' find ' + inputDir + ' -name "*%s*.gz"' % m.monitorName

                cmd += ' | xargs ' + gzcat + " | " + principal + " >> " + tempName2

                run_cmd(cmd, 2, True)

            #print "open files: ", tempName2, tempName
            fin = open(tempName2, 'r')
            fout = open(tempName, 'a')

            res_total = 0
            res_count_1 = 0
            res_count_2 = 0
            for line_fin in fin:

                try:
                    epoch_original = float(line_fin.split(" ")[0])

                except ValueError:
                    if is_float_try(line_fin.split(" ")[1]):
                        epoch_original = float(line_fin.split(" ")[1])
                    else:
                        # hack to read output from old monitor versions...
                        print "error value while processing file."
                        print "file in : ", tempName2
                        print "file out:", tempName
                        print "line in : ", line_fin
                        continue
                        #epoch_original = float(line_fin.split(" ")[1])

                except:
                    print "error while processing file."
                    print "file in : ", tempName2
                    print "file out:", tempName
                    print "line in : ", line_fin
                    sys.exit()

                epoch_delayed = epoch_original + m.client_minus_server_epoch
                resolution_value = random.randint(0, 100)
                #print "resolution_value: %d resolution: %d" % (resolution_value, resolution)
                res_total +=1
                if resolution_value <= resolution:
                    res_count_1 += 1
                    fout.write("%f %s\n" % (epoch_delayed, line_fin.split(" ")[1:]))
                else:
                    res_count_2 += 1

            fin.close()
            fout.close()
            if res_total > 0:
                print "res_total: %d (%f) res_count_1 (file): %d (%f) res_count_2 (ignored): %d (%f)" %(res_total, (res_total*1.0/res_total), res_count_1, (res_count_1*1.0/res_total), res_count_2, (res_count_2*1.0/res_total))
            else:
                print "res_total == 0"

            cmd = "rm %s"%tempName2
            run_cmd(cmd, 2, False)
            #print "close files: ", tempName2, tempName

        cmd = " sort -n -k 1 " + tempName + " > " + sortName
        run_cmd(cmd, 2, True)

    print "+-------------------------------------"
    print " END"
    print "+-------------------------------------"
    print ""
    print "%s %s finished!" % (now_str(), script_name)
    print ""
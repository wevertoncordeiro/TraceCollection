#!/bin/bash

FILE="0"
PROB="undef" # failure prob: must be expressed between [0,100]
SEED=1
SKIP_SORT=0

while getopts hsf:r:p: option; do
        case "${option}" in
                h)
                        echo "`basename $0`: emulates failure probability in a trace file";
                        echo "";
                        echo "    trace file must be in format \"window time_min IP:port peerId monitorId monitor\"";
                        echo "    (without quotes). output is a trace file in the same format";
                        echo "";
                        echo "`basename $0`: args";
                        echo "  -s      skip file sorting (input must be sorted by window and peerId, numerically)";
			echo "          pair (window,peerId) must be unique";
                        echo "  -f      input file";
                        echo "  -r      random number generator seed";
                        echo "  -p      failure probability";
                        echo "";
                        exit 0;
                        ;;
                s) SKIP_SORT=1;;
                f) FILE=${OPTARG};;
                r) SEED=${OPTARG};;
                p) PROB=${OPTARG};;
        esac;
done

if [ $FILE = "0" ]; then
  echo "-f : File must be specified";
  exit 1;
fi;

if [ $PROB = "undef" ]; then
  echo "-p : Failure probability must be specified";
  exit 1;
fi;

# file format:
#window #time_min #IP:port #peerId #monitorId #monitor

# input random number generator seed
RANDOM=$SEED

FILE_SORTED=${FILE};

# first, sort the input file per window then per peerid
if [ $SKIP_SORT -ne 1 ]; then
  sort -u -k1n,1 -k4n,4 ${FILE} > ${FILE}.sort_u_1n_4n;
  FILE_SORTED=${FILE}.sort_u_1n_4n;
fi;

DEBUG=${FILE_SORTED}.fail${PROB}_seed${SEED}_debug;
OUTPUT=${FILE_SORTED}.fail${PROB}_seed${SEED};

#cleanup
rm -f $DEBUG;
rm -f $OUTPUT;

# keep stats of number of peers within window, number of failed
curr_window=-1
count_peers=0;
count_failed=0;

echo "debug file is ${DEBUG}";
echo "output file is ${OUTPUT}";

while read line; do
	set -- $line;
	window=$1;

	failure=$((RANDOM%101));

	if [ $curr_window -ne $window ]; then
		if [ $curr_window -ne -1 ]; then
			echo "stat: window $curr_window: peers $count_peers failed $count_failed" >> ${DEBUG};
		fi;
		curr_window=$window;
		count_peers=0;
		count_failed=0;
	fi;

	let count_peers=count_peers+1;

	if [ $PROB -lt $failure  ]; then
		echo $line >> ${OUTPUT};
	else
		echo "peer $4 failed at window $1: $failure" >> ${DEBUG};
		let count_failed=count_failed+1;
	fi
done < <(tail -n+2 ${FILE_SORTED})

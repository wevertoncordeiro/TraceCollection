#!/bin/bash

# file must be in format #peerid #window.
# file must be sorted by #peerid, then by #window
# this script does not perform any sorting

INPUT="0";
WORKING_DIR="undef";
OUTPUT="0";
GAP=0;

while getopts hf:n:o:d: option; do
  case "${option}" in
    h)
      echo "`basename $0`: correct gaps in the snapshot file";
      echo "";
      echo "    a gap is a sequence of windows in which a peer";
      echo "    is not sampled. a gap is only considered in";
      echo "    between windows that peer has already appeared.";
      echo "";
      echo "    input file must be in format #peerid #window";
      echo "    input file must be sorted by #peerid, then by #window";
      echo "";
      echo "`basename $0`: args";
      echo "  -f      input file";
      echo "  -d      dir in which stats files must be stored";
      echo "  -o      output file";
      echo "  -n      maximum window gap size considered as failure [ 0 - none ]";
      echo "";
      exit 0;
    ;;
    f) INPUT=${OPTARG};;
    o) OUTPUT=${OPTARG};;
    d) WORKING_DIR=${OPTARG};;
    n) GAP=${OPTARG};;
  esac;
done

test $INPUT = "0" && { echo "-f : Input file must be specified"; exit 1; }
test $OUTPUT = "0" && { echo "-o : Output file must be specified"; exit 1; }

if [[ $WORKING_DIR = undef ]]; then
  WORKING_DIR=`dirname ${INPUT}`;
else
  mkdir -p ${WORKING_DIR} || { echo "cannot create dir ${WORKING_DIR}"; exit 1; }
fi;

rm -rf $WORKING_DIR/interval.sizes ${OUTPUT};

address=-1; #undefined

while read line; do
  if [[ ${line:0:1} = \# ]] ; then echo $line >> ${OUTPUT}; continue; fi;
  set -- $line;

  if [ $1 -ne $address ]; then
    # we are processing a different address. flush previous address if it exists
    if [ $address -ne -1 ]; then
      echo "G $begin $end $count" >> $WORKING_DIR/interval.sizes;
      echo "G $begin $end $count"; #debug
    fi;

    # init session begin/end markers and counter
    address=$1; begin=$2; end=$2;
    let count=1;

    # we can output this line directly
    echo $line >> ${OUTPUT};

    # put address in the stats file
    echo "A $address" >> $WORKING_DIR/interval.sizes;
    echo "A $address" #debug
  else
    # address remains the same
    current=$2;

    # check if this is a continuous session. if so, increment positive
    # snapshot sequence length and push session end to the current window
    if [ $current -eq $((end+1)) ]; then
      let count=count+1;
      end=$current;

      # output snapshot to the file
      echo $line >> ${OUTPUT};
    else
      # this is not a continuous session. flush positive snapshot sequence len
      echo "G $begin $end $count" >> $WORKING_DIR/interval.sizes;
      echo "G $begin $end $count"; #debug

      gaplen=$((current-end-1));
      # now flush null snapshot sequence length
      echo "B $end $current $gaplen" >> $WORKING_DIR/interval.sizes;
      echo "B $end $current $gaplen"; # debug

      # check if there is a gap that should be corrected
      if [ ${gaplen} -le ${GAP} ]; then
        # output snapshots to close the gap
        for i in `seq $((end+1)) $((current-1))`; do
          echo "$address $i" >> $OUTPUT;
        done;
      fi;
      
      # now, output the line read
      echo $line >> ${OUTPUT};

      # update positive snapshot sequence len and session begin/end markers
      let count=1;
      begin=$2; end=$2;
    fi;
  fi;
done < <(cat ${INPUT})

# record the last session which was not yet closed. we can do that
# since we have reached the end of the file
echo "G $begin $end $count" >> $WORKING_DIR/interval.sizes;
echo "G $begin $end $count"; #debug

grep G $WORKING_DIR/interval.sizes | awk '{print $4}' | sort -g > $WORKING_DIR/good.hist;
uniq -c $WORKING_DIR/good.hist > $WORKING_DIR/good.hist.count;
grep B $WORKING_DIR/interval.sizes | awk '{print $4}' | sort -g > $WORKING_DIR/bad.hist;
uniq -c $WORKING_DIR/bad.hist > $WORKING_DIR/bad.hist.count;


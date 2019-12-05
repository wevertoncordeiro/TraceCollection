#!/bin/bash

GROUND_TRUTH="0";
ORIGINAL="0";
CORRECTED="0";
WORKING_DIR="0";

while getopts hg:o:c:d: option; do
  case "${option}" in
    g) GROUND_TRUTH=${OPTARG};;
    o) ORIGINAL=${OPTARG};;
    c) CORRECTED=${OPTARG};;
    d) WORKING_DIR=${OPTARG};;
    h)
       echo "";
       echo "$0: options";
       echo " -g ground truth file, in snapshot format #peerid #window";
       echo " -o original file, in snapshot format #peerid #window";
       echo " -c corrected file, in snapshot format #peerid #window";
       echo " -d working dir, where stats file are written";
       echo "";
       exit 0;;
  esac;
done

test $ORIGINAL = "0" && { echo "-o: original file not specified."; exit 1; }
test $CORRECTED = "0" && { echo "-c: corrected file not specified."; exit 1; }
test $WORKING_DIR = "0" && { echo "-d: working_dir not specified."; exit 1; }

mkdir -p $WORKING_DIR && rm -rf $WORKING_DIR/* ;

#sort ${ORIGINAL} > $WORKING_DIR/`basename ${ORIGINAL}`.sort;
grep -v "#" ${ORIGINAL} | sort > $WORKING_DIR/`basename ${ORIGINAL}`.sort;

#sort ${CORRECTED} > $WORKING_DIR/`basename ${CORRECTED}`.sort;
grep -v "#" ${CORRECTED} | sort > $WORKING_DIR/`basename ${CORRECTED}`.sort;

ORIGINAL=$WORKING_DIR/`basename ${ORIGINAL}`.sort;
CORRECTED=$WORKING_DIR/`basename ${CORRECTED}`.sort;

comm -1 -3 ${ORIGINAL} ${CORRECTED} > $WORKING_DIR/modified.txt

mod=`wc -l $WORKING_DIR/modified.txt | cut -f1 -d ' '`;

if [ ${GROUND_TRUTH} != "0" ]; then
  #sort ${GROUND_TRUTH} > $WORKING_DIR/`basename ${GROUND_TRUTH}`.sort;
  grep -v "#" ${GROUND_TRUTH} | sort  > $WORKING_DIR/`basename ${GROUND_TRUTH}`.sort;
  
  GROUND_TRUTH=$WORKING_DIR/`basename ${GROUND_TRUTH}`.sort;

  comm -2 -3 ${GROUND_TRUTH} ${ORIGINAL} > $WORKING_DIR/missing.txt
  comm -1 -2 ${GROUND_TRUTH} $WORKING_DIR/modified.txt > $WORKING_DIR/true_mod.txt
  comm -1 -3 ${GROUND_TRUTH} $WORKING_DIR/modified.txt > $WORKING_DIR/false_mod.txt
  comm -2 -3 $WORKING_DIR/missing.txt $WORKING_DIR/modified.txt > $WORKING_DIR/false_neg.txt

  miss=`wc -l $WORKING_DIR/missing.txt | sed -e 's/^[[:space:]]*//' | cut -f1 -d ' '`;
  true_mod=`wc -l $WORKING_DIR/true_mod.txt | sed -e 's/^[[:space:]]*//' | cut -f1 -d ' '`;
  false_mod=`wc -l $WORKING_DIR/false_mod.txt | sed -e 's/^[[:space:]]*//' | cut -f1 -d ' '`;
  false_neg=`wc -l $WORKING_DIR/false_neg.txt | sed -e 's/^[[:space:]]*//' | cut -f1 -d ' '`;
fi;

echo "#miss #mod #true_mod #false_mod #false_neg" > $WORKING_DIR/log.txt;
echo $miss $mod $true_mod $false_mod $false_neg >> $WORKING_DIR/log.txt;

if [ ${GROUND_TRUTH} != "0" ]; then
  printf "corrected: %.2f%%\n" `echo 100*$true_mod/$miss | bc -l` >> $WORKING_DIR/log.txt;
  printf "true correct.: %.2f%%\n" `echo 100*$true_mod/$mod | bc -l` >> $WORKING_DIR/log.txt;
  printf "false correct.: %.2f%%\n" `echo 100*$false_mod/$mod | bc -l` >> $WORKING_DIR/log.txt;
  printf "not corrected: %.2f%%\n" `echo 100*$false_neg/$miss | bc -l` >> $WORKING_DIR/log.txt;
fi

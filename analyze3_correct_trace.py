#!/usr/bin/python
'''

'''
import sys, time, getopt, urllib, random, struct, commands, os, string, numpy
import subprocess

from analyze0_main import *


def run_script_correct_snapshot_failures(input_file_, output_file_, statistics_dir_, n_gap_=0):

	cmd = "./script_correct_snapshot_failures.sh "
	cmd += " -f %s" % input_file_
	cmd += " -o %s" % output_file_
	cmd += " -d %s" % statistics_dir_
	cmd += " -n %d" % n_gap_
	run_cmd(cmd, 1, True)


def run_program_failure_probability(confidence_, output_file_name_, path_):
	# "failure_probability --file-good good.hist.count --file-bad bad.hist.count --size-good $(wc -l good.hist | cut -f1) --size-bad $(wc -l bad.hist | cut -f1) --confidence 0.95 > failure_probability.log 2>&1

	try:
		size_good = int(commands.getoutput("cat %s/good.hist | wc -l " % path_))

	except Exception, e:
		print "Exception:", e
		print "size good error: %s " % size_good
		sys.exit(-1)

	try:
		size_bad = int(commands.getoutput("cat %s/bad.hist | wc -l " % path_))

	except Exception, e:
		print "Exception:", e
		print "size bad error: %s " % size_bad
		sys.exit(-1)

	print "\t size_good: %d size_bad: %d \n" % (size_good, size_bad)
	# sys.exit()

	cmd = "./failure_probability"
	cmd += " --file-good %s/%s " % (path_, GOOD_FILE_NAME)
	cmd += " --file-bad %s/%s " % (path_, BAD_FILE_NAME)
	cmd += " --size-good %d " % size_good
	cmd += " --size-bad %d " % size_bad
	cmd += " --confidence %s " % confidence_
	cmd += " > %s 2>&1" % output_file_name_
	run_cmd(cmd, 1, True, False)


def print_usage():
	print ""
	print "This script converts Tracker lens results from TRACE format (one peer per line) to: "
	print "   a) SNAPSHOT format (peerid window) - BASELINE "
	print "   b) SNAPSHOT format (peerid window) - CORRECTED according to a given alpha"
	print ""
	print "USAGE:"
	print "-h --help                          : show this usage help message"
	print "-i --in-trace               [file] : (i.e. *_TRACE.txt)"
	print "-s --out-original-snapshot  [file] : (i.e. *.snap)"
	print "-c --out-corrected-snapshot [file] : (i.e. *.snap)"
	print "-l --out-log                [file] : (i.e. failure_probability.log)"
	print "-a --alpha int (0..100)            : (default %d)" % DEFAULT_ALPHA
	print "-o --convert-original [true/false] : (default TRUE) make the first (a) conversion? "
	print ""


if __name__ == '__main__':

	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	# INITIALIZE VARIABLES
	in_trace_file_name = ""
	out_snap_orig_file_name = ""
	out_snap_cor_file_name = ""
	out_log_file_name = ""
	alpha = DEFAULT_ALPHA
	convert_original = True

	try:
		optlist, args = getopt.gnu_getopt(sys.argv[1:], 'hi:s:c:a:o:l:',
										  ['help', 'in-trace=', "out-original-snapshot=", "out-corrected-snapshot=",
										   'alpha=', 'convert-original=', 'out-log='])
		for o, a in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			elif o in ["-i", "--in-trace"]:
				in_trace_file_name = a

			elif o in ["-s", "--out-original-snapshot"]:
				out_snap_orig_file_name = a

			elif o in ["-c", "--out-corrected-snapshot"]:
				out_snap_cor_file_name = a

			elif o in ["-l", "--out-log"]:
				out_log_file_name = a

			elif o in ["-a", "--alpha"]:
				alpha = int(a)
				if alpha < 0 or alpha > 100:
					print "\n\n\nERROR: ALPHA (%d) MUST BE >= 0 and <=100\n\n\n" % alpha
					sys.exit(-1)

			if o in ["-o", "--convert-original"]:
				convert_original = str2bool(a)

	except Exception, e:
		print "Exception:", e
		print "Please, use -h or --help for instructions on how to use this script."
		sys.exit(-1)

	print ""
	print "ARGUMENTS"
	print "---------"
	print "\t-i --in-trace              :", in_trace_file_name
	print "\t-s --out-original-snapshot :", out_snap_orig_file_name
	print "\t-c --out-corrected-snapshot:", out_snap_cor_file_name
	print "\t-l --out-log               :", out_log_file_name
	print "\t-a --alpha=int (0..100)%   :", alpha
	print "\t-o --convert_original      :", convert_original
	print ""

	if in_trace_file_name == "" or out_snap_orig_file_name == "" or out_snap_cor_file_name == "":
		print "Input file or original snap file or corrected snap file is null."
		print "Please, use -h or --help for instructions on how to use this script."
		sys.exit(-1)

	print ""
	print "MAKING DIRS"
	print "-----------"
	out_snap_orig_dir = Dirs().statistics_original
	out_snap_cor_dir = Dirs().statistics_corrected
	for d in [out_snap_orig_dir, out_snap_cor_dir]:
		cmd = "mkdir -p " + d
		run_cmd(cmd, 1, True)

	script_root = os.path.basename(__file__).split(".")[0]

	if out_log_file_name == "":
		out_log_file_name = Dirs.statistics_corrected + os.path.basename(out_snap_cor_file_name) + ".failure_probability.log"

	GOOD_FILE_NAME = "good.hist.count"
	BAD_FILE_NAME = "bad.hist.count"

	print ""
	print "SETTINGS"
	print "--------"
	print "\tout_snap_orig_dir :", out_snap_orig_dir
	print "\tout_snap_cor_dir  :", out_snap_cor_dir
	print "\tout_log_file_name :", out_log_file_name
	print "\tGOOD_FILE_NAME    : %s%s" % (out_snap_orig_dir, GOOD_FILE_NAME)
	print "\tBAD_FILE_NAME     : %s%s" % (out_snap_orig_dir, BAD_FILE_NAME)
	print ""

	print "PRE PROCESSING..."
	print "-----------------"

	number_of_cycles_for_considering_gap_as_failure = 1

	monitoring_start_epoch = get_start_monitoring_epoch()

	if convert_original:
		# converting original
		cmd = "./script_convert_trace_to_snapshot.sh -f %s -o %s" % (in_trace_file_name, out_snap_orig_file_name)
		run_cmd(cmd, 1, True)

		run_script_correct_snapshot_failures(out_snap_orig_file_name, out_snap_cor_file_name, out_snap_orig_dir, 0)

		cmd = "mv %s %s " % (GOOD_FILE_NAME, out_snap_orig_dir)
		run_cmd(cmd, True, 1)

		cmd = "mv %s %s " % (BAD_FILE_NAME, out_snap_orig_dir)
		run_cmd(cmd, True, 1)

	else:
		print "\t conversion of the original file skipped"

	print "CORRECTING..."
	print "-------------"

	confidence = (alpha / 100.0)  # e.g. 0.95

	# try to correct the trace
	run_program_failure_probability(confidence, out_log_file_name, out_snap_orig_dir)

	# obtaining results
	failure_probability = commands.getoutput("tail -n 1 %s | awk '{print $1}'" % out_log_file_name)

	gap = get_number_of_cycles_for_considering_gap_as_failure(out_log_file_name, 1)

	if gap is not None:
		# correct the trace
		run_script_correct_snapshot_failures(out_snap_orig_file_name, out_snap_cor_file_name, out_snap_cor_dir, gap)

	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""
#!/usr/bin/python

import sys, time, getopt, commands, os, string, numpy, datetime
import subprocess
# import bisect

from colorama import Fore, Back, Style, init

from analyze0_main import *

init(autoreset=True)

class Session:

	def __init__(self, line_):
		self.begin = line_.session_begin
		self.end = line_.session_end


class Peer:

	def __init__(self, line_):
		self.line = line_
		self.id = line_.peer_id
		self.sessions = []
		self.sessions.append(Session(line_))


class Line:

	def __init__(self, line_):
		try:
			if line_ is None:
				self.peer_id = -1
			else:
				self.line = line_.split("\n")[0]
				ls = self.line.split("|")
				self.peer_id = int(ls[0])
				self.session_begin = int(ls[1])
				self.session_end = int(ls[2])

		except Exception, e:
			print "Exception:%s line:%s" % (e, line_)


def print_usage():
	print "Compares ground truth, original and corrected files "
	print " files must be in SNAPSHOT format (peerId window)"
	print ""
	print "USAGE: %s [OPTIONS] " % os.path.basename(__file__)
	print "-h --help           : show this usage help message"
	print "-d --debug          : debug information "
	print "-e --less=N         : debug=On and pauses after N lines (for debug purposes) "
	print "-k --check          : check results with a different methodology "
	print ""
	print "-g --ground=file    : SNAPSHOT FORMAT "
	print "-r --original=file  : SNAPSHOT FORMAT "
	print "-c --corrected=file : SNAPSHOT FORMAT "
	print "-o --output=file    : ANALYSIS FORMAT "
	print "-l --log=file       : LOG FORMAT "
	print "-m --omit-pif       : omit probability of injected fail in table "
	print "-a --last           : last alpha item in table "



def print_debug(msg_, end_=False):
	global debug

	color_msg = msg_
	# print "msg: '%s'" % msg_ # debug

	if "[G!=O] [G!=C] [O!=C]" in msg_:
		color_msg = Fore.CYAN + msg_ + Fore.RESET

	elif "!=" in msg_ or "==" in msg_:
		color_msg = "\t"
		msg_split = msg_.split(" ")
		for token in msg_split:
			if "\t" in token:
				token = token.split("\t")[1]

			#print "token: '%s'" % token # debug
			if token == "[G!=O]":
				color_msg += Fore.YELLOW
			elif token == "[G!=C]":
				color_msg += Fore.RED
			elif token == "[G==C]" and msg_ != "\t[G==O] [G==C] [O==C]":
				color_msg += Fore.GREEN
			elif token == "[O!=C]":
				color_msg += Fore.MAGENTA
			else:
				color_msg += Fore.RESET

			color_msg += token

	if debug:
		if end_:
			print color_msg
		else:
			print color_msg,


def format_number(number_):
	#print number_ , # debug
	r = str(number_)
	if number_ > 1000:
		r = "%dk" % (number_/1000)

	#print r # debug
	return r


def read_line(file_):
	try:
		line = file_.readline()
		if line:
			while line[0] == "#":
				line = file_.readline()

			return line.split("\n")[0]
		else:
			return None

	except EOFError as error:
		# one file can be smaller than the others and raise this error
		return None


if __name__ == '__main__':

	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	# INITIALIZE VARIABLES
	debug = False
	check = False

	file_snapshot_ground_truth = None
	file_snapshot_original = None
	file_snapshot_corrected = None
	file_name_output = None
	alpha = None
	failure_probability = None
	omit_pif = False
	last_alpha = False
	out_log_file_name = None
	less_n = 0

	try:
		optlist, args = getopt.gnu_getopt(sys.argv[1:], 'hdmakg:r:c:o:l:e:',
										  ['help', 'debug', 'omit-pif', 'last-alpha', 'check',
										   'ground=', 'original=', 'corrected=', 'output=', 'log=', 'less='])

		for o, a in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			elif o in ["-d", "--debug"]:
				debug = True

			elif o in ["-m", '--omit-pif']:
				omit_pif = True

			elif o in ["-a", '--last-alpha']:
				last_alpha = True

			elif o in ["-k", '--check']:
				check = True

			elif o in ["-g", '--ground']:
				file_snapshot_ground_truth = a

			elif o in ["-r", '--original']:
				file_snapshot_original = a

			elif o in ["-c", '--corrected']:
				file_snapshot_corrected = a

			elif o in ["-o", '--output']:
				file_name_output = a

			elif o in ["-l", '--log']:
				out_log_file_name = a

			elif o in ["-e", "--less"]:
				less_n = int(a)
				debug = True
				if less_n < 0:
					raise ValueError('-e= --less= < 0.')

	except Exception, e:
		print "Exception:", e
		print "Please, use option -h or --help for instructions."
		sys.exit(-1)

	if file_snapshot_ground_truth is None:
		print "ERROR: file_snapshot_ground_truth is None "
		sys.exit(-1)

	if file_snapshot_original is None:
		print "ERROR: file_snapshot_original is None "
		sys.exit(-1)

	if file_snapshot_corrected is None:
		print "ERROR: file_snapshot_corrected is None "
		sys.exit(-1)

	if file_name_output is None:
		print "ERROR: file_name_output is None"
		sys.exit(-1)

	print "\nOPTIONS:"
	print "-------------"
	print "\tdebug        :", debug
	print "\tcheck        :", check
	print ""
	print "\tground_truth :", file_snapshot_ground_truth,
	if os.path.isfile(file_snapshot_ground_truth):
		print " [OK]"
	else:
		print "file not found!"
		sys.exit(-1)

	print "\toriginal     :", file_snapshot_original,
	if os.path.isfile(file_snapshot_original):
		print " [OK]"
	else:
		print "file not found!"
		sys.exit(-1)

	print "\tcorrected    :", file_snapshot_corrected,
	if os.path.isfile(file_snapshot_corrected):
		print " [OK]"

	else:
		print "file not found! Probably, file could not be corrected. "

		file_out = open(file_name_output, 'a')
		file_out.write("%d %d [FAILED: FILE NOT FOUND]\n" % (failure_probability, alpha))

		out = " \\omite{*%d*} " % alpha

		if omit_pif:
			out += " \\omite{pif=%.02f} " % (failure_probability / 100.0)
		else:
			out += "&     \\setf{%.02f} " % (failure_probability / 100.0)

		if last_alpha:
			out += "& \\setf{--} & \\multicolumn{4}{c}{\\setf{Not corrected}} \\\\"
		else:
			out += "& \\setf{--} & \\multicolumn{4}{c||}{\\setf{Not corrected}}  "

		out += "\n"
		file_out.write(out)
		file_out.close()
		sys.exit(0)

	print ""

	#file_name_output = dir_data + file_name_output
	print "\toutput       :", file_name_output
	print "\tlog_file_name:", out_log_file_name
	print "\tomit-omit_pif:", omit_pif
	print "\tlast_alpha   :", last_alpha

	try:
		alpha = int(file_snapshot_corrected.split("ALP-")[1].split(".")[0])
		print "\talpha        :", alpha

	except Exception, e:
		print "[EXCEPTION] while deducing alpha from file_snapshot_corrected: ", e
		print " file_snapshot_corrected:",
		print ' formula: int(file_snapshot_corrected.split("ALP-")[1].split(".")[0])'
		print ""
		sys.exit(-1)

	try:
		failure_probability = int(file_snapshot_corrected.split("FAIL-")[1].split("_")[0])
		print "\tfailure_prob.:", failure_probability
	except Exception, e:
		print "[EXCEPTION] while deducing failure_probability from file_snapshot_corrected: ", e
		print " file_snapshot_corrected:",
		print ' formula: int(file_snapshot_corrected.split("FAIL-")[1].split("-")[0])'
		print ""
		sys.exit(-1)

	print ""
	count_ground_truth_snapshots = 0
	count_missing_positive_snapshots = 0
	count_modified_snapshots = 0
	count_modified_snapshots_accurately = 0
	count_modified_snapshots_inaccurately = 0
	count_false_negative = 0
	count_true_negative = 0

	exception = False
	out = "\n"
	if debug or check:

		out = "\n\n\n#######################\n"
		file_ground = open(file_snapshot_ground_truth, 'r')
		file_original = open(file_snapshot_original, 'r')
		file_corrected = open(file_snapshot_corrected, 'r')

		line_original_n = read_line(file_original)
		line_corrected_n = read_line(file_corrected)
		line_ground_n = read_line(file_ground)

		snaps = 0
		modified_snaps = 0
		missing_snaps = 0
		true_positives = 0
		false_positives = 0
		true_negatives = 0
		false_negatives = 0

		peer = None
		lines = 0
		problems = 0
		try:

			while True:

				count_ground_truth_snapshots += 1
				if line_ground_n is None and line_original_n is None and line_corrected_n is None:
					# only ends when all files are at end
					break

				if line_ground_n is not None and peer != int(line_ground_n.split(" ")[0]):
					peer = int(line_ground_n.split(" ")[0])
					print_debug("+-------------------", True)
					print_debug(" PEER %d" % peer, True)


				if line_ground_n is not None and line_original_n is not None and line_corrected_n is not None:
					print_debug("p:%d g:%s o:%s c:%s " % (peer, line_ground_n.split(" ")[1], line_original_n.split(" ")[1], line_corrected_n.split(" ")[1]))
				else:
					print_debug(" some file ended.")

				if line_ground_n == line_original_n and line_ground_n == line_corrected_n and line_original_n == line_corrected_n:
					print_debug("\t[G==O] [G==C] [O==C]")

					line_ground_n = read_line(file_ground)
					line_original_n = read_line(file_original)
					line_corrected_n = read_line(file_corrected)

					snaps += 1
					# modified_snaps += 1
					# missing_snaps += 1
					# true_positives += 1
					# false_positives += 1
					true_negatives += 1
					# false_negatives += 1

				elif line_ground_n == line_original_n and line_ground_n == line_corrected_n and line_original_n != line_corrected_n:
					print_debug("\t[G==O] [G==C] [O!=C]")
					print "[ERROR]"
					sys.exit(-1)

				elif line_ground_n == line_original_n and line_ground_n != line_corrected_n and line_original_n == line_corrected_n:
					print_debug("\t[G==O] [G!=C] [O==C]")
					print "[ERROR]"
					sys.exit(-1)

				elif line_ground_n == line_original_n and line_ground_n != line_corrected_n and line_original_n != line_corrected_n:
					print_debug("\t[G==O] [G!=C] [O!=C]")

					# line_ground_n = read_line(file_ground_n)
					# line_original_n = read_line(file_original_n)
					line_corrected_n = read_line(file_corrected)

					# snaps += 1
					modified_snaps += 1
					# missing_snaps += 1
					# true_positives += 1
					false_positives += 1
					# true_negatives += 1
					# false_negatives += 1

				elif line_ground_n != line_original_n and line_ground_n == line_corrected_n and line_original_n == line_corrected_n:
					print_debug("\t[G!=O] [G==C] [O==C]")
					print "[ERROR]"
					sys.exit(-1)

				elif line_ground_n != line_original_n and line_ground_n == line_corrected_n and line_original_n != line_corrected_n:
					print_debug("\t[G!=O] [G==C] [O!=C]")

					line_ground_n = read_line(file_ground)
					# line_original_n = read_line(file_original_n)
					line_corrected_n = read_line(file_corrected)

					snaps += 1
					modified_snaps += 1
					missing_snaps += 1
					true_positives += 1
					# false_positives += 1
					# true_negatives += 1
					# false_negatives += 1

				elif line_ground_n != line_original_n and line_ground_n != line_corrected_n and line_original_n == line_corrected_n:
					print_debug("\t[G!=O] [G!=C] [O==C]")

					line_ground_n = read_line(file_ground)
					# line_original_n = read_line(file_original_n)
					# line_corrected_n = read_line(file_corrected_n)

					snaps += 1
					# modified_snaps += 1
					missing_snaps += 1
					# true_positives += 1
					# false_positives += 1
					# true_negatives += 1
					false_negatives += 1

				elif line_ground_n != line_original_n and line_ground_n != line_corrected_n and line_original_n != line_corrected_n:
					print_debug("\t[G!=O] [G!=C] [O!=C]")

					# THIS IS A PARTICULAR CASE!
					# either ground truth or corrected trace can be ahead of the other:
					#  a) ground truth may have a snapshot that was not corrected (i.e. false negative)
					#  b) corrected may have a snapshot that was not in the original (i.e. false positive)
					#  c) original cannot be ahead since it can only have dropped line
					# Therefore, we must decide what is the case (a) or (b) so we can make the right move.

					peer_ground = -1
					peer_corrected = -1
					snap_ground = -1
					snap_corrected = -1

					if line_ground_n is not None:
						peer_ground = int(line_ground_n.split(" ")[0])
						snap_ground = int(line_ground_n.split(" ")[1])

					if line_corrected_n is not None:
						peer_corrected = int(line_corrected_n.split(" ")[0])
						snap_corrected = int(line_corrected_n.split(" ")[1])

					if (peer_ground > peer_corrected) or (snap_ground > snap_corrected):
						print_debug("peer_ground (%d) > peer_corrected  (%d) or snap_ground (%d) > snap_corrected (%d)" % (
							peer_ground, peer_corrected, snap_ground, snap_corrected), True)
						# Corrected trace is behind (and ground truth is ahead)!
						# e.g. p:9 g:58 o:59 c:57

						# thus, we will move forward the corrected trace

						# line_ground_n = read_line(file_ground_n)
						# line_original_n = read_line(file_original_n)
						line_corrected_n = read_line(file_corrected)

						# and update statistics
						# snaps += 1
						modified_snaps += 1
						# missing_snaps += 1
						# true_positives += 1
						false_positives += 1
						# true_negatives += 1
						# false_negatives += 1

					else:
						print_debug("[NOT] peer_ground (%d) > peer_corrected  (%d) or snap_ground (%d) > snap_corrected (%d)" % (
							peer_ground, peer_corrected, snap_ground, snap_corrected), True)

						# Ground truth is behind (and corrected is ahead)!
						# e.g. p:1 g:0 o:2 c:1

						# thus, we will move forward the ground truth trace
						line_ground_n = read_line(file_ground)
						# line_original_n = read_line(file_original_n)
						# line_corrected_n = read_line(file_corrected_n)

						# and update statistics
						snaps += 1
						# modified_snaps += 1
						missing_snaps += 1
						# true_positives += 1
						# false_positives += 1
						# true_negatives += 1
						false_negatives += 1

				else:
					print_debug("\t[G??O] [G??C] [O??C]")
					print "[ERROR][An unexpected case occurred]"
					sys.exit(-1)

				msg = "snap:%d missing:%d modified:%d true_pos:%d false_pos:%d true_neg:%d false_neg:%d" % (
					snaps, missing_snaps, modified_snaps, true_positives, false_positives, true_negatives, false_negatives)
				print_debug(msg, True)

				lines += 1

				if less_n > 0 and lines == less_n:
					print ""
					raw_input("Press Enter to continue...")
					print ""
					lines = 0

		except Exception, e:
			print "Exception: ", e
			exception = True

		file_ground.close()
		file_original.close()
		file_corrected.close()

		cmd = " ./script_snapshot_analysis_summary.sh"
		cmd += " -g %s" % file_snapshot_ground_truth
		cmd += " -o %s" % file_snapshot_original
		cmd += " -c %s" % file_snapshot_corrected
		cmd += " -d %s/test/" % dir_analysis
		run_cmd(cmd, 2, True)

		cmd = "cat %s/test/log.txt  " % dir_analysis

		print " cmd: ", cmd
		check_results = commands.getoutput(cmd).split("\n")[1]

		print "check_results:", check_results
		out += "\ncheck_results: %s\n" % check_results

		value = int(check_results.split(" ")[0])
		print "miss     : %d %d" % (missing_snaps, value),
		out += "miss     : %d %d" % (missing_snaps, value)
		if missing_snaps == value:
			print "[OK]"
			out += "[OK]\n"
		else:
			print "[ERROR]"
			out += "[ERROR]\n"

		value = int(check_results.split(" ")[1])
		print "mod      : %d %d" % (modified_snaps, value),
		out += "mod      : %d %d" % (modified_snaps, value)
		if modified_snaps == value:
			print "[OK]"
			out += "[OK]\n"
		else:
			print "[ERROR]"
			out += "[ERROR]\n"

		value = int(check_results.split(" ")[2])
		print "true_mod : %d %d" % (true_positives, value),
		out += "true_mod : %d %d" % (true_positives, value)
		if true_positives == value:
			print "[OK]"
			out += "[OK]\n"
		else:
			print "[ERROR]"
			out += "[ERROR]\n"

		value = int(check_results.split(" ")[3])
		print "false_mod: %d %d" % (false_positives, value),
		out += "false_mod: %d %d" % (false_positives, value)
		if false_positives == value:
			print "[OK]"
			out += "[OK]\n"
		else:
			print "[ERROR]"
			out += "[ERROR]\n"

		value = int(check_results.split(" ")[4])
		print "false_neg: %d %d" % (false_negatives, value),
		out += "false_neg: %d %d" % (false_negatives, value)
		if false_negatives == value:
			print "[OK]"
			out += "[OK]\n"
		else:
			print "[ERROR]"
			out += "[ERROR]\n"
		out += "\n"

	else:
		cmd = " ./script_snapshot_analysis_summary.sh"
		cmd += " -g %s" % file_snapshot_ground_truth
		cmd += " -o %s" % file_snapshot_original
		cmd += " -c %s" % file_snapshot_corrected
		cmd += " -d %s/test/" % dir_analysis
		run_cmd(cmd, 2, True)

		cmd = "cat %s/test/log.txt  " % dir_analysis
		print ""
		print " cmd: ", cmd
		check_results = commands.getoutput(cmd).split("\n")[1]
		print "check_results:", check_results

		# PROCESSING

		missing_snaps = int(check_results.split(" ")[0])
		print "miss     : %d  " % missing_snaps

		modified_snaps = int(check_results.split(" ")[1])
		print "mod      : %d  " % modified_snaps

		true_positives = int(check_results.split(" ")[2])
		print "true_mod : %d  " % true_positives

		false_positives = int(check_results.split(" ")[3])
		print "false_mod: %d  " % false_positives

		false_negatives = int(check_results.split(" ")[4])
		print "false_neg: %d  " % false_negatives

	if not os.path.isfile(file_name_output):
		print "FILE NOT FOUND: ", file_name_output
		print "CREATING A NEW ONE...."
		print ""
		out += " #1-failure_prob"			    #1
		out += " #2-alpha"						#2
		out += " #3-snapshots" 					#3
		out += " #4-missing"					#4
		out += " #5-modified"					#5
		out += " #6-modified_true_positive"		#6
		out += " #7-modified_false_positive"	#7
		out += " #8-unmodified_false_negative"	#8
		out += " #9-unmodified_true_negative"	#9
		out += " #10-groundtruth"				#10
		out += " #11-original"					#11
		out += " #12-corrected"					#12
		out += "\n"

	out += "%d" % failure_probability						#1
	out += " %d" % alpha									#2
	out += " %d" % count_ground_truth_snapshots				#3
	out += " %d" % count_missing_positive_snapshots			#4
	out += " %d" % count_modified_snapshots					#5
	out += " %d" % count_modified_snapshots_accurately		#6
	out += " %d" % count_modified_snapshots_inaccurately	#7
	out += " %d" % count_false_negative						#8
	out += " %d" % count_true_negative						#9
	out += " %s" % file_snapshot_ground_truth				#10
	out += " %s" % file_snapshot_original					#11
	out += " %s" % file_snapshot_corrected					#12
	out += "\n\n"

	# Data for Table 2
	out += " \\omite{*%d*} " % alpha

	if omit_pif:
		out += " \\omite{pif=%.02f} " % (failure_probability / 100.0)
	else:
		out += "&     \\setf{%.02f} " % (failure_probability / 100.0)

	gap = None
	if out_log_file_name is not None:
		gap = get_number_of_cycles_for_considering_gap_as_failure(out_log_file_name)

	if gap is None:
		out += "& \\setf{--} &"
	else:
		out += "& \\setf{%d} &" % gap

	a = true_positives
	b = missing_snaps
	out += "$\\sfrac{%s}{%s}$ " % (format_number(a), format_number(b))
	if b > 0:
		c = 1.0 * a/b
		out += "& \\setf{%.02f} &" % c
	else:
		out += "& \\setf{--} &"

	a = false_positives
	b = modified_snaps
	out += "$\\sfrac{%s}{%s}$ " % (format_number(a), format_number(b))
	if b > 0:
		c = 1.0 * a / b
		out += "& \\setf{%.02f} " % c
	else:
		out += "& \\setf{--} "

	if last_alpha:
		out += "\\\\"

	# this metric currently isn't exhibited in Table 2
	# a = false_negatives
	# b = missing_snaps
	# if b > 0:
	# 	c = 1.0 * a / b
	# 	out += " $\\sfrac{%d}{%d}$ & \\setf{%.02f} &" % (a, b, c)
	# else:
	# 	out += " $\\sfrac{%d}{%d}$ & \\setf{--} &" % (a, b)

	out += "\n\n"
	file_out = open(file_name_output, 'a+')
	file_out.write(out)
	file_out.close()

	print ""
	print "out:", out

	print ""
	if exception:
		print "[EXCEPTION]", now_str(), __file__,
		print ""
		print ""
		sys.exit(-1)

	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""



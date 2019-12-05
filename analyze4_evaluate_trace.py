#!/usr/bin/python
'''

'''
import sys, time, getopt, commands, os, string, numpy, datetime
import subprocess
# import bisect

from analyze0_main import *

results = {}

# http://gnuplot.sourceforge.net/docs_4.2/node192.html
KEY_ON_INSIDE = "set key on inside right bottom"
KEY_ON_OUTSIDE = "set key on outside center top "
KEY = KEY_ON_OUTSIDE

PREFIX_CDF = "cdf_"
PREFIX_HIST = "hist_"


class Analysis:

	def __init__(self, file_name_):
		self.fileName = file_name_

		self.arrivals = {}
		self.interArrivals = []
		self.sessions_count = {}
		self.duration = {}
		self.sessions_length = []

	def print_arrivals_count(self):

		if debug:
			print "\t\t# ArrivalsCount data (time: count):", self.arrivals

		# s = ""
		# for t in sorted(self.arrivals):
		#     #print "%session_line|%d"%(session_begin, self.arrivals[session_begin])
		#     s += "%d:%d, "%(t, self.arrivals[t])
		# print "\t\t# Arrivals Data (time: count):",  s

		print "\t\t# Arrivals Count:", sum(self.arrivals.values()), " In different-Times:", len(self.arrivals.keys())
		print ""

	def print_inter_arrivals(self):

		if debug:
			print "\t\t# Inter-arrivals Data (session_time_x - session_time_x-1):", self.interArrivals
		# print "\t\t# Inter-arrivals Data (session_time_x - session_time_x-1):", self.interArrivals
		print "\t\t# Inter-arrivals Count:", len(self.interArrivals), " Mean:", numpy.mean(self.interArrivals)
		print ""

	def print_sessions_count(self):

		v = self.sessions_count.values()
		if debug:
			print "\t\t\t# sessions_count   keys:", self.sessions_count.keys()
			print "\t\t\t# sessions_count values:", v

		print "\t\t# sessions_count \tCount:", len(v), "peers \tSum:", sum(v), "sessions\tMean: %0.02f " % numpy.mean(
			v), "\tStd.Dev.: %0.02f" % numpy.std(v), "Median: ", numpy.median(v),
		print ""

	def print_sessions_length(self):

		if debug:
			print "\t\t\t# Duration Data (peer: [time_in, time_out, time_diff] ):", self.duration

		s = ""
		for t in sorted(self.duration):
			# print "%session_line|%d"%(session_begin, self.arrivals[session_begin])
			s += "%s:%s, " % (t, self.duration[t])

		if debug:
			print "\t\t\t# sessions_length  (session:[in, out, diff] ): ", s

		for d in self.duration:
			# print d
			self.sessions_length.append(self.duration[d][2])
		if debug:
			print "\t\t\t# sessions_length (sorted([diff])):", sorted(self.sessions_length)

		print "\t\t# sessions_length \tCount:", len(self.sessions_length), "sessions \tSum:", sum(
			self.sessions_length), "windows\tMean: %0.02f" % numpy.mean(
			self.sessions_length), "\tStd.Dev.: %0.02f" % numpy.std(self.sessions_length), "Median: ", numpy.median(
			self.sessions_length),

	def get_curve_file_name(self):

		curve_file_name = os.path.basename(self.fileName).replace(".txt", "")
		# curveTitle = curveTitle.replace("_CORRECTED", "_C")
		# curveTitle = curveTitle.replace("_CORRECTED", "_C")
		return curve_file_name

	def get_curve_nick(self):

		curve_nick = os.path.basename(self.fileName)
		# if "_SESSION" in curve_nick:
		#     curve_nick = curve_nick.replace("_SESSION", "_ORIGINAL")
		#     curve_nick = curve_nick.replace("_RES-100", "")

		curve_nick = curve_nick.replace("_SESSION", "_BASELINE")
		# curve_nick = curve_nick.replace("_CORRECTED", "")
		curve_nick = curve_nick.replace("_.", ".")
		curve_nick = curve_nick.replace("_", "\_")

		return curve_nick

	# prefixes for types of data
	def get_session_count_prefix(self):
		return "session_count"

	def get_session_length_prefix(self):
		return "session_length"

	# prefixes for types of plot
	def get_cdf_file_name(self, type_):
		return dir_data + type_ + "cdf_%s.txt" % self.get_curve_file_name()

	def get_hist_file_name(self, type_):
		return dir_data + type_ + "hist_%s.txt" % self.get_curve_file_name()

	# session count file names
	def get_cdf_session_count_file_name(self):
		return self.get_cdf_file_name(self.get_session_count_prefix())

	def get_hist_session_count_file_name(self):
		return self.get_hist_file_name(self.get_session_count_prefix())

	# session length file names
	def get_cdf_session_length_file_name(self):
		return self.get_cdf_file_name(self.get_session_length_prefix())

	def get_hist_session_length_file_name(self):
		return self.get_hist_file_name(self.get_session_length_prefix())

	def process_sessions_count(self):
		print "\t\t\tSESSIONS COUNT"
		print "\t\t\t--------------"
		f_cdf = open(self.get_cdf_session_count_file_name(), 'w')
		cdf_header = "#cdf\t\t#count\t#accum\t#count\t#total"
		f_cdf.write(cdf_header+"\n")
		print "\t\t\t", cdf_header

		f_hist = open(self.get_hist_session_count_file_name(), 'w')
		f_hist.write("#session_count\n")

		values = self.sessions_count.values()
		value_accum = 0
		total = sum(values) * 1.0
		value = sorted(values)[0]
		value_count = 0
		for d in sorted(values):
			# print " d: ", d # debug
			if d != value:
				value_accum += (value_count * value)
				cdf = value_accum / total
				line = "%f\t%d\t%d\t%d\t%d\n" % (cdf, value, value_accum, value_count, total)
				print "\t\t\t", line,  # debug
				f_cdf.write(line)

				# histogram
				hist = "%d\n" % value
				f_hist.write(hist * value_count)

				value = d
				value_count = 0

			value_count += 1

		value_accum += (value_count * value)
		cdf = value_accum / total
		line = "%f\t%d\t%d\t%d\t%d\n" % (cdf, value, value_accum, value_count, total)
		f_cdf.write(line)
		print "\t\t\t", line  # debug

		hist = "%d\n" % value
		f_hist.write(hist * value_count)

		f_cdf.close()
		f_hist.close()

		values = self.sessions_count.values()
		value_accum = 0
		total = len(values) * 1.0
		value = sorted(values)[0]
		value_count = 0
		print "\t\t\t", cdf_header, " OLD"
		for d in sorted(values):
			# print " d: ", d # debug
			if d != value:
				value_accum += value_count
				cdf = value_accum / total
				line = "%f\t%d\t%d\t%d\t%d\n" % (cdf, value, value_accum, value_count, total)
				print "\t\t\t", line,  # debug
				value = d
				value_count = 0

			value_count += 1
		value_accum += (value_count*value)
		cdf = value_accum / total
		line = "%f\t%d\t%d\t%d\t%d\n" % (cdf, value, value_accum, value_count, total)
		print "\t\t\t", line  # debug

	def process_session_length(self):
		print "\t\t\tSESSIONS LENGTH"
		print "\t\t\t---------------"

		f_cdf = open(self.get_cdf_session_length_file_name(), 'w')
		cdf_header = "#cdf\t\t#length\t#accum\t#count\t#total"
		f_cdf.write(cdf_header+"\n")
		print "\t\t\t", cdf_header

		f_hist = open(self.get_hist_session_length_file_name(), 'w')
		f_hist.write("#session_length\n")
		value_accum = 0
		total = len(self.sessions_length) * 1.0
		# print self.sessions_length

		value = sorted(self.sessions_length)[0]
		value_count = 0
		for d in sorted(self.sessions_length):

			if d != value:
				value_accum += value_count
				cdf = value_accum / total
				line = "%f\t%d\t%d\t%d\t%d" % (cdf, value, value_accum, value_count, total)
				f_cdf.write(line+"\n")
				print "\t\t\t", line  # debug

				hist = "%d\n" % value
				f_hist.write(hist * value_count)

				value = d
				value_count = 0

			value_count += 1

		value_accum += value_count
		cdf = value_accum / total
		line = "%f\t%d\t%d\t%d\t%d\n" % (cdf, value, value_accum, value_count, total)
		f_cdf.write(line)
		print "\t\t\t", line  # debug

		hist = "%d\n" % value
		f_hist.write(hist * value_count * 15)
		f_cdf.close()
		f_hist.close()


def get_file_base_name():
	if output_file_name_prefix is None:
		return os.path.basename(__file__).split(".")[0]
	else:
		return "%s_" % (output_file_name_prefix)


def get_file_session_length():
	return get_file_base_name() + "sessionLength"


def get_file_session_count():
	return get_file_base_name() + "sessionCount"


def get_file_session_count_plot(prefix_):
	return dir_plot + prefix_ + get_file_session_count() + ".plot"


def get_file_session_count_eps(prefix_):
	return dir_eps + prefix_ + get_file_session_count() + ".eps"


def get_file_session_count_png(prefix_):
	return get_file_session_count_eps(prefix_).replace(".eps", ".png")


def get_file_session_length_plot(prefix_):
	return dir_plot + prefix_ + get_file_session_length() + ".plot"


def get_file_session_length_eps(prefix_):
	return dir_eps + prefix_ + get_file_session_length() + ".eps"


def get_file_session_length_png(prefix_):
	return get_file_session_length_eps(prefix_).replace(".eps", ".png")


def plot_cdf_session_length(results_):
	cmd = "plot "

	for result in sorted(results_):
		analysis = results_[result]
		analysis.process_session_length()
		cmd += " '%s' using 2:1 title '%s' with lp ," % (analysis.get_cdf_session_length_file_name(),
														 analysis.get_curve_nick())
	plot = plot_header()
	plot += '''
unset grid
unset key
set xlabel "Duration of users' sessions"
set ylabel "CDF"

#set yrange [0:2000] #janela de 50
#set xrange [0:10] #janela de 300

set term postscript eps enhanced color "Helvetica" 24 lw 2
set output "%s"

%s
%s 
		''' % (get_file_session_length_eps(PREFIX_CDF), KEY, cmd)
	plot += '\nset output "%s"' % get_file_session_length_png(PREFIX_CDF)
	plot += '\nset term png'
	plot += '\nreplot'

	# WRITE FILE
	plot_file_name = get_file_session_length_plot(PREFIX_CDF)
	f_plot = open(plot_file_name, 'w')
	f_plot.write(plot)
	f_plot.close()

	# PLOT
	run_cmd("gnuplot %s" % plot_file_name, True, 2)


def plot_hist_session_length(results_):
	cmd = "plot "

	for result in sorted(results_):
		analysis = results_[result]
		# analysis.process_session_length()
		cmd += " '%s' using (bin($1,binwidth)):(1.0) title '%s' smooth freq with boxes ," % (
		analysis.get_hist_session_length_file_name(),
		analysis.get_curve_nick())

	#        cmd = cmd[0: len(cmd) -1]
	plot = plot_header()
	plot += '''
set term postscript eps enhanced color "Helvetica" 24 lw 2
unset grid
unset key
set xlabel "Duration of users' sessions"
set ylabel "Histogram"
set output "%s"
set yrange [.5:] #janela de 50
set xrange [0:100] #janela de 300

binwidth=3 #1/2 day, since 1 day (1440min) contains 96 snapshots of 15 minutes each
bin(x,width)=width*floor(x/width)

#plot 'datafile' using (bin($1,binwidth)):(1.0) smooth freq with boxes

%s
%s 
		''' % (get_file_session_length_eps(PREFIX_HIST), KEY, cmd)

	# WRITE FILE
	plot_file_name = get_file_session_length_plot(PREFIX_HIST)
	f_plot = open(plot_file_name, 'w')
	f_plot.write(plot)
	f_plot.close()

	# PLOT
	run_cmd("gnuplot %s" % plot_file_name, True, 1)


def plot_header():
	return "# File generated by %s on %s" % (os.path.basename(__file__), datetime.datetime.now())


def plot_cdf_session_count(results_):
	# PLOT COMMAND
	cmd = "plot "

	for result in sorted(results_):
		analysis = results_[result]
		analysis.process_sessions_count()  # creates file with data
		cmd += " '%s' using 2:1 title '%s' with lp ," % (analysis.get_cdf_session_count_file_name(),
														 analysis.get_curve_nick())
	# PLOT SETTINGS
	plot = plot_header()
	plot += '''
unset grid
unset key
set xlabel "Number of users' sessions"
set ylabel "CDF"

set yrange [.8:] #janela de 50
set xrange [0:100] #janela de 300

set term postscript eps enhanced color "Helvetica" 24 lw 2
set output "%s"

%s
%s 
		''' % (get_file_session_count_eps(PREFIX_CDF), KEY, cmd)
	plot += '\nset output "%s"' % get_file_session_count_png(PREFIX_CDF)
	plot += '\nset term png'
	plot += '\nreplot'

	# WRITE FILE
	plot_file_name = get_file_session_count_plot(PREFIX_CDF)
	f_plot = open(plot_file_name, 'w')
	f_plot.write(plot)
	f_plot.close()

	# PLOT
	run_cmd("gnuplot %s" % plot_file_name, True, 1)

def process_line(line_):
	return int(line_.split(" ")[0]), int(line_.split(" ")[1].split("\n")[0])


def print_usage():
	print "A tool for analysis of monitoring original/corrected results "
	print " files with results must be in the SESSION FORMAT 'peerId|sessionBegin|sessionEnd|type' (without quotes)";
	print " 'type' is maintained for backwards compatibility."
	print "\nUsage: [options] file_name_1 file_name_2 ..."
	print "\nOptions:"
	print "-h --help show this usage help message"
	print "-d --debug show some debug messages"
	print "-o --output= file prefix"
	print "  "
	# print "-f --file [file] input file (Weverton'session_line script output)"
	# print "-o --output [file] output file "
	print ""


if __name__ == '__main__':
	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	# INITIALIZE VARIABLES
	debug = False
	output_file_name_prefix = None
	count = 1

	try:
		optlist, args = getopt.gnu_getopt(sys.argv[count:], 'hdo:', ['help', 'debug', 'output='])
		for o, session in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			if o in ["-d", "--debug"]:
				count += 1
				debug = True

			elif o in ["-o", '--output']:
				count += 1
				output_file_name_prefix = session

	except Exception, e:
		print "Exception:", e
		print_usage()
		sys.exit(-1)

	if len(sys.argv[count:]) == 0:
		print "ERROR: no file! Use -h or --help for usage."
		sys.exit(-1)

	print "\nOPTIONS:"
	print "-------------"
	print "\tDebug: ", debug

	print "\nINPUT"
	print "-------------"
	print "\tFiles: ", sys.argv[count:]

	dir_data = Dirs().plots + "01_evaluation/00_data/"
	dir_plot = Dirs().plots + "01_evaluation/01_plot/"
	dir_eps = Dirs().plots + "01_evaluation/02_eps/"
	dir_png = Dirs().plots + "01_evaluation/03_png/"

	print ""
	print "\nMAKING DIRS"
	print "-------------"
	for dir in [dir_plot, dir_eps, dir_data, dir_png]:
		cmd = "mkdir -p " + dir
		run_cmd(cmd, 1, True)

	print "\nTESTING INPUT FILES"
	print "---------------------"
	for inputFileName in sys.argv[count:]:
		print "\tFile: ", inputFileName,
		if os.path.isfile(inputFileName):
			if os.path.getsize(inputFileName)> 100:
				analysis = Analysis(inputFileName)
				results[inputFileName] = analysis
				print " [OK]"
			else:
				print " [FOUND_EMPTY]"

		else:
			print " [NOT FOUND]"

	script_root = os.path.basename(__file__).split(".")[0]
	tempFileName = Dirs().temp + script_root + "_TEMP.txt"

	print "\nPROCESSING FILES"
	print "----------------"
	count_files = 1
	for inputFileName in sorted(results):
		# inputFileName_base = os.path.basename(file_name_input).split(".")[0]
		# tempFileName = Dirs().temp + inputFileName_base + "_TEMP.txt"
		print "\n"
		print "\tFILE (%d/%d) file_name_input: %s " % (count_files, len(results), inputFileName)
		print "\t-----------------------------------------------------------------------------"
		count_files += 1
		analysis = results[inputFileName]

		print ""
		print "\t\tPROCESSING SNAPSHOTS"
		print "\t\t--------------------"
		snapshot_file = open(inputFileName, 'r')
		snapshot_line = snapshot_file.readline()
		# skip header
		while snapshot_line[0] == "#":
			snapshot_line = snapshot_file.readline()

		#print snapshot_line.split("\n")[0] # debug
		peer_previous, window_previous = process_line(snapshot_line)

		# initialize variables
		peer_current = peer_previous
		window_current = window_previous

		# initialize first session
		if debug:
			print "#SESSION_\tsession\tpeer\tid\tbegin\tbw\tend\tew\tduration\tdws"
			print "PEER", peer_previous
			print "---------------"

		analysis.sessions_count[peer_current] = 1
		current_session_begin = window_current

		while True:
			snapshot_line = snapshot_file.readline()

			if not snapshot_line:
				break

			#print snapshot_line.split("\n")[0] # debug
			peer_current, window_current = process_line(snapshot_line)

			if peer_current != peer_previous:
				# the newly read address is different from the one we were tracking,
				# so close the old session and flush good session statistics

				# close the session of the previous peer
				session_name = "%d_%d" % (peer_previous, analysis.sessions_count[peer_previous])
				session_duration = window_previous - current_session_begin + 1
				# if session_duration > 0:
				# 	# session might have been already captured
				analysis.duration[session_name] = [current_session_begin, window_previous, session_duration]

				if debug:
					print "SESSION_\t%s\tp:\t%d\tb:\t%d\te:\t%d\td:\t%d" % (
						session_name, peer_previous, current_session_begin, window_previous, session_duration)
					print ""
					print "PEER", peer_current
					print "---------------"
				# start the session of the current peer
				analysis.sessions_count[peer_current] = 1
				current_session_begin = window_current

			else:
				# peer_current == peer_previous:
				# same peer may be within same session or not
				session_diff = window_current - window_previous
				#print "session diff:", session_diff, " peer:", peer_current , " current:", window_current, " previous:", window_previous
				if session_diff <= 1:
					# same session
					# do nothing

					pass
				else:
					# new session for the same peer
					# print window_current - window_previous #debug
					# close the previous session
					session_name = "%d_%d" % (peer_current, analysis.sessions_count[peer_current])
					session_duration = window_previous - current_session_begin + 1
					analysis.duration[session_name] = [current_session_begin, window_previous, session_duration]

					if debug:
						print "SESSION_\t%s\tp:\t%d\tb:\t%d\te:\t%d\td:\t%d" % (
							session_name, peer_previous, current_session_begin, window_previous, session_duration)

					# start the session of the current peer
					analysis.sessions_count[peer_current] += 1
					current_session_begin = window_current

			# update markers
			peer_previous = peer_current
			window_previous = window_current
		# end while true for reading file

		# close the last session
		session_name = "%d_%d" % (peer_previous, analysis.sessions_count[peer_previous])
		session_duration = window_previous - current_session_begin + 1
		analysis.duration[session_name] = [current_session_begin, window_previous, session_duration]

		if debug:
			print "SESSION_\t%s\tp:\t%d\tb:\t%d\te:\t%d\td:\t%d" % (
			session_name, peer_previous, current_session_begin, window_previous, session_duration)
		
		print ""
		print "\t\tANALYSING SESSIONS"
		print "\t\t------------------"
		analysis.print_sessions_count()
		analysis.print_sessions_length()
		print ""

	print ""
	print "\tPLOTTING CDFs"
	print "\t-------------"
	plot_cdf_session_length(results)
	plot_cdf_session_count(results)
	if output_file_name_prefix is not None:
		dest_length_file = dir_eps + output_file_name_prefix + "_session_length_cdf.eps"
		cmd = "mv %s %s" % (get_file_session_length_eps(PREFIX_CDF), dest_length_file)
		run_cmd(cmd, True, 1)

		dest_count_file = dir_eps + output_file_name_prefix + "_session_count_cdf.eps"
		cmd = "mv %s %s" % (get_file_session_count_eps(PREFIX_CDF), dest_count_file)
		run_cmd(cmd, True, 1)

	print ""
	print "\tPLOTTING HISTOGRAMS"
	print "\t-------------------"
	plot_hist_session_length(results)
	# plot_cdf_session_count(results)
	if output_file_name_prefix is not None:
		dest_length_file = dir_eps + output_file_name_prefix + "_session_length_hist.eps"
		cmd = "mv %s %s" % (get_file_session_length_eps(PREFIX_HIST), dest_length_file)
		run_cmd(cmd, True, 1)

	cmd = "mv %s*.png %s" % (dir_eps, dir_png)
	run_cmd(cmd, True, 1)

	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""
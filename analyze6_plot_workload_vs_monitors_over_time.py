#!/usr/bin/python
'''

'''
import sys, time, getopt, urllib, random, struct, commands, os, string, numpy, math, datetime

from analyze0_main import *

PL_FILE_NAME = "00_data_source/servers_status.txt"

NUMWANT = 50
#numwant: Optional. Number of peers that the client would like to receive from the tracker.
#This value is permitted to be zero. If omitted, typically defaults to 50 peers.
#source: https://wiki.theory.org/index.php/BitTorrentSpecification

#it was reported that
# "UDP tracker actually returns up to 200 (and no more) peers when I increases the num_want variable (to 500).
#  The HTTP version, on the other hand, seldom does."
#https://sourceforge.net/p/libtorrent/mailman/message/31465636/

hash_count_peer = 1
hash_table_peer = {}
monitors_dict = {}
sentinels_dict = {}

sum_list_size_diff = 0

class Announce:
	def __init__(self, epoch_, monitor_, tracker_, leechers_, seeders_, peer_list_, line_=""):
		global sum_list_size_diff
		self.epoch = epoch_
		self.monitor = monitor_
		self.tracker = tracker_
		try:
			self.leechers = int(leechers_)
			self.seeders = int(seeders_)

			if self.seeders + self.leechers > 1000:
				print line_

		except Exception, e:
			print "[WARNING] Announce.__init__ ", e
			self.leechers = -1
			self.seeders = -1

		self.peer_list, self.monitors_list, self.sentinels_list = process_peer_list(peer_list_, monitors_dict.values(), sentinels_dict.values())

		self.obtained = len(self.peer_list)
		if self.leechers == -1:
			self.leechers = self.obtained
			self.seeders = 0

		if len(self.peer_list) > self.seeders + self.leechers:
			# print "\n\n\n################\n\n\n"
			# print "[ERROR]: (size of peer_list) %d > %d (number of seeders(%d) + number of leechers(%d)) " % \
			# 	  (len(self.peer_list), (self.seeders+self.leechers), self.seeders, self.leechers)
			# print "line: ", line_
			# print "peerlist original: ", peer_list_
			# print "peerlist processed: ", self.peer_list
			# print "trunking list..."
			# self.peer_list = self.peer_list[0:self.seeders+self.leechers]
			#
			diff = len(self.peer_list)-(self.seeders + self.leechers)
			sum_list_size_diff += diff
			print "[WARNING]: size of peer_list %d > %d (number of seeders:%d + leechers:%d) by:%d  sum_list_size_diff: %d" % \
				  (len(self.peer_list), (self.seeders + self.leechers),  self.seeders, self.leechers, diff, sum_list_size_diff)

		else:
			pass
			#if debug:
			#print "(size of peer_list) %d <= %d (number of seeders(%d) + number of leechers(%d)) " % (
			#	len(self.peer_list), (self.seeders + self.leechers), self.seeders, self.leechers)

	def __string__(self):
		return "monitor:%s tracker:%s obtained:%d seeders:%d, leechers:%d"\
			   % (self.monitor, self.tracker, self.obtained, self.seeders, self.leechers)


class Tracker:
	def __init__(self, tracker_):
		self.tracker = tracker_
		self.announces = []
		self.monitors = set()


class Window:

	def __init__(self,  epoch_, number_,):

		self.epoch_begin = epoch_
		self.epoch_end = epoch_
		self.window_number = number_
		self.trackers = {}

	@staticmethod
	def header():
		return "#1-Window"\
			   " 2-avg_peers 3-std_peers"\
			   " 4-replied_queries 5-required_queries_avg_LNUMWANT"\
			   " 6-monitors 7-obtained_peers 8-min_peers 9-max_peers 10-sum_peer"\
			   " 11-required_queries_max_LNUMWANT 12-required_queries_sum_LNUMWANT"\
			   " 13-peers_uniques 14-required_queries_sum_avg_peers"\
			   " 15-obtained_monitors 16-obtained_sentinels"\
			   " 17-required_queries_max_avg_peers 18-required_queries_unique_peers_avg_peers"\
			   " 19-required_queries_avg_L200 20-required_queries_max_L200 21-required_queries_sum_L200 "\
			   " 22-obtained_peers_avg"\
			   " 23-obtained_peers_std"\
	           "\n"


	@staticmethod
	def get_required_queries(num_users_, num_boot_, list_max_):
		if not os.path.isfile("hoayfeld"):
			print "error: hoayfeld not found."
			sys.exit(-1)

		cmd = "./hoayfeld "
		cmd += " --action comp-e-est "
		cmd += " --num-users %d " % num_users_
		cmd += " --list-max %d " % list_max_
		#cmd += " --num-boot 1 "
		cmd += " --num-boot %d " % num_boot_

		if debug:
			print cmd

		result = commands.getoutput(cmd)
		return float(result.split()[1])

	# run_cmd(cmd, 1, True)

	def line(self):

		informed_peers_avg, informed_peers_std, replied_announces, monitors, peers_obtained, peers_min, peers_max, peers_sum, peers_uniques, monitors, sentinels, obtained_peers_avg, obtained_peers_std = self.get_summary()
		required_queries_avg = self.get_required_queries(informed_peers_avg, 1, NUMWANT)
		required_queries_max = self.get_required_queries(peers_max, 1, NUMWANT)
		required_queries_sum = self.get_required_queries(peers_sum, 1, NUMWANT)
		required_queries_sum_avg_peers = self.get_required_queries(peers_sum, 1, obtained_peers_avg)
		required_queries_max_avg_peers = self.get_required_queries(peers_max, 1, obtained_peers_avg)
		required_queries_unique_peers_avg_peers = self.get_required_queries(peers_uniques, 1, obtained_peers_avg)

		required_queries_avg_L200 = self.get_required_queries(informed_peers_avg, 1, 200)
		required_queries_max_L200 = self.get_required_queries(peers_max, 1, 200)
		required_queries_sum_L200 = self.get_required_queries(peers_sum, 1, 200)

		line = "%d" % self.window_number 	#  1
		line += " %f" % informed_peers_avg			#  2
		line += " %f" % informed_peers_std			#  3
		line += " %d" % replied_announces   #  4
		line += " %f" % required_queries_avg#  5
		line += " %d" % monitors 			#  6
		line += " %d" % peers_obtained		#  7
		line += " %d" % peers_min			#  8
		line += " %d" % peers_max			#  9
		line += " %d" % peers_sum			# 10
		line += " %f" % required_queries_max# 11
		line += " %f" % required_queries_sum# 12
		line += " %d" % peers_uniques		# 13
		line += " %f" % required_queries_sum_avg_peers	# 14
		line += " %d" % monitors 			# 15
		line += " %d" % sentinels			# 16
		line += " %f" % required_queries_max_avg_peers # 17
		line += " %f" % required_queries_unique_peers_avg_peers # 18
		line += " %d" % required_queries_avg_L200  # 19
		line += " %d" % required_queries_max_L200  # 20
		line += " %d" % required_queries_sum_L200  # 21
		line += " %f" % obtained_peers_avg  # 22
		line += " %f" % obtained_peers_std  # 23
		line += "\n"
		return line

	def get_summary(self):
		monitors = set()
		informed_peers = []
		obtained_peers = []

		announces_count = 0
		best_tracker_replies = ""
		best_tracker_replies_count = 0
		best_tracker_peers = ""
		best_tracker_peers_count = 0
		best_tracker_uniques = ""
		best_tracker_uniques_count = 0
		peer_list = set()
		monitors_set = set()
		sentinels_set = set()

		for tracker in self.trackers.values():
			tracker_informed_peers = []
			tracker_obtained_peers = []
			tracker_monitors_set = set()
			tracker_sentinels_set = set()
			peer_list_tracker = set()

			for announce in tracker.announces:
				tracker_informed_peers.append(announce.seeders + announce.leechers)

				if announce.obtained > 0:
					obtained_peers.append(announce.obtained)

				tracker_obtained_peers.append(announce.obtained)
				monitors.add(announce.monitor)
				#print "monitor: ", announce.monitor, " peers: ", announce.peers
				peer_list_tracker.update(announce.peer_list)
				tracker_monitors_set.update(announce.monitors_list)
				tracker_sentinels_set.update(announce.sentinels_list)

				announces_count += 1
				if debug:
					print "\t%02d "%announces_count, convert_from_epoch_to_time_str(announce.epoch), "monitor:", announce.monitor, " informed:", announce.seeders + announce.leechers, " obtained:", len(announce.peer_list)


			if debug:
				print "tracker_informed_peers:", tracker_informed_peers, "\n"
			informed_peers.append(numpy.max(tracker_informed_peers))

			if best_tracker_peers_count < sum(tracker_obtained_peers):
				best_tracker_peers_count = sum(tracker_obtained_peers)
				best_tracker_peers = tracker.tracker

			if best_tracker_replies_count < len(tracker.announces):
				best_tracker_replies_count = len(tracker.announces)
				best_tracker_replies = tracker.tracker

			if best_tracker_uniques_count < len(peer_list_tracker):
				best_tracker_uniques_count = len(peer_list_tracker)
				best_tracker_uniques = tracker.tracker

			peer_list.update(peer_list_tracker)
			monitors_set.update(tracker_monitors_set)
			sentinels_set.update(tracker_sentinels_set)

		informed_peers_mean = 0
		informed_peers_std = 0
		informed_peers_min = 0
		informed_peers_max = 0
		informed_peers_sum = 0
		obtained_peers_sum = 0
		obtained_peers_std = 0
		try:
			informed_peers_min = numpy.min(informed_peers)
			informed_peers_max = numpy.max(informed_peers)
			informed_peers_sum = sum(informed_peers)
			informed_peers_mean = numpy.mean(informed_peers)
			informed_peers_std = numpy.std(informed_peers)

		except Exception, e:
			print e, " informed_peers: ", informed_peers
			sys.exit()

		#f = open(get_log_tracker_file_name(), 'w')
		data = "window:%03d " % self.window_number
		data += " begin:%s" % convert_from_epoch_to_time_str(self.epoch_begin)
		data += " end:%s" % convert_from_epoch_to_time_str(self.epoch_end)
		data += " best_replies:%s count_replies:%d" % (get_tracker_nick(best_tracker_replies), best_tracker_replies_count)
		data += " best_obtained_peers:%s count_obtained_peers:%d" % (get_tracker_nick(best_tracker_peers), best_tracker_peers_count)
		data += " best_uniques:%s count_uniques:%d" % (get_tracker_nick(best_tracker_uniques), best_tracker_uniques_count)
		data += " monitors:%d" % len(monitors_set)
		data += " sentinels:%d" % len(sentinels_set)
		data += " informed_peers_min:%d" % informed_peers_min
		data += " informed_peers_max:%d" % informed_peers_max
		data += " informed_peers_sum:%d" % informed_peers_sum
		data += "\n"
		#f.write(data)
		#f.close()


		try:
			obtained_peers_sum = sum(obtained_peers)
			obtained_peers_avg = 0
			if len(obtained_peers)>0:
				obtained_peers_avg = 1.0*obtained_peers_sum / len(obtained_peers)
			obtained_peers_std = numpy.std(obtained_peers)
		except Exception, e:
			print e

		return informed_peers_mean, informed_peers_std, announces_count, len(monitors), obtained_peers_sum, informed_peers_min, informed_peers_max, informed_peers_sum, len(peer_list), len(monitors_set), len(sentinels_set), obtained_peers_avg, obtained_peers_std


def get_log_tracker_file_name():
	return "summary_" + output_base_name + "_log_tracker.txt"


def plot_header():
	return "# File generated by %s on %s" % (os.path.basename(__file__), datetime.datetime.now())


def print_usage():
	print "%s " % os.path.basename(__file__)
	print ""
	print "USAGE: [OPTIONS] file_name_1 file_name_2 ... "
	print "\nOptions:"
	print "-h --help show this usage help message"
	print "-d --debug show some debug messages"
	print "-i --input=file (temporary swarm)"
	print "-o --output=base id for output files (.txt, .plot, .eps)"
	print "-t --tracker=address "
	print ""


if __name__ == '__main__':

	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	# INITIALIZE VARIABLES
	debug = False
	input_file_name = "00_data_source/test_results/00_Collection_SWARM.txt"
	output_base_name = os.path.basename(__file__).split(".")[0]
	count = 1
	tracker_address_filter = None

	try:
		optlist, args = getopt.gnu_getopt(sys.argv[count:], 'hdi:o:t:', ['help','debug', 'input=', 'output=', 'tracker='])
		for o, a in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			if o in ["-d", "--debug"]:
				count += 1
				debug = True

			if o in ["-i", "--input"]:
				count += 1
				input_file_name = a

			if o in ["-o", "--output"]:
				count += 1
				output_base_name = a

			if o in ["-t", "--tracker"]:
				count += 1
				tracker_address_filter = a

	except Exception, e:
		print e
		sys.exit(-1)

	print "\nOPTIONS:"
	print "-------------"
	print "Debug: ", debug

	print "\nINPUT"
	print "-------------"
	print "Output base file_name_base: ", output_base_name
	print "Input file file_name_base : ", input_file_name
	print "Tracker address : ", tracker_address_filter

	if not os.path.isfile(input_file_name):
		print " Error: file not found: ", input_file_name
		sys.exit(-1)

	print "\nPROCESSING"
	print "-------------"
	dir_data = Dirs().plots + "03_workload_vs_monitors/00_data/"
	dir_plot = Dirs().plots + "03_workload_vs_monitors/01_plot/"
	dir_eps = Dirs().plots + "03_workload_vs_monitors/02_eps/"
	dir_png = Dirs().plots + "03_workload_vs_monitors/03_png/"
	dir_pdf = Dirs().plots + "03_workload_vs_monitors/04_pdf/"

	for dir in [dir_plot, dir_eps, dir_data, dir_png, dir_pdf]:
		cmd = "mkdir -p " + dir
		run_cmd(cmd, 0, True)

	data_file_name = "%s%s.txt" % (dir_data, output_base_name)
	print " data_file_name     :", data_file_name
	plot_file_name = "%s%s.plot" % (dir_plot, output_base_name)
	print " plot_file_name     :", plot_file_name
	eps_file_name = "%s%s" % (dir_eps, output_base_name)
	print " eps_file_name_base :", eps_file_name
	png_file_name = "%s%s" % (dir_png, output_base_name)
	print " png_file_name_base :", png_file_name
	pdf_file_name = "%s%s" % (dir_pdf, output_base_name)
	print " pdf_file_name_base :", pdf_file_name
	print " tracker_log_file   :", get_log_tracker_file_name()

	dir_servers = Dirs().servers
	monitors_file_name = dir_servers + MONITORS_FILE
	sentinels_file_name = dir_servers + SENTINELS_FILE
	print " dir_servers        :", dir_servers
	print " monitors_file_name :", monitors_file_name,
	monitors_dict = get_server_IPs(monitors_file_name)
	print "\n monitors_dict    :", monitors_dict

	print " sentinels_file_name:", sentinels_file_name,
	sentinels_dict = get_server_IPs(sentinels_file_name)
	print "\n sentinels_dict   :", sentinels_dict

	cmd = "rm %s " % get_log_tracker_file_name()
	run_cmd(cmd, 1, True)

	monitoring_start_epoch = get_start_monitoring_epoch()

	input_file = open(input_file_name)
	output_file = open(data_file_name, 'w')

	previous_window_number = -1
	window = None
	trackers = {}
	for line in input_file:

		#print line
		#example of input line
		#1543600055.000000 ['udp://tracker.opentrackr.org:1337/announce', 'intvl:', '1746', 'minIntvl:', '-1', 'd:', '-1', 'l:', '5', 'session_line:', '4', 'n:', '9', 'rtt:', '0.451426029205', '2018-11-30_17-15-00_a0000000026_plink.cs.uwaterloo.ca', 'peer_id:', '{139.47.17.59:', '35790,'}\n']

		try:
			convert_from_epoch_to_time_str(float(line.split()[0]))
			line_epoch = float(line.split()[0])

			window_minutes = (line_epoch - monitoring_start_epoch) / 60
			current_window_number = math.trunc(window_minutes / WINDOW_LEN_MINUTES)
			if current_window_number != previous_window_number:
				previous_window_number = current_window_number
				if window is None:
					# first window
					output_file.write(Window.header())
				else:
					output_file.write(window.line())

				window = Window(line_epoch, current_window_number)
			window.epoch_end = line_epoch
		except Exception, e:
			print "\n[WARNING] convert_from_epoch_to_time_str exception: ", e , " line:", line, " line skipped."
			continue #skip this line in case of any problem...

		try:
			tracker_address = line.split("'")[1]
		except Exception, e:
			print "\n[WARNING] tracker_address: ", e, "\nline:", line, " line skipped."
			continue #skip this line in case of any problem...

		if tracker_address_filter is None or tracker_address == tracker_address_filter:
			peerlist_line = []
			try:
				peerlist_line = line.split("{")[1].split("}")[0].replace(" ", "")

			except Exception, e:
				print "\n[WARNING] peerlist_line exception:", e, "\nline:", line, " line skipped."
				continue #skip this line in case of any problem...

			try:
				monitor = line.split("'")[31]
			except Exception, e:
				print "\n[WARNING] monitor exception:", e, "\nline:", line, " line skipped."
				continue #skip this line in case of any problem...

			if tracker_address in window.trackers:
				tracker = window.trackers.get(tracker_address)
			else:
				tracker = Tracker(tracker_address)
				window.trackers[tracker_address] = tracker

			if tracker_address in trackers:
				trackers[tracker_address] += 1
			else:
				trackers[tracker_address] = 1

			try:
				leechers_str = line.split("'l:', '")[1].split("'")[0]

			except Exception, e:
				print "\n[WARNING] leechers_str exception: ", e, "leechers_str: ", leechers_str, "\n\nline:", line
				#continue # skip this line in case of any problem...

			try:
				seeders_str = line.split("'s:', '")[1].split("'")[0]

			except Exception, e:
				print "\n[WARNING] seeders_str exception: ", e, "seeders_str: ", seeders_str, "\n\nline:", line

			try:
				n_peers = int(seeders_str) + int(leechers_str)
				if n_peers > 1000:
					print "n_peers:", n_peers
					print line
					#sys.exit(-1)
			except :
				pass

			# continue # skip this line in case of any problem...
			try:
				#if monitor not in tracker.monitors:
				# guarantee that only one monitor announce reply will be considered: TODO evaluate this!
				announce = Announce(line_epoch, monitor, tracker_address, leechers_str, seeders_str, peerlist_line, line)
				tracker.announces.append(announce)
				tracker.monitors.add(monitor)

			except Exception, e:
				print "\n[WARNING] announce exception: ", e, "\n\nline:", line, " line skipped."
				continue # skip this line in case of any problem...

	output_file.write(window.line())
	input_file.close()
	output_file.close()
	print "[OK]  ", now_str(), "processing data"

	f = open(get_log_tracker_file_name(), 'w')
	for t in sorted(trackers, key=trackers.__getitem__, reverse=True):
		f.write("%s %d\n" % (t, trackers[t]))
	f.close()

	terminal_eps = 'term postscript eps enhanced color "Helvetica" 24 lw 2'
	terminal_png = 'term png'
	terminal_pdf = 'term pdf enhanced color font "Helvetica, 24" '

	file_plot = open(plot_file_name, 'w')
	plot = plot_header()
	plot += '''
unset grid
set key on outside top horizontal 
#set y2tics
#set xrange [0:7200] # 2.5 months (ground truth)
set xrange [0:17280] # 6.0 months (case study)
set yrange [:]
set xlabel "Sampling No."
#set xlabel "Day No."
set ylabel "Number of Peer Lists"
set output "%s_queries.eps"


# line styles
set style line  1 lt 1 lc rgb '#352a87' # blue
set style line  2 lt 1 lc rgb '#0f5cdd' # blue
set style line  3 lt 1 lc rgb '#1481d6' # blue
set style line  4 lt 1 lc rgb '#06a4ca' # cyan
set style line  5 lt 1 lc rgb '#2eb7a4' # green
set style line  6 lt 1 lc rgb '#87bf77' # green
set style line  7 lt 1 lc rgb '#d1bb59' # orange
set style line  8 lt 1 lc rgb '#fec832' # orange
set style line  9 lt 1 lc rgb '#f9fb0e' # yellow

# New default Matlab line colors, introduced together with parula (2014b)
set style line 11 lt 1 lc rgb '#0072bd' # blue
set style line 12 lt 1 lc rgb '#d95319' # orange
set style line 13 lt 1 lc rgb '#edb120' # yellow
set style line 14 lt 1 lc rgb '#7e2f8e' # purple
set style line 15 lt 1 lc rgb '#77ac30' # green
set style line 16 lt 1 lc rgb '#4dbeee' # light-blue
set style line 17 lt 1 lc rgb '#a2142f' # red

set key samplen 1
set style line 1 lt 2 lc rgb '#7e2f8e' pointtype 2 pointsize 1  
set style line 2 lt 3 lc rgb '#87bf77' pointtype 3 pointsize 1 
set style line 3 lt 1 lc rgb '#4dbeee' pointtype 1 pointsize 1 


''' % (eps_file_name)
	file_plot.write(plot)


	plot = "set %s\n\n" % terminal_eps
	plot += "plot "
	plot += "  '%s' using 1:4 title 'Collected Peer Lists' with p ls 1" % data_file_name
	#session_line += ", '%session_line' using 1:5 title 'Required Queries (avg peers)' " % data_file_name
	plot += ", '%s' using 1:12 title 'Est. Req., N=(Sum), L=%d' with p ls 2" % (data_file_name, NUMWANT)
	plot += ", '%s' using 1:11 title 'Est. Req., N=(Max), L=%d' with p ls 3" % (data_file_name, NUMWANT)
	#plot += ", '%s' using 1:14 title 'Est. Req., N=(Sum), L=(Avg. Col. Peers)' " % data_file_name
	#plot += ", '%s' using 1:17 title 'Est. Req., N=(Max), L=(Avg. Col. Peers)' " % data_file_name
	plot += "\n\n"
	plot += 'set output "%s_queries.png"\n' % png_file_name
	plot += "set %s\n" % terminal_png
	plot += "replot\n\n"
	plot += "\n\n"
	plot += 'set output "%s_queries.pdf"\n' % pdf_file_name
	plot += "set %s\n" % terminal_pdf
	plot += "replot\n\n"
	file_plot.write(plot)

	plot = "set %s\n" % terminal_eps
	plot = '''
set ylabel "Number of Peers"
set output "%s_peers.eps"
#%s

	''' % (eps_file_name, Window.header())
	file_plot.write(plot)


	# x1y2  w yerr
	# Window avg_peers std_peers realized_queries expected_queries monitors\n"
	x_axys = "1"
	#x_axys = "($1/((24*60)/15))
	plot = "set %s\n" % terminal_eps
	plot += "plot '%s' using %s:($13+$16) title 'Collected Unique Peers' with p ls 1" % (data_file_name, x_axys)
	#plot += ", '%s' using %s:15 title 'Obtained Monitors' " % (data_file_name, x_axys)
	#plot += ", '%s' using %s:16 title 'Obtained Sentinels' " % (data_file_name, x_axys)
	#plot += ", '%s' using %s:2 title 'Reported Avg ' " % (data_file_name, x_axys)
	plot += ", '%s' using %s:10 title 'Sum Peers' with p ls 2" % (data_file_name, x_axys)
	plot += ", '%s' using %s:9 title 'Max Peers' with p ls 3" % (data_file_name, x_axys)
	plot += "\n\n"
	plot += 'set output "%s_peers.png"\n' % png_file_name
	plot += "set %s\n" % terminal_png
	plot += "replot\n"
	plot += "\n\n"
	plot += 'set output "%s_peers.pdf"\n' % pdf_file_name
	plot += "set %s\n" % terminal_pdf
	plot += "replot\n"
	file_plot.write(plot)

	file_plot.close()

	cmd = "gnuplot %s" % plot_file_name
	run_cmd(cmd, 1, True)


	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""
#!/usr/bin/python
'''
Created on Dec 06, 2018

Last update: Oct 05, 2019

@author: Rodrigo Mansilha
'''
import sys, time, getopt, random,  commands, os, datetime

# CONSTANTS
TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
PL_FILE_NAME = "00_data_source/servers_status.txt"
SENTINELS_FILE = "servers_sentinels.txt"
MONITORS_FILE = "servers_monitors.txt"
WINDOW_LEN_MINUTES = 15
RANDOM_SEED = 1

# DEFAULT VALUES
DEFAULT_MAGNET_FILE = "00_data_source/magnet_torrent_list.txt"
DEFAULT_DIR_SOURCE = "00_data_source/test_results/"
DEFAULT_SERVERS_FILE = "00_data_source/servers_status.txt"
DEFAULT_TRACKERS_FILE = "00_data_source/trackers_uniques.txt"
DEFAULT_SWARM_POS = 0
DEFAULT_SWARM_NUMBER = 0
DEFAULT_WINDOWS = 0
DEFAULT_ALPHA = 95

DEFAULT_CONVERT_FROM_DIR_TO_SWARM = False
DEFAULT_CONVERT_FROM_SWARM_TO_TRACE = False
DEFAULT_TRACE_CORRECTION = False
DEFAULT_TRACE_EVALUATION = False
DEFAULT_TRACE_EVALUATION_ALL = False
DEFAULT_TRACE_PLOT = False
DEFAULT_TRACE_PLOT_2 = False
DEFAULT_INTRODUCE_FAILURE = False
DEFAULT_EVALUATE_CORRECTION = False


#RANGES = [192, 96, 48, 24, 0]
RANGES = [0]
RESOLUTION_PROBABILITIES = [100]


FAILURE_PROBABILITIES = [00, 1, 5, 10, 15, 20, 25, 50, 75, 90]
#FAILURE_PROBABILITIES = [75, 90]
#FAILURE_PROBABILITIES = [00]

#ALPHAS = [60, 75, 90]
ALPHAS = [75, 85, 95]

#TRACKERS = ["", "udp://exodus.desync.com:6969/announce", "udp://tracker.cyberia.is:6969/announce"]
#TRACKERS = ["","udp://exodus.desync.com:6969/announce"]
#TRACKERS = ["", "udp://tracker.opentrackr.org:1337/announce", "udp://exodus.desync.com:6969/announce", "udp://tracker.cyberia.is:6969/announce"]

cmd = "cat %s " % DEFAULT_TRACKERS_FILE
TRACKERS = commands.getoutput(cmd).split("\n")
TRACKERS += [""]

# setup default values
magnet_file = DEFAULT_MAGNET_FILE
dir_source = DEFAULT_DIR_SOURCE
servers_file = DEFAULT_SERVERS_FILE
swarm_pos = DEFAULT_SWARM_POS
swarm_number = DEFAULT_SWARM_NUMBER
windows = DEFAULT_WINDOWS

convert_from_dir_to_swarm = DEFAULT_CONVERT_FROM_DIR_TO_SWARM
convert_from_swarm_to_trace = DEFAULT_CONVERT_FROM_SWARM_TO_TRACE
trace_correction = DEFAULT_TRACE_CORRECTION
trace_evaluation = DEFAULT_TRACE_EVALUATION
trace_evaluation_all = DEFAULT_TRACE_EVALUATION_ALL

introduce_failure = DEFAULT_INTRODUCE_FAILURE
evaluate_correction = DEFAULT_EVALUATE_CORRECTION

trace_plot = DEFAULT_TRACE_PLOT
trace_plot_2 = DEFAULT_TRACE_PLOT_2

dir_servers = "01_data_servers/"

dir_windows_prefix = "02_data_temp/00_windows"
dir_delayed = "02_data_temp/01_delayed/"
dir_temp = "02_data_temp/02_tmp/"
dir_proc = "02_data_temp/03_proc/"

dir_swarm = "03_data_result/00_swarm/"
dir_trace = "03_data_result/01_trace/"
dir_snapshot = "03_data_result/02_snapshot/"
dir_corrected = "03_data_result/03_corrected/"
dir_statistics_original = dir_corrected + "statistics_original/"
dir_statistics_corrected = dir_corrected + "statistics_corrected/"
dir_analysis = "03_data_result/04_analysis/"

dir_plots = "04_plot/"


class Dirs:
	def __init__(self):
		self.delayed = dir_delayed
		self.temp = dir_temp
		self.proc = dir_proc
		self.swarm = dir_swarm
		self.trace = dir_trace
		self.servers = dir_servers
		self.plots = dir_plots
		self.corrected = dir_corrected
		self.snapshot = dir_snapshot
		self.analysis = dir_analysis
		self.statistics_original = dir_statistics_original
		self.statistics_corrected = dir_statistics_corrected


names = {}
names['3C1D52279C6DCAB8B61AA58B6C2574A0BE2933E0'] = ['00_Collection_of_250_decrypted_3DS_ROMs_for_Citra_Emulator',
													 '00_Collection']
names['BA329B763627FA256CC1B311FBD3124F7B28E174'] = ['01_Aerofly_FS_2_Flight_Simulator-RELOADED',
													 '01_Aerofly']

# names['90E8A665EF71C89BA562D9D25E2CFCC11FDD70BC'] = ['02_NBA_2K18-CODEX', '02_NBA'] #Los Increibles 2 [1080p][Castellano][wWw EliteTorrent BiZ]
# names['0160FA6AF624241D0979362A564B7FEA65390C6A'] = ['03_Los_Increibles_2_1080p_Castellano_wWw_EliteTorrent_BiZ',
# 													 '03_Los_Increibles'] #The Happytime Murders 2018 1080p BluRay x264 DTS-FGT
# names['7B91F6E5131C8176828458579D38BF0AD78E9C64'] = ['04_The_Happytime_Murders_2018_1080p_BluRay_x264_DTS-FGT',
# 													 '04_The_Happytime'] #A Star is Born 2018 1080p KORSUB HDRip x264 AAC2 0-STUTTERSHIT
# names['E03A72E6864336B9BB388A7207A8FF1E4C543EBA'] = [
# 	'05_A_Star_is_Born_2018_1080p_KORSUB_HDRip_x264_AAC2_0-STUTTERSHIT', '05_A_Star'] #Mission Impossible - Fallout (2018) [BluRay] (1080p) [YTS AM]
#

names['90E8A665EF71C89BA562D9D25E2CFCC11FDD70BC'] = ['02_Los_Increibles_2_1080p_Castellano_wWw_EliteTorrent_BiZ',
													 '02_Increibles']

names['0160FA6AF624241D0979362A564B7FEA65390C6A'] = ['03_The_Happytime_Murders_2018_1080p_BluRay_x264_DTS-FGT',
													 '03_Happytime']

names['7B91F6E5131C8176828458579D38BF0AD78E9C64'] = ['04_A_Star_is_Born_2018_1080p_KORSUB_HDRip_x264_AAC2_0-STUTTERSHIT',
													 '04_Star']

names['E03A72E6864336B9BB388A7207A8FF1E4C543EBA'] = ['05_Mission_Impossible_Fallout_2018_BluRay_1080p_YTS_AM',
													 '05_Mission']

tracker_names = {}
tracker_names["udp://tracker.opentrackr.org:1337/announce"] = 'opentrackr'
tracker_names["udp://exodus.desync.com:6969/announce"] = 'desync'
tracker_names["udp://tracker.cyberia.is:6969/announce"] = 'cyberia'


class Torrent:
	def name(self):
		if self.infohash in names:
			return names[self.infohash][0]
		else:
			return self.infohash
			# names[''] = 'Mission Impossible - Fallout (2018) [BluRay] (1080p) [YTS AM]'

	def nick_name(self):
		if self.infohash in names:
			return names[self.infohash][1]
		else:
			return self.infohash

	def snapshotCorrectedFileName(self, alpha_, resolution_=100, failure_probability_=0):
		return dir_corrected + self.nick_name() + "_SNAP_CORRECTED_RES-%03d_FAIL-%03d_ALP-%03d.txt" % (resolution_, failure_probability_, alpha_)

	def snapshotOriginalFileName(self, resolution_=100, failure_probability_=0):
		return dir_snapshot + self.nick_name() + "_SNAP_ORIGINAL_RES-%03d_FAIL-%03d.txt" % (
		resolution_, failure_probability_)

	def traceFileName(self, resolution_=100, failure_probability_=0):
		trace_file_name = dir_trace + self.nick_name() + "_TRACE_RES-%03d.txt" % resolution_

		if failure_probability_ > 0:
			trace_file_name += ".sort_u_1n_4n.fail%d_seed%d" %(failure_probability_, RANDOM_SEED)

		return trace_file_name

	def failure_probability_log_file_name(self, alpha_, resolution_=100, failure_probability_=0):
		out_corrected_snap_file_name = self.snapshotCorrectedFileName(alpha_, resolution_, failure_probability_)
		return Dirs().statistics_corrected + os.path.basename(out_corrected_snap_file_name) + ".failure_probability.log"

	def get_swarm_file_name(self, resolution_=100):
		# self.swarmFileName = dir_swarm + self.nick_name() + "_SWARM.txt"
		return dir_swarm + self.nick_name() + "_SWARM_RES-%03d.txt" % resolution_

	def make_trackers_set(self):
		print "\n"
		print "\tmaking trackers set..."
		for tracker_torrent in self.trackers:
			for tracker_TRACKER in TRACKERS:
				#print "torrent: %session_line torrent_tracker: %session_line tracker_TRACKER: %session_line " % (self.nick_name(), tracker_torrent, tracker_TRACKER)
				if tracker_TRACKER in tracker_torrent:
					self.trackers_set.add(tracker_TRACKER)
					break
		#print  self.trackers
		#print  self.trackers_set
		print "\ttrackers set size: %d list size: %d" %(len(self.trackers_set), len(self.trackers))

	def __init__(self, infohash):
		self.infohash = infohash
		self.trackers = list()
		self.trackers_set = {""}
		self.tempFileName = dir_temp + self.nick_name() + "_TMP.txt"
		self.procFileName = dir_proc + self.nick_name() + "_PROC.txt"
		#self.swarmFileName = dir_swarm + self.nick_name() + "_SWARM.txt"

	def __str__(self):
		return self.name() + " " + self.infohash + " trackers:%d " % len(self.trackers)


class Tracker:

	def __init__(self, tracker_address_):
		self.tracker = tracker_address_
		self.torrents = list()

	def __str__(self):
	#def get_description(self):
		#return "url:%session_line nick:% torrents:%d" % (self.tracker, get_tracker_nick(self.tracker), len(self.torrents))
		return "url:%s" % (self.tracker)


class Monitor:

	def __init__(self, line_="all"):
		self.line = line_
		if self.line != "all":
			try:
				#print line_

				self.client_minus_server_epoch = int(self.line.split("client_minus_server_epoch:")[1].split(" ")[1])
				#print " client_minus_server_epoch=", self.client_minus_server_epoch

				# print "reading isSentinal...\session_begin\session_begin\session_begin",
				self.isSentinel = str2bool(self.line.split("=")[6].split(" ")[0])
				#print " isSentinel=", self.isSentinel

				# print "reading startTimeStr...\session_begin\session_begin\session_begin",
				self.startTimeStr = self.line.split("startTimeStr=")[1].split(" ")[0]
				self.startTime = time.strptime(self.startTimeStr, TIME_FORMAT)
				self.startTimeEpoch = time.mktime(self.startTime)
				self.startTimeEpoch += self.client_minus_server_epoch
				#print " startTimeEpoch=", self.startTimeStr

				self.monitorName = self.line.split("=")[9].split(" ")[0]
				#print " monitorName=", self.monitorName

				self.actor = self.line.split("actor=")[1].split(" ")[0]
				#print " actor", self.actor

				self.actor_int = int(self.actor.split("a")[1])
				#print " actor_int=", self.actor_int

				self.host = self.line.split("host=")[1].split("'")[0]
				# print " host=", self.host

			except Exception, e:
				print "exception: ", e

	def __str__(self):
		if self.line == "all":
			return "all"
		else:
			return self.startTimeStr + " %d" % self.startTimeEpoch + \
			   " " + self.actor + " " + self.host + " " + str(self.isSentinel) + \
			   " %d" % self.client_minus_server_epoch + self.monitorName


def get_server_IPs(file_name_):
	server_names = {}
	file_name_ip = file_name_ + "_with_ip.txt"
	print " original file_name_base   :", file_name_, " with_ip_file_name:", file_name_ip

	if not os.path.isfile(file_name_ip):
		f = open(file_name_ip, 'w')
		cmd = "cat %s" % file_name_
		lines = commands.getoutput(cmd).split('\n')
		for line in lines:
			server_name = line.split(" ")[0]
			try:
				cmd = 'ping -c 1 %s | grep PING | cut -d "(" -f 2 | cut -d ")" -f 1' % (server_name)
				server_ip = commands.getoutput(cmd)
			except:
				server_ip = "ping_time_out"
			#print session_line, ip
			f.write("%s %s\n" % (server_name, server_ip))

		f.close()

	cmd = "cat %s" % file_name_ip
	lines = commands.getoutput(cmd).split('\n')
	for line in lines:
		server_name = line.split(" ")[0]
		server_ip = line.split(" ")[1]
		server_names[server_name] = server_ip

	return server_names

	#print monitorIPs
	#print monitorIPs_Names
	f.close()
	return monitorIPs, monitorIPs_Names


def convert_from_epoch_to_time_str(epoch_):
	return time.strftime(TIME_FORMAT, time.localtime(epoch_))


def str2bool(value_):
	# print v.lower(),
	return value_.lower() in ("yes", "y", "true", "t", "1")


def get_number_of_cycles_for_considering_gap_as_failure(out_log_file_name_, tabs_=1):
	number_of_cycles_for_considering_gap_as_failure = None
	failure_probability = commands.getoutput("tail -n 1 %s | awk '{print $1}'" % out_log_file_name_)

	str_tabs = "\n" * tabs_
	if failure_probability == "FAILURE":
		print str_tabs, "CORRECT TRACE << FAILED >>"

	else:
		cmd = "tail -n1 %s | awk '{print $4}'" % out_log_file_name_
		print str_tabs, "getting results... ", cmd
		number_of_cycles_for_considering_gap_as_failure = int(commands.getoutput(cmd))
		print ""
		print str_tabs, "CORRECT TRACE << SUCCEED >> ",
		print "number_of_cycles_for_considering_gap_as_failure: ", number_of_cycles_for_considering_gap_as_failure

	return number_of_cycles_for_considering_gap_as_failure


def print_usage():
	print "Analyzes results of the Tracker lens"
	print ""
	print "USAGE:"
	print "-h --help           : show this usage help message"
	print ""
	print "-m --magnet=file    : containing magnetlinks (default=%s)" % DEFAULT_MAGNET_FILE
	print "-d --dir=path       : to directory with monitoring results (default=%s)" % DEFAULT_DIR_SOURCE
	print "-r --servers=file   : containing the list of servers (default=%s)" % DEFAULT_SERVERS_FILE
	print "-p --pos=number     : of the first swarm position (default=%d)" % DEFAULT_SWARM_POS
	print "-n --num=number     : of swarms to analyze (default=%d)" % DEFAULT_SWARM_NUMBER
	print "-w --windows=number : of time windows to be analyzed. 0 means all (default=%d)"% DEFAULT_WINDOWS
	#    print "-l --peerlistsize : max peer list Size. Value=0 means no limit. Default value=0 "
	print ""
	print "OPERATIONS:"
	print "-s --swarm    : do convert from directory to swarm?               (default=%s) (analyze1_convert_from_directory_to_swarm)" % str(
		DEFAULT_CONVERT_FROM_DIR_TO_SWARM)
	print "-t --trace    : do convert from swarm to trace?                   (default=%s) (analyze2_convert_from_swarm_to_trace) " % str(
		DEFAULT_CONVERT_FROM_SWARM_TO_TRACE)
	print "-f --failure  : do introduce failures?                            (default=%s) (script2_emulate_snapshot_failures.sh)" % str(
		DEFAULT_INTRODUCE_FAILURE)
	print "-c --correct  : do convert from trace to sesssion and correct it? (default=%s) (analyze3_correct_trace)" % str(
		DEFAULT_TRACE_CORRECTION)
	print "-e --evaluate : do evaluate traces (i.e. make CDF plots)?         (default=%s) (analyze4_evaluate_trace.py) " % str(
		DEFAULT_TRACE_EVALUATION)
	#print "-E --evaluateall : do evaluate/compare all traces?  (default=%s) (analyze4_evaluate_trace.py) " % str(
	#	DEFAULT_TRACE_EVALUATION_ALL)
	print "-l --plot     : do plot results?                                  (default=%s) (analyze5_plot_scatter_peers_over_time) " % str(
		DEFAULT_TRACE_PLOT)
	print "-o --plot2    : do plot results?                                  (default=%s) (analyze6_plot_workload_vs_monitors_over_time)" % str(
		DEFAULT_TRACE_PLOT_2)
	print "-E --evaluate2: do analyze corrections (i.e. make Table 2)?       (default=%s) (analyze7_evaluate_correction.py) " % str(
		DEFAULT_EVALUATE_CORRECTION)
	# print "-m --mon=[number] number of monitoring results to analyze 1<=x<=50"
	print ""


def plot_header():
	return "# File generated by %s on %s" % (os.path.basename(__file__), datetime.datetime.now())


def now_str():
	return time.strftime(TIME_FORMAT, time.localtime())


def run_cmd(cmd_, tabs_=0, print_cmd_=True, print_output_=False):
	space = "\t" * tabs_

	try:
		if print_cmd_:
			print space, now_str(), "CMD: " + cmd_

		if print_output_:
			print commands.getoutput(cmd_)
		else:
			commands.getoutput(cmd_)

			# print "out: ", out
			# if print_:
			#    print " done."
	except Exception, e:
		print " exception: ", e

	print ""


def subprocess(cmd):
	print "Subprocess: ", cmd
	#   result = commands.getoutput(cmd)
	return_code = subprocess.call(cmd, shell=True)
	print "return_code: ", return_code


def get_tracker_nick(tracker_address_):
	#print "tracker_address_:", tracker_address_
	if tracker_address_ == "":
		return ""

	else:
		return "_tr-%s" % tracker_address_.replace(".", "_")
    
#        if tracker_address_ in tracker_names:
#			return "_tr-%session_line" % tracker_names[tracker_address_]
#        else:
#            if ("/" in tracker_address_):
#                try:
#                    return "_tr-%session_line" % tracker_address_.split("/")[2].split(":")[0].replace(".", "_")
#                except:
#                    print "[WARNING] tracker_address_ in session wrong format:", tracker_address_
#                    return tracker_address_
#            else:
#                return "_tr-%session_line" % tracker_address_.replace(".", "_")


def process_peer_list(peer_list_original_, monitors_=[], sentinels_=[]):
	'''
	Process peer list string with format 'ip,port,,'
	example: '142.103.2.2:,6969,,88.12.21.204:,6881,,92.56.142.22:,23618'
	string may be empty: ''

	:param peer_list_original_: list with peers
	:param monitors_: list of ips of monitors
	:param sentinels_: list of ips of sentinels
	:return: processed_peer_list, processed_monitors_list, processed_sentinels_list
	'''

	processed_peer_list = []
	processed_monitors_list = []
	processed_sentinels_list = []
	peer_list_original_ = peer_list_original_.replace("'","").strip()

	#print "\n\npeer_list_original_:", peer_list_original_ # debug

	# list may be empty ('')
	# example of a list whith data: 142.103.2.2:,6969,,88.12.21.204:,6881,,92.56.142.22:,23618'
	if peer_list_original_:
		peer_list_split = peer_list_original_.split(",")
		size = len(peer_list_split)
		#print "size: ", size # debug
		pos = 0
		while pos < size:

			if ":" in peer_list_split[pos]:
				ip = peer_list_split[pos].split(":")[0]
				port = peer_list_split[pos+1]
				ip_port = "%s:%s" % (ip, port)
				#print "pos: %d ip_port: %s ip: %s port: %s" % (pos, ip_port, ip, port) # debug

				if ip == "0.0.0.0":
					pass

				elif ip in sentinels_:
					processed_sentinels_list.append(ip)
				elif ip in monitors_:
					processed_monitors_list.append(ip)
				else:
					processed_peer_list.append(ip_port)
			pos += 3  # ip: , port, ,

	return processed_peer_list, processed_monitors_list, processed_sentinels_list


def do_copy_windows_files_from_dir_in_to_dir_out(windows_, dir_in_, dir_out_):

	for i in range(windows_):
		print "copying files %d from %s to %s" %(i, dir_in_, dir_out_)
		cmd = 'find %s -name "*r%04d.gz" -exec cp -uf -t %s "{}" +' % (dir_in_, i, dir_out_)
		run_cmd(cmd, 3, True, True)


def do_convert_from_dir_to_swarm(torrent_, swarm_pos_, dir_source_, resolution_):

	print "\n"
	print "\t\tCONVERT FROM DIR TO SWARM"
	print "\t\t-------------------------"

	print "\n\t\tconvert from dir to swarm infohash: %s file_name_base: %s" % (torrent_.infohash, torrent_.name())

	cmd = " python analyze1_convert_from_directory_to_swarm.py "
	cmd += " --file=%s" % magnet_file
	cmd += " --dir=%s" % dir_source_
	cmd += " --pos=%s" % swarm_pos_
	cmd += " --num=1"
	cmd += " --resolution=%d" % resolution_
	run_cmd(cmd, 3, True)


def do_convert_from_swarm_to_trace(torrent_, resolution_):
	print ""
	print "\t\tCONVERT FROM SWARM TO TRACE"
	print "\t\t---------------------------\t"

	max_resolution = max(RESOLUTION_PROBABILITIES)

	# force skip the beginning of file due to clock sync problems... (TODO: find a better methodology)
	cmd = "head -n 3 %s | tail -n 1 " % torrent_.get_swarm_file_name(max_resolution)

	try:
		monitoring_start_epoch = float(commands.getoutput(cmd).split(" ")[0])

	except Exception, e:
		print "[ERROR] monitoring_start_epoch could not be found. ", commands.getoutput(cmd)
		print " cmd:", cmd
		sys.exit(-1)

	monitoring_start_epoch = commands.getoutput(cmd).split(" ")[0]
	print "\t\t\tconvert from swarm to trace infohash: %s file_name_base: %s " % (torrent_.infohash, torrent_.name())
	cmd = " python analyze2_convert_from_swarm_to_trace.py"
	cmd += " --input=%s" % torrent_.get_swarm_file_name(resolution_)
	cmd += " --output=%s" % torrent_.traceFileName(resolution_)
	cmd += " --epoch=%s" % monitoring_start_epoch
	#      cmd += " --peerListSize=%d" % maxPeerListSize

	run_cmd(cmd, 3, True)
	# subprocess(cmd)


def do_introduce_failure(torrent_, resolution_, failure_probability_):
	#TODO consider using snapshotFileName instead of traceFileName
	print ""
	print "\t\t\tINTRODUCE FAILURE"
	print "\t\t\t-----------------"
	if failure_probability_ == 0 :
		print "\t\t\t\tskip failure since prob == 0"
	else:
		cmd = " ./script2_emulate_snapshot_failures.sh "
		cmd += " -f %s " % torrent_.traceFileName(resolution_, 0)
		cmd += " -r %d " % RANDOM_SEED
		cmd += " -p %d " % failure_probability_
		run_cmd(cmd, 4, True)
		# subprocess(cmd)


def do_correct_trace(torrent_, resolution_=100, failure_probability_=0):
	print ""
	print "\t\t\tCORRECT TRACES"
	print "\t\t\t--------------"
	print ""
	print "\t\t\tcorrect trace infohash:%s file_name_base:%s failure_probability:%d "%(torrent_.infohash, torrent_.name(), failure_probability_)

	count_alpha = 1
	for alpha in ALPHAS:

		print "\t\t\t\tALPHA (%d/%d): %d" % (count_alpha, len(ALPHAS), alpha)
		print "\t\t\t\t------------------------"

		out_corrected_snap_file_name = torrent_.snapshotCorrectedFileName(alpha, resolution_, failure_probability_)
		out_log_file_name = torrent_.failure_probability_log_file_name(alpha, resolution_, failure_probability_)
		#print "\n\session_begin\session_begin\session_begin\trange_size (%d/%d): %d" % (count_ranges, len(RANGES), range_size)
		cmd = " python analyze3_correct_trace.py"
		cmd += " --in-trace=%s" % torrent_.traceFileName(resolution_, failure_probability_)
		cmd += " --out-original-snapshot=%s" % torrent_.snapshotOriginalFileName(resolution_, failure_probability_)
		cmd += " --out-corrected-snapshot=%s" % out_corrected_snap_file_name
		cmd += " --out-log=%s" % out_log_file_name
		cmd += " --alpha=%d " % alpha

		if count_alpha == 1:
			# only the first alpha requires processing original snapshot (since they can be used for the next ones)
			cmd += " --convert-original=True"
		else:
			cmd += " --convert-original=False"

		count_alpha += 1
		run_cmd(cmd, 5, True)

		gap = get_number_of_cycles_for_considering_gap_as_failure(out_log_file_name, 4)

def do_evaluate_correction(torrent_):
	print ""
	print "\t\tEVALUATING CORRECTION"
	print "\t\t--------------------"

	snapshot_ground_truth = torrent_.snapshotOriginalFileName(100, 0)

	for resolution in RESOLUTION_PROBABILITIES:
		print "\t\t\tRESOLUTION: %d " % resolution

		file_output = Dirs().analysis + "%s_ANALYSIS.txt" % os.path.basename(snapshot_ground_truth.split(".")[0])

		for failure_probability in FAILURE_PROBABILITIES:

			print "\t\t\t\tFAILURE PROBABILITY: %d " % failure_probability
			snapshot_original = torrent_.snapshotOriginalFileName(resolution, failure_probability)
			count_alphas = 0
			for alpha in ALPHAS:
				print "\t\t\t\t\tALPHA: %d " % alpha
				snapshot_corrected = torrent.snapshotCorrectedFileName(alpha, resolution, failure_probability)
				out_log_file_name = torrent_.failure_probability_log_file_name(alpha, resolution, failure_probability)
				cmd = "python analyze7_evaluate_correction_NEW3.py "
				cmd += " --output=%s " % file_output
				cmd += " --ground=%s " % snapshot_ground_truth
				cmd += " --original=%s " % snapshot_original
				cmd += " --corrected=%s " % snapshot_corrected
				cmd += " --log=%s " % out_log_file_name
				# cmd += " --check " # test

				count_alphas += 1
				if count_alphas > 1:
					cmd += " --omit-pif"

				if count_alphas == len(ALPHAS):
					cmd += " --last-alpha"

				run_cmd(cmd, 5, True, False)

				print ""
				print "\t\t\t\t\tend alpha"
				print "\t\t\t\t\t-------------------------"

			print ""
			print "\t\t\t\tend failure probability"
			print "\t\t\t\t-----------------------"

		print ""
		print "\t\t\tend resolution"
		print "\t\t\t--------------"

	# print ""
	# print "\t\tPLOTTING CORRECTION"
	# print "\t\t-------------------"
	#
	# plot = plot_header()
	# plot += '''
	# unset grid
	# unset key
	# set xlabel "Alpha"
	# set ylabel "Peer IP (anonymized)"
	#
	# set xrange [0:]
	# set yrange [0:]
	#
	# set term postscript eps enhanced color "Helvetica" 24 lw 2
	# set output "%s"
	#
	# plot '%s' using 1:2 title "sampling" with points lc 1 pt 1 ps 1
	# 			''' % (file_name_eps, file_data_name)
	#
	# plot += "\n"
	# plot += 'set output "%s"\n' % file_name_png
	# plot += "set term png\n"
	# plot += "replot\n"
	#
	# file_plot = open(file_name_plot, 'w', 1)
	# file_plot.write(plot)
	# file_plot.close()
	#
	# cmd = "gnuplot %s" % file_name_plot
	# run_cmd(cmd, 2, True)

	print "\t\tend correction evaluation"
	print "\t\t-------------------------"


def do_evaluate_trace_compare_each(torrent_):

	print ""
	print "\t\t\tEVALUATE EACH TRACE"
	print "\t\t\t-------------------"
	print ""
	print "\t\t\tinfohash: %s file_name_base: %s " % (torrent_.infohash, torrent_.name())
	cmd = " python analyze4_evaluate_trace.py "
	cmd += "--output=%s " % torrent_.nick_name()

	for resolution in RESOLUTION_PROBABILITIES:
		for failure_probability in FAILURE_PROBABILITIES:
			cmd += " %s" % torrent.snapshotOriginalFileName(resolution, failure_probability)
			for alpha in ALPHAS:
				cmd += " %s" % torrent.snapshotCorrectedFileName(alpha, resolution, failure_probability)

	run_cmd(cmd, 4, True)


def do_trace_scatter_plot(torrent_, resolution_, failure_probability_):
	print ""
	print "\t\t\tPLOT TRACES"
	print "\t\t\t-----------"
	print ""
	print "\t\t\t\tplot trace infohash:%s file_name_base:%s resolution:%d failure_probability:%d " % (torrent_.infohash, torrent_.name(), resolution_, failure_probability_)
	cmd = " python analyze5_plot_scatter_peers_over_time.py %s " % torrent_.traceFileName(resolution_, failure_probability_)
	run_cmd(cmd, 4, True)


def do_trace_plot_2(torrent_, resolution_):
	print ""
	print "\t\tPLOT TRACES 2"
	print "\t\t-------------"
	print ""
	print "\t\t\tplot trace 2 infohash:%s file_name_base:%s resolution:%d" % (torrent_.infohash, torrent_.name(), resolution_)

	cmd = " python analyze6_plot_workload_vs_monitors_over_time.py "
	cmd += " --input=%s " % torrent_.get_swarm_file_name(resolution_)
	cmd += " --output=%s_RES-%03d" % (torrent_.nick_name(), resolution_)

	run_cmd(cmd, 3, True)


def load_torrents(inputFileName):
	# le arquivo
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
			# if debug:
			#                    print "blank_line..."
			else:
				print "\tline_being_processed:", line[:100], " ..."
				countTorrents += 1
				magnetlink = line.partition('magnet:')[2].partition('"')[0]
				# print magnetlink
				infohash_hex = magnetlink.partition('btih:')[2].partition('&')[0]
				torrent = Torrent(infohash_hex)

				# print "infohash_hex:", infohash_hex
				# look for trackers' address
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
						# print "tracker:", it, " end:", tracker
						#                            tr = tr(infohash_url, tracker, 0)
						#                            print tr
						torrent.trackers.append(tracker)
						tracker_object = None
						if not tracker in trackers:
							tracker_object = Tracker(tracker)
						else:
							tracker_object = trackers[tracker]
						tracker_object.torrents.append(infohash_hex)
						trackers[tracker] = tracker_object
						#print "\session_begin\session_begin%session_line" % tracker_object
				torrents.append(torrent)
				print "\ttorrent: ", torrent

	except Exception, e:
		print "Exception while processing file:", inputFileName, " line:", i, " exception:", e
		print "Please, use -h or --help for instructions on how to use this script."
		sys.exit(-1)

	print "file_processing_finish!"
	print "NUMBER_OF_TORRENTS:" + str(countTorrents) + " NUMBER_OF_TORRENTS_AND_TRACKERS:" + str(countTorrentsTrackers)
	print ""
	return torrents


def is_tracker_in_torrent(torrent_, tracker_):

	for t in torrent.trackers:
		if tracker_ in t:
			return True

	return False


def get_start_monitoring_epoch():
	monitors = []
	file_pl = open(PL_FILE_NAME)
	for line_pl in file_pl:
		monitors.append(Monitor(line_pl))
	file_pl.close()

	return min(monitors, key=lambda monitor: monitor.startTimeEpoch).startTimeEpoch


if __name__ == '__main__':

	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	try:
		optlist, args = getopt.gnu_getopt(sys.argv[1:], 'hm:d:r:p:n:w:stfceElo',
										  ['help', 'magnet=', 'dir=', 'servers=', 'pos=', 'num=', 'windows=' \
										   'swarm', 'trace', 'failure', 'correct', 'evaluate', 'evaluate2', 'plot', 'plot2'])
		for o, a in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			elif o in ["-m", '--magnet']:
				magnet_file = a

			elif o in ["-d", '--dir']:
				dir_source = a

			elif o in ["-r", '--servers']:
				servers_file = a

			elif o in ["-p", '--pos']:
				swarm_pos = int(a)

			elif o in ["-n", '--num']:
				swarm_number = int(a)

			elif o in ["-w", '--windows']:
				windows = int(a)

			elif o in ["-s", "--swarm"]:
				convert_from_dir_to_swarm = True

			elif o in ["-t", "--trace"]:
				convert_from_swarm_to_trace = True

			elif o in ["-c", "--correct"]:
				trace_correction = True

			elif o in ["-f", "--failure"]:
				introduce_failure = True

			elif o in ["-e", "--evaluate"]:
				trace_evaluation = True

			elif o in ["-E", "--evaluate2"]:
				evaluate_correction = True

			elif o in ["-l", "--plot"]:
				trace_plot = True

			elif o in ["-o", "--plot2"]:
				trace_plot_2 = True

	except Exception, e:
		print "Exception", e
		print "Please, use option -h or --help for instructions."
		sys.exit(-1)

	print "SETTINGS"
	print "--------"
	print " RESOLUTIONS      : %s " % str(RESOLUTION_PROBABILITIES)
	print " ALPHAS           : %s " % str(ALPHAS)
	print " FAILURE PROB.    : %s " % str(FAILURE_PROBABILITIES)
	print " RANDOM SEED      : %d " % RANDOM_SEED
	print ""
	print "ARGUMENTS"
	print "---------"
	print " -m --magnet=file  : %s " % magnet_file
	print " -d --dir=path     : %s " % dir_source
	print " -r --servers=file : %s " % servers_file
	print " -p --pos=number   : %d " % swarm_pos
	print " -n --num=number   : %d %s  " % (swarm_number, ("" if swarm_number != 0 else "(MAX)"))
	print ""
	print "OPERATIONS"
	print "----------"
	print " -s --swarm        : %s" % convert_from_dir_to_swarm
	print " -t --trace        : %s" % convert_from_swarm_to_trace
	print " -f --failure      : %s" % introduce_failure
	print " -c --correct      : %s" % trace_correction
	print " -e --evaluate     : %s" % trace_evaluation
	print " -E --evaluateCorr : %s" % evaluate_correction
	print " -l --plot         : %s" % trace_plot
	print " -o --plot2        : %s" % trace_plot_2

	print ""

	print "Creating the structure of directories..."
	for dir in [dir_delayed, dir_temp, dir_proc, dir_swarm, dir_trace, dir_snapshot, dir_corrected, dir_analysis]:
		cmd = "mkdir -p " + dir
		run_cmd(cmd, 1, True)
	print "done."
	print ""

	if not os.path.isdir(dir_source):
		print "Exception: data source dir (%s) not found." % dir_source
		sys.exit(-1)

	if not os.path.isfile(magnet_file):
		print "Exception: magnet file (%s) not found." % magnet_file
		sys.exit(-1)

	torrents = load_torrents(magnet_file)

	if swarm_number == 0:
		swarm_number = len(torrents)

	if swarm_pos + swarm_number > len(torrents):
		print "Exception: swarm pos (%d) + swarm number (%d) must be < number of swarms (%d)" % \
			  (swarm_pos, swarm_number, len(torrents))
		sys.exit(-1)

	else:
		try:
			torrents = torrents[swarm_pos: swarm_pos + swarm_number]
		except Exception, e:
			print e
			sys.exit(-1)

	if windows > 0:
		print "\n"
		print "WINDOWS (%d) > 0 " % windows
		print "-------------------"
		dir_windows_local = "%s_%06d" % (dir_windows_prefix, windows)
		cmd = "mkdir -p %s " % dir_windows_local
		run_cmd(cmd, 2, True, True)

		print "\n\t\tcopy file from %s to %s" % (dir_source, dir_windows_local)
		do_copy_windows_files_from_dir_in_to_dir_out(windows, dir_source, dir_windows_local)
		dir_source = dir_windows_local

	count_torrents = 0
	for torrent in torrents:
		count_torrents += 1
		print "\n"
		header = "TORRENT (%d/%d): %s" % (count_torrents, len(torrents), torrent.nick_name())
		print header
		print "-" * len(header)

		#"Runnig..."
		count_resolution = 1
		for resolution in RESOLUTION_PROBABILITIES:
			print ""
			print "\tRESOLUTION (%d/%d): %s" % (count_resolution, len(RESOLUTION_PROBABILITIES), resolution)
			print "\t---------------------"
			count_resolution += 1

			if convert_from_dir_to_swarm:
				# index for count torrent begins with 0
				do_convert_from_dir_to_swarm(torrent, count_torrents-1+swarm_pos,  dir_source, resolution)
			else:
				print ""
				print "\t\tskip convert_from_dir_to_swarm (option -s)"

			if convert_from_swarm_to_trace:
				do_convert_from_swarm_to_trace(torrent, resolution)
			else:
				print ""
				print "\t\tskip convert_from_swarm_to_trace (option -t)"

			count_failure_probabilities = 1
			for failure_probability in FAILURE_PROBABILITIES:
				print ""
				print "\t\tFAILURE PROBABILITY (%d/%d): %d" % (count_failure_probabilities, len(FAILURE_PROBABILITIES), failure_probability)
				print "\t\t-----------------------------"
				count_failure_probabilities += 1

				if introduce_failure:
					do_introduce_failure(torrent, resolution, failure_probability)
				else:
					print ""
					print "\t\t\tskip introduce_failure (option -f)"

				if trace_correction:
					# TODO show gap as failure
					do_correct_trace(torrent, resolution, failure_probability)
				else:
					print ""
					print "\t\t\tskip trace_correction (option -c)"

				if trace_evaluation and resolution == RESOLUTION_PROBABILITIES[len(RESOLUTION_PROBABILITIES)-1]:
					#only one plot per torrent/failure probability, the last one!
					do_evaluate_trace_compare_each(torrent)
				else:
					print ""
					print "\t\t\tskip trace evaluation - each swarm (option -e)"

				if trace_plot:
					do_trace_scatter_plot(torrent, resolution, failure_probability)
				else:
					print ""
					print "\t\t\tskip trace plot (option -l)"

				print ""
				print "\t\tend failure probability"
				print "\t\t-----------------------"

			if trace_plot_2:
				do_trace_plot_2(torrent, resolution)
			else:
				print ""
				print "\t\tskip trace plot 2 (option -o)"

			print ""
			print "\tend resolution"
			print "\t--------------"

		if evaluate_correction:
			do_evaluate_correction(torrent)
		else:
			print ""
			print "\t\tskip evaluate correction (option -E)"

		print ""
		print "end torrent"
		print "-----------"

	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""
#!/usr/bin/python
'''


Second step to process the monitoring outputs.
This script converts from session swarm output format (one line per tracker response) to session peer presence format (one line per peer).

'''
import sys, time, getopt, urllib, random, struct, commands, os, string, math
from collections import defaultdict
from sets import Set

from analyze0_main import *

TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

PL_FILE_NAME = "00_data_source/servers_status.txt"

servers_dir = Dirs().servers

cmd = "cat %s " % DEFAULT_TRACKERS_FILE
TRACKER_ADDRESSES = commands.getoutput(cmd).split("\n")


def my_hash_peer(peer_str_):

	global hash_count_peer
	global hash_table_peer

	my_hash_peer_value = hash_table_peer.get(peer_str_)

	if my_hash_peer_value is None:
		my_hash_peer_value = hash_count_peer
		hash_table_peer[peer_str_] = my_hash_peer_value
		hash_count_peer += 1

	return my_hash_peer_value


def my_hash_monitor(monitor_str_):

	global hash_table_monitor
	global hash_count_monitor

	my_hash_monitor_value = hash_table_monitor.get(monitor_str_)

	if my_hash_monitor_value is None:
		my_hash_monitor_value = hash_count_monitor
		hash_table_monitor[monitor_str_] = my_hash_monitor_value
		hash_count_monitor += 1

	return my_hash_monitor_value


def loadSentinelIPs(sentinelFileName):
	sentinelIPs = []
	sentinelIP_Names = {}
	print "sentinels original file file_name_base:", sentinelFileName
	if os.path.isfile(sentinelFileName + "_with_ip.txt"):
		sentinelFileName = sentinelFileName + "_with_ip.txt"

	print "sentinels final file file_name_base:", sentinelFileName
	cmd = "cat %s" % sentinelFileName
	servers = commands.getoutput(cmd).split('\n')
	f = open(sentinelFileName + "_with_ip.txt", 'w')
	for s in servers:
		ip = None
		try:
			ip = s.split(" ")[1]
			# session_line = session_line.split(' ')[0]
		except:
			cmd = 'ping -c 1 %s | grep PING | cut -d "(" -f 2 | cut -d ")" -f 1' % (s)
			ip = commands.getoutput(cmd)
		print s, ip
		f.write("%s %s\n" % (s, ip))
		sentinelIPs.append(ip)
		sentinelIP_Names[ip] = s
	f.close()
	# print sentinelIPs
	# print sentinelIP_Names
	return sentinelIPs, sentinelIP_Names


def loadMonitorsIPs(monitorFileName):
	monitorIPs = []
	monitorIPs_Names = {}

	print "monitors original file file_name_base:", monitorFileName
	if os.path.isfile(monitorFileName + "_with_ip.txt"):
		monitorFileName = monitorFileName + "_with_ip.txt"

	cmd = "cat %s" % monitorFileName
	servers = commands.getoutput(cmd).split('\n')
	f = open(monitorFileName + "_with_ip.txt", 'w')
	for s in servers:
		ip = None
		try:
			ip = s.split(" ")[1]
			# session_line = session_line.split(' ')[0]
		except:
			cmd = 'ping -c 1 %s | grep PING | cut -d "(" -f 2 | cut -d ")" -f 1' % (s)
			ip = commands.getoutput(cmd)
		print s, ip
		f.write("%s %s\n" % (s, ip))
		monitorIPs.append(ip)
		monitorIPs_Names[ip] = s
	# print monitorIPs
	# print monitorIPs_Names
	f.close()
	return monitorIPs, monitorIPs_Names


def print_usage():
	print ""
	print "This script converts Tracker lens results from SWARM format (one peerlist per line) TRACE format (one peer per line)"
	print ""
	print "USAGE:"
	print "-h --help           : show this usage help message"
	print "-i --input [file]   : (i.e. *_SWARM.txt)"
	print "-o --output [file]  : (i.e. *_TRACE.txt)"
	print "-e --epoch value    :  when the monitoring started"
	print ""


if __name__ == '__main__':

	# HEADER
	print "\n"
	script_name = os.path.basename(__file__)
	print script_name.upper()
	print "-" * len(script_name)

	# INITIALIZE VARIABLES
	inputFileName = ""
	outputFileName = ""

	sentinels_file_name = servers_dir + "servers_sentinels.txt"
	monitors_file_name = servers_dir + "servers_monitors.txt"

	maxPeerListSize = 0
	tracker_address_filter = None

	n = 0
	monitoring_start_epoch = None

	try:

		optlist, args = getopt.gnu_getopt(sys.argv[1:], 'hi:o:e:',['help', 'input=', "output=", 'epoch='])
		for o, a in optlist:
			if o in ["-h", "--help"]:
				print_usage()
				sys.exit(0)

			elif o in ["-i", "--input"]:
				inputFileName = a

			elif o in ["-o", "--output"]:
				outputFileName = a

			if o in ["-e", "--epoch"]:
				monitoring_start_epoch = float(a)

	except Exception, e:
		print "Exception:", e
		print "Please, use -h or --help for instructions on how to use this script."
		sys.exit(-1)

	if inputFileName == "" or outputFileName == "":
		print "input file or output file is null."
		print "Please, use -h or --help for instructions on how to use this script."
		sys.exit(-1)

	print ""
	print "INPUT"
	print "-------------"
	print " Input file file_name_base  :", inputFileName
	print " Output file file_name_base :", outputFileName
	print " Start time epoch :", monitoring_start_epoch
	#print " Start time       :", time.strftime(TIME_FORMAT, time.localtime(monitoring_start_epoch))
	print "-------------------------------------"

	if monitoring_start_epoch is None:
		#monitoring_start_epoch = get_start_monitoring_epoch()
		cmd = "head -n 1 %s | tail -n 1 " % inputFileName
		monitoring_start_epoch = float(commands.getoutput(cmd).split(" ")[0])

	# HASHs
	hash_count_peer = 1
	hash_table_peer = {}

	hash_count_monitor = 1
	hash_table_monitor = {}

	# FILES
	file_output = open(outputFileName, "w")
	print "PROCESSING MONITORS..."
	print "----------------------"
	monitors_dict = get_server_IPs(monitors_file_name)

	print " monitors_file_name         :", monitors_file_name
	print " monitors_dict              :", monitors_dict
	print ""

	print "PROCESSING SENTINELS..."
	print "-----------------------"
	print " sentinels_file_name       :", sentinels_file_name
	sentinels_dict = get_server_IPs(sentinels_file_name)
	sentinelIPs = []
	sentinelIP_Names = {}
	if sentinels_file_name is not None:
		sentinelIPs, sentinelIP_Names = loadSentinelIPs(sentinels_file_name)
	print " sentinels_dict             :", sentinels_dict
	print ""


	out_header = "#window #time_min #IP:port #peerId #monitorId #monitor\n"
	file_output.write(out_header)

	line_count = 0
	file_input = open(inputFileName, "r")
	for line in file_input.readlines():

		try:
			#print "line_count: %d  line: %s" % (line_count, line) # debug

			# INPUT EXAMPLE
			# 1543600336.000000 ['udp://tracker.opentrackr.org:1337/announce', 'intvl:', '1691', 'minIntvl:', '-1', 'd:', '-1', 'l:', '6', 's:', '4', 'n:', '10', 'rtt:', '0.693554878235', '2018-11-30_17-15-00_a0000000028_pl1.rcc.uottawa.ca', 'p:', '{68.33.74.250:', '0,', '130.194.252.9:', '6969,', '216.48.80.12:', '6969,', '201.95.221.120:', '38943,', '95.212.149.150:', '10864,', '109.93.134.208:', '25510,', '36.90.18.254:', '16661,', '89.64.62.248:', '45579,', '189.163.97.255:', '51413,', '137.59.252.136:', '64057}\n']
			line_split = line.split()

			# CALCULATES WINDOW
			try:
				convert_from_epoch_to_time_str(float(line_split[0]))
				line_epoch = float(line_split[0])
			except Exception, e:
				print "[WARNING] [convert_from_epoch_to_time_str] exception:'", e, "' line:'", line, "' action: line skipped."
				continue

			time_line = None
			try:
				window_minutes = (line_epoch - monitoring_start_epoch) / 60
				current_window_number = math.trunc(window_minutes / WINDOW_LEN_MINUTES)
				if current_window_number < 0:
					print "[WARNING] [current_window_number<0] line:'", line, "' action: line skipped."
					continue
			except Exception, e:
				print "[WARNING] [current_window_number] exception:'", e, "' line:'", line, "' action: line skipped."
				continue

			# MONITOR
			monitor_str = line_split[16].split("'")[1]
			monitor_id = my_hash_monitor(monitor_str)
			#print "monitor_str:", monitor_str, " monitor_id:", monitor_id # debug

			# PEERS
			#print line.split("{")[1].split("}")[0].replace(" ", "") # debug
			peerlist_line, monitors_list_processed, sentines_list_processed = process_peer_list(line.split("{")[1].split("}")[0].replace(" ", ""), monitors_dict.values(), sentinels_dict.values())
			#print peerlist_line # debug
			for peer_str in peerlist_line:
				try:
					# peer_str='IP:port' (without quotes)
					ip = peer_str.split(":")[0]
					port = peer_str.split(":")[1]
					peer_id = my_hash_peer(peer_str)
					#print "peer:%s ip:%s port:%s id:%d" %(peer_str, ip, port, peer_id) # debug
					out_line = "%d %.02f %s %d %d %s\n" % (current_window_number, window_minutes, peer_str, peer_id, monitor_id, monitor_str)
					#print out_line # debug
					file_output.write(out_line)
				except Exception, e:
					print "[WARNING] [peer_list] exception:'", e, "' line:'", line, "' action: line skipped."
					continue

		except Exception, e:
			print "[WARNING] [general] exception:'", e, "' line:'", line, "' action: line skipped."
			continue

	file_input.close()
	file_output.close()

	print ""
	print "%s %s finished!" % (now_str(), script_name)
	print ""

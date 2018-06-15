#!/usr/bin/env python
import os
import sys
import getopt

from subprocess import Popen, PIPE, STDOUT

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/lib')
import file_handling
import functions
from nodes import Node

# Test if FastPath was compliled
if(not os.path.dirname(os.path.realpath(__file__))+'/fastpath/fastpathz'):
		sys.stderr.write("Error: fastpathz binary not found, did you type 'make'?\n")
		sys.exit()
#--------------------------------------------------------------------------------------------------#
#                               ARGUEMENTS                                                         #
#--------------------------------------------------------------------------------------------------#

args = file_handling.get_args()

#--------------------------------------------------------------------------------------------------#
#                               FILE INPUT                                                         #
#--------------------------------------------------------------------------------------------------#

my_contigs = file_handling.read_fasta(args.infile);
if not my_contigs:
	sys.stdout.write("Error: no sequences found in infile\n")
	sys.exit()

#--------------------------------------------------------------------------------------------------#
#                               MAIN ROUTINE                                                       #
#--------------------------------------------------------------------------------------------------#
for id, seq in my_contigs.items():

	#-------------------------------Create the Graph-------------------------------------------#
	my_orfs = functions.get_orfs(seq)

	my_graph = functions.get_graph(my_orfs)
	#-------------------------------Run Bellman-Ford-------------------------------------------#
	source = "Node('source','source',0,0)"
	target = "Node('target','target',0," + str(len(seq)+1) + ")"
	try:
		proc = Popen([os.path.dirname(os.path.realpath(__file__))+'/fastpath/fastpathz', '-s', source, '-t', target], stdout=PIPE, stdin=PIPE, stderr=PIPE)
	except:
		sys.stdout.write("Error running fastpathz. Did you run make to compile the binary?\n")
		sys.exit()
	# Write edges to the fastpath program, and multiply the weight to not lose decimal places
	for e in my_graph.iteredges():
		proc.stdin.write(repr(e.source) + "\t" + repr(e.target) + "\t" + str(e.weight*100000) + "\n")
		#sys.stdout.write(repr(e.source) + "\t" + repr(e.target) + "\t" + str(e.weight*100000) + "\n")
	#sys.exit()
	output = proc.communicate()[0].rstrip()
	if(output[:5] == 'ERROR'):
		print output
		sys.exit()
	my_path = output.split('\n')
	
	#Determine whether the first edge is a gap or an fragment open reading frame
	try:
		node1 = eval(my_path[1])
		node2 = eval(my_path[2])
		if(node1.type == 'stop' and node1.frame < 0):
			if(node1.frame == node2.frame):
				my_path = my_path[1:]
			else:
				my_path = my_path[2:]
		elif(node1.type == 'start' and node1.frame > 0):
			if(node1.frame == node2.frame):
				my_path = my_path[1:]
			else:
				my_path = my_path[2:]
	except:
		sys.stdout.write("Error running fastpathz: " + output + '\n')
 

	#-------------------------------Write Output ----------------------------------------------#
	file_handling.write_output(id, args, my_path, my_graph, my_orfs)

#--------------------------------------------------------------------------------------------------#
#                               END                                                                #
#--------------------------------------------------------------------------------------------------#






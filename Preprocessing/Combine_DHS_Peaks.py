import os
import subprocess
import sys

#This script cats the individual peak files together and merges them using bedtools merge.
#
#Arguments:
#arg1: Output folder for the combined peak set
#arg2-n: Path to the files that should be combined

def main():
	if (len(sys.argv) < 3):
		print("Insufficient arguments. Arguments are: <Output folder for the combined peaks> <Peak file 1> ... <Peak file n>")
	else:
		command="mkdir "+str(sys.argv[1])
		subprocess.call(command,shell=True)
		command="cat "
		for i in xrange(2,len(sys.argv)):
			command=command+str(sys.argv[i])+" "
		command=command+" > temp.peaks.bed"
		os.system(command)
		command="bedtools merge -i temp.peaks.bed > "+sys.argv[1]+"/filtered.peaks.merged.bed"
		os.system(command)
		command="rm temp.peaks.bed"
		os.system(command)

main()

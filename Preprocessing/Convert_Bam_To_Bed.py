import sys
import os
import argparse

#This script converts the DNase Bam files to bed files which are the input format of JAMM.
#It automatically generates a proper folder structure such that JAMM can be used easily.
#Note that the bam files will be deleted after conversion.
#
#arg1: Path to the BAM files
#arg2: Target of the Bed files

def main():
	parser=argparse.ArgumentParser(prog="Convert_BAM_To_Bed.py")
	parser.add_argument("source",nargs=1,help="Path to the DNase bam files provided at synapse")
	parser.add_argument("destination",nargs=1,help="Path to write the transformed files to")
	args=parser.parse_args()
	bamfiles=os.listdir(args.source[0])
	command="mkdir "+args.destination[0]
	os.system(command)
	for f in bamfiles:
		s=f.split(".")
		folderName=str(s[1]+"_"+s[2]+"_"+s[3])
		command="mkdir "+str(folderName)
		os.system(command)
		command="bamToBed -i "+args.source[0]+str(f)+" > "+args.destination[0]+folderName+"/"+f.replace("bam","bed")
		os.system(command)
		command="rm "+sys.argv[1]+str(f)
		os.system(command)

main()

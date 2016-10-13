import os
import sys
import argparse
from sets import Set


#This script transforms the TEPIC output into a bed file structure.
#Further, the coverage computed within peaks is added as an additional column to the file containing TF Affinity values.
#
#arg1: Path to the folder containing TF predictions computed by TEPIC. The reformated files will be stored in the same directory.

def main():
	parser=argparse.ArgumentParser(prog="Intersect_Bins_And_TF_Predictions.py")
	parser.add_argument("TF_Predictions",nargs=1,help="Path to TEPIC TF predictions computed in DHS. The reformated files will be stored in the same directory. Note that the original files will not be deleted.")
	args=parser.parse_args()

	files=os.listdir(args.TF_Predictions[0])
	for f in files:
		if ("Affinity.txt" in f):
			print("Reformating "+str(f))
			original=open(args.TF_Predictions[0]+f,"r")
			normalised=open(args.TF_Predictions[0]+f.replace(".txt",".bed"),"w")
			header=original.readline()
			normalised.write("#\t\t"+header)
			for l in original:
				s=l.split()
				ch=s[0].split(":")[0]
				se=s[0].split(":")[1]
				start=se.split("-")[0]
				end=se.split("-")[1]
				newline=str("chr"+ch+"\t"+start+"\t"+end)
				for i in xrange(1,len(s)):
					newline+="\t"+str(s[i])
				newline+="\n"
				normalised.write(newline)
			normalised.close()
			original.close()
		if ("Peak_Coverage.txt" in f):
			print("Reformating "+str(f))
			original=open(args.TF_Predictions[0]+f,"r")
			normalised=open(args.TF_Predictions[0]+f.replace(".txt",".bed"),"w")
			normalised.write("#\t\t\tCoverage\n")
			for l in original:
				s=l.split()
				newline="chr"+s[0]+'\t'+s[1]+'\t'+s[2]+'\t'+s[3]+'\n'
				normalised.write(newline)
			normalised.close()
			original.close()

	files=os.listdir(args.TF_Predictions[0])
	tfs=Set()
	for f in files:
		tfs.add(f.split("_")[0])
	for tf in tfs:
		for f in files:
			if (tf in f):
				if ("Scaled_Affinity.bed" in f):
					continue
				elif ("Affinity.bed" in f):
					command1="cut -f 4 "+args.TF_Predictions[0]+tf+"*Peak_Coverage.bed > coverage.temp"
					print(command1)
					os.system(command1)
					command="paste "+args.TF_Predictions[0]+f+" coverage.temp > "+args.TF_Predictions[0]+tf+"_Affinity_Peak_Coverage.bed"	
					print(command)
					os.system(command)
					command="rm coverage.temp"
					os.system(command)
			
main()

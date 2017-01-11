import sys
from collections import deque
import argparse
import subprocess
import os

#This script converts the shrunken Leaderboard or Test files such that for each TF the maximum affinity value of the 4 neighbouring bins (two in each direction) is reported.
#arg1 Path to the original shrunken Leaderboard or Test files
#arg2 Target directory to store the new maximised files

def writeMax(fifo):
	temp=str(fifo[2][0])
	for i in xrange(1,len(fifo[0])-3):
		temp+="\t"+str(max(float(fifo[0][i]),float(fifo[1][i]),float(fifo[2][i]),float(fifo[3][i]),float(fifo[4][i])))
	return temp+"\t"+fifo[2][len(fifo[0])-3]+"\t"+fifo[2][len(fifo[0])-2]+"\t"+fifo[2][len(fifo[0])-1]

def toString(texts):
	temp=str(texts[0])
	for i in xrange(1,len(texts)):
		temp+="\t"+texts[i]
	return temp
	
def main():
	parser=argparse.ArgumentParser(prog="ConvertMaxLeaderboardTest.py")
	parser.add_argument("cutData",nargs=1,help="Path to the original shrunken test or leader data")
	parser.add_argument("outPath",nargs=1,help="Output path for the shortened integrated Data")
	args=parser.parse_args()
	command = "mkdir "+args.outPath[0]
	print(command)
	subprocess.call(command,shell=True)	
	tfs=os.listdir(args.cutData[0])
	for tf in tfs:
		command="mkdir "+args.outPath[0]+tf
		print(command)
		subprocess.call(command,shell=True)
		ltfiles=os.listdir(args.cutData[0]+tf)
		for ltfile in ltfiles:
			print(ltfile)
			infile=open(args.cutData[0]+tf+"/"+ltfile,"r")
			oheader=infile.readline().strip()
			outfileName=ltfile+".maximised"
			outfile=open(args.outPath[0]+tf+"/"+outfileName,"w")
			outfile.write("\t"+oheader+"\n")
			line1=infile.readline()
			outfile.write(line1.strip()+"\n")
			line1=line1.split()
			line2=infile.readline()
			outfile.write(line2.strip()+"\n")
			line2=line2.split()
			line3=infile.readline().split()
			line4=infile.readline().split()
			fifo=deque([line1,line2,line3,line4])
			for line in infile:
				fifo.append(line.split())
				outfile.write(writeMax(fifo)+"\n")
				fifo.popleft()
			infile.close()
			outfile.write(toString(fifo[2])+"\n")
			outfile.write(toString(fifo[3])+"\n")
			outfile.close()

main()

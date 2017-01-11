import sys
import argparse
import subprocess
import os

#This script converts the shrunken Training files such that for each TF in adjacent bins that are labelled as bound, the maximum affinity is reported.
#arg1 Path to the original shrunken Training files
#arg2 Target directory to store the new maximised training files

def main():
	parser=argparse.ArgumentParser(prog="ConvertTrainingDataToMaxAffinityFormat.py")
	parser.add_argument("cutData",nargs=1,help="Path to the original shrunken training data")
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
		trainingfiles=os.listdir(args.cutData[0]+tf)
		for trainingfile in trainingfiles:
			#Extract header
			command="head -n 1 "+args.cutData[0]+tf+"/"+trainingfile+" > header.txt"
			print(command)
			subprocess.call(command,shell=True)
			#Grep Bound
			command="grep \"B\" "+args.cutData[0]+tf+"/"+trainingfile+" > "+trainingfile+".bound"
			print(command)
			subprocess.call(command,shell=True)
			#Deal with header
			headercheck=open(trainingfile+".bound","r")
			firstline=headercheck.readline()
			if ("response" in firstline):
				command="sed -i '1d' "+trainingfile+".bound"
				print(command)
				subprocess.call(command,shell=True)
			headercheck.close()
			#Grep Unbound
			command="grep \"U\" "+args.cutData[0]+tf+"/"+trainingfile+" > "+trainingfile+".unbound"
			print(command)
			subprocess.call(command,shell=True)
			#Deal with header
			headercheck=open(trainingfile+".unbound","r")
			firstline=headercheck.readline()
			if ("response" in firstline):
				command="sed -i '1d' "+trainingfile+".unbound"
				print(command)
				subprocess.call(command,shell=True)
			headercheck.close()
			#Convert Bound
			print("Converting")
			infile=open(trainingfile+".bound","r")
			outfile=open(trainingfile+".bound.maximised","w")
			hdict={}
			neighbours=[]
			counts=-1
			prevstart=0
			prevchrom=""
			line=0
			for l in infile:
				s=l.split()
				chrom=s[0].split(":")[0]
				start=int(s[0].split(":")[1].split("-")[0])
				if (prevchrom!=chrom):
					neighbours=neighbours+[[s]]
					prevstart=start
					prevchrom=chrom
					counts+=1
				elif (start-prevstart == 50):
					neighbours[counts]=neighbours[counts]+[s]
					prevstart=start
					prevchrom=chrom
				else:
					neighbours=neighbours+[[s]]
					prevstart=start
					prevchrom=chrom
					counts+=1
				#Go through neighbours
			for i in xrange(0,len(neighbours)):
				#Go through each factor
				for tfn in xrange(1,len(neighbours[0][0])-4):
					#Go through all values
					maxValue=0
					for j in xrange(0,len(neighbours[i])):	
						maxValue=max(maxValue,float((neighbours[i][j][tfn])))
						for j in xrange(0,len(neighbours[i])): 
							neighbours[i][j][tfn]=str(maxValue)
			for i in xrange(0,len(neighbours)):
				for j in xrange(0,len(neighbours[i])):	
					temp=str(neighbours[i][j][0])
					for x in xrange(1,len(neighbours[i][j])):
						temp+="\t"+neighbours[i][j][x]
					outfile.write(temp+"\n")
			outfile.close()
			command="cat header.txt "+trainingfile+".bound.maximised "+str(trainingfile)+".unbound > "+str(args.outPath[0])+str(tf)+"/"+str(trainingfile)+".maximised"
			print(command)
			subprocess.call(command,shell=True)

main()

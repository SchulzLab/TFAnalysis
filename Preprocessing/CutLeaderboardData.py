import os
import sys
import argparse
import subprocess

#This script combines the TEPIC annotations in bins with the open chromatin predictions for leader data
#arg1=Path to the file you want to cut the data from
#arg2=Path to file containing the names of the TF that should be cut 
#arg3=Path to store the filtered data

def main():
	parser=argparse.ArgumentParser(prog="CutLeaderboardData.py")
	parser.add_argument("integratedData",nargs=1,help="Path to the data from which columns should be extracted")
	parser.add_argument("cutInformation",nargs=1,help="Files containing the TFs that should be cut")
	parser.add_argument("outPath",nargs=1,help="Output path for the shortened integrated Data")
	args=parser.parse_args()
	command="mkdir "+args.outPath[0]
	subprocess.call(command,shell=True)

	integratedFiles=os.listdir(args.integratedData[0])
	cutInformationFiles=os.listdir(args.cutInformation[0])
	nleaderTFs=["E2F1","FOXA2","HNF4A","NANOG"]
	for iFiles in integratedFiles:
		for cFiles in cutInformationFiles:
			cutTF=cFiles.split("_")[0]
			if (cutTF not in nleaderTFs):
				integratedTF=iFiles.split(".")[0]
				cutSet=set()
				cutFile=open(args.cutInformation[0]+cFiles,"r")
				for l in cutFile:
					cutSet.add(l.strip().replace("..","::").replace(".var.2.","(var.2)").replace(".var.3.","(var.3)").replace("2.5","2-5").replace("3.2","3-2").replace("3.1","3-1").replace("1.F","1-F").replace("x.a","x-a").replace("2.3","2-3").replace("2.8","2-8").replace("6.1","6-1").replace("6.2","6-2").upper())
				cutFile.close()
			
				integratedFile=open(args.integratedData[0]+iFiles,"r")
				header=integratedFile.readline()
				sh=header.split()
				temp="cut -f 1"
				for i in xrange(0,len(sh)):
					comp=str(sh[i].upper())	
					if(comp in cutSet):
						temp=temp+","+str(i+2)
				integratedFile.close()
				command=temp+" "+args.integratedData[0]+iFiles+" > "+args.outPath[0]+cutTF+"_Leaderboard_TEPIC_Annotation_Cut.txt"
				print(command)
				subprocess.call(command,shell=True)

main()

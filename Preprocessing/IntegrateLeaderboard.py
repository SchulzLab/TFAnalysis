import os
import sys
import argparse
import subprocess

#This script combines the TEPIC annotations in bins with the open chromatin predictions for leader data
#arg1=Path to the TEPIC annotations
#arg2=Path to the DNase coverage bed files for the center bin
#arg3=Path to the DNase coverage bed files for the left bin
#arg4=Path to the DNase coverage bed files for the right bin
#arg5=Output path. Subdirectories are created automatically

def main():
	parser=argparse.ArgumentParser(prog="IntegrateLeaderboard.py")
	parser.add_argument("tf",nargs=1,help="Path to TEPIC annotations")
	parser.add_argument("dnaseM",nargs=1,help="Path to the DNase coverage bed files for the center bins")
	parser.add_argument("dnaseL",nargs=1,help="Path to the DNase coverage bed files for the left bins")
	parser.add_argument("dnaseR",nargs=1,help="Path to the DNase coverage bed files for the right bins")
	parser.add_argument("destination",nargs=1,help="Path to write the Integrated data to")
	args=parser.parse_args()
	tfFiles=os.listdir(args.tf[0])
	dnaseFilesC=os.listdir(args.dnaseM[0])
	dnaseFilesL=os.listdir(args.dnaseL[0])
	dnaseFilesR=os.listdir(args.dnaseR[0])
	command="mkdir "+args.destination[0]
	print(command)
	subprocess.call(command,shell=True)
	leaderTFs={}
	leaderTFs["ARID3A"]=["K562"]
	leaderTFs["ATF3"]=["liver"]
	leaderTFs["ATF7"]=["MCF-7"]
	leaderTFs["CEBPB"]=["MCF-7"]
	leaderTFs["CREB1"]=["MCF-7"]
	leaderTFs["CTCF"]=["GM12878"]
	leaderTFs["E2F6"]=["K562"]
	leaderTFs["EGR1"]=["K562"]
	leaderTFs["EP300"]=["MCF-7"]
	leaderTFs["FOXA1"]=["MCF-7"]
	leaderTFs["GABPA"]=["K562"]
	leaderTFs["GATA3"]=["MCF-7"]
	leaderTFs["JUND"]=["H1-hESC"]
	leaderTFs["MAFK"]=["K562","MCF-7"]
	leaderTFs["MAX"]=["MCF-7"]
	leaderTFs["MYC"]=["HepG2"]
	leaderTFs["REST"]=["K562"]
	leaderTFs["RFX5"]=["HepG2"]
	leaderTFs["SPI1"]=["K562"]
	leaderTFs["SRF"]=["MCF-7"]
	leaderTFs["STAT3"]=["GM12878"]
	leaderTFs["TAF1"]=["HepG2"]
	leaderTFs["TCF12"]=["K562"]
	leaderTFs["TCF7L2"]=["MCF-7"]
	leaderTFs["TEAD4"]=["MCF-7"]
	leaderTFs["YY1"]=["K562"]
	leaderTFs["ZNF143"]=["K562"]
	for tfFile in tfFiles:
		tf=tfFile.split("_")[0]
		command="mkdir "+args.destination[0]+tf
		print(command)
		subprocess.call(command,shell=True)
		for tfTissue in leaderTFs[tf]:
			for dnaseFile in dnaseFilesC:
				tissueDNase=dnaseFile.split(".")[1]
				for dnaseFileL in dnaseFilesL:
					tissueDNaseL=dnaseFileL.split(".")[1]
					for dnaseFileR in dnaseFilesR:
						tissueDNaseR=dnaseFileR.split(".")[1]
						if (tfTissue==tissueDNase) and (tfTissue==tissueDNaseL) and (tfTissue==tissueDNaseR):
							command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.dnaseM[0]+dnaseFile+" > "+args.dnaseM[0]+dnaseFile+".sorted"
							print(command)
							subprocess.call(command,shell=True)
							command="cat headerC_TL.txt "+args.dnaseM[0]+dnaseFile+".sorted | cut -f 4 -d \" \" > IntegrateC_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="sed -i 's/ /\t/g' IntegrateC_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.dnaseL[0]+dnaseFileL+" > "+args.dnaseL[0]+dnaseFileL+".sorted"
							print(command)
							subprocess.call(command,shell=True)
							command="cat headerL.txt "+args.dnaseL[0]+dnaseFileL+".sorted | cut -f 4 -d \" \" > IntegrateL_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="sed -i 's/ /\t/g' IntegrateL_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.dnaseR[0]+dnaseFileR+" > "+args.dnaseR[0]+dnaseFileR+".sorted"
							print(command)
							subprocess.call(command,shell=True)
							command="cat headerR.txt "+args.dnaseR[0]+dnaseFileR+".sorted | cut -f 4 -d \" \" > IntegrateR_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="sed -i 's/ /\t/g' IntegrateR_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="paste "+args.tf[0]+tfFile+" IntegrateC_temp.txt IntegrateL_temp.txt IntegrateR_temp.txt > "+args.destination[0]+tf+"/"+tf+"."+tfTissue+".Integrated.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="rm IntegrateC_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="rm IntegrateL_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
							command="rm IntegrateR_temp.txt"
							print(command)
							subprocess.call(command,shell=True)
		
main()

import os
import sys
import argparse
import subprocess

#This script combines the TEPIC annotations in bins with the open chromatin predictions for training data
#arg1=Path to the TEPIC annotations
#arg2=Path to the DNase coverage bed files for the center bin
#arg3=Path to the DNase coverage bed files for the left bin
#arg4=Path to the DNase coverage bed files for the right bin
#arg5=Output path. Subdirectories are created automatically

def main():
	parser=argparse.ArgumentParser(prog="IntegrateTraining.py")
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
	for tfFile in tfFiles:
		tf=tfFile.split(".")[0]
		tfTissue=tfFile.split(".")[1].split("_")[0]
		command="mkdir "+args.destination[0]+tf
		print(command)
		subprocess.call(command,shell=True)
		for dnaseFile in dnaseFilesC:
			tfDNase=dnaseFile.split(".")[0]
			tissueDNase=dnaseFile.split(".")[1]
			for dnaseFileL in dnaseFilesL:
				tfDNaseL=dnaseFileL.split(".")[0]
				tissueDNaseL=dnaseFileL.split(".")[1]
				for dnaseFileR in dnaseFilesR:
					tfDNaseR=dnaseFileR.split(".")[0]
					tissueDNaseR=dnaseFileR.split(".")[1]
					if (tf==tfDNase) and (tfTissue==tissueDNase) and (tf==tfDNaseL) and (tfTissue==tissueDNaseL) and(tf==tfDNaseR) and (tfTissue==tissueDNaseR):
						command="cat headerC.txt "+args.dnaseM[0]+dnaseFile+" | cut -f 4,5 -d \" \" > IntegrateC_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="sed -i 's/ /\t/g' IntegrateC_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="cat headerL.txt "+args.dnaseL[0]+dnaseFileL+" | cut -f 4 -d \" \" > IntegrateL_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="sed -i 's/ /\t/g' IntegrateL_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="cat headerR.txt "+args.dnaseR[0]+dnaseFileR+" | cut -f 4 -d \" \" > IntegrateR_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="sed -i 's/ /\t/g' IntegrateR_temp.txt"
						print(command)
						subprocess.call(command,shell=True)
						command="paste "+args.tf[0]+tfFile+" IntegrateC_temp.txt IntegrateL_temp.txt IntegrateR_temp.txt> "+  args.destination[0]+tf+"/"+tf+"."+tfTissue+".Integrated.txt"
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

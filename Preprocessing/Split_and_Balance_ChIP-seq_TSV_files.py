import os
import subprocess
import sys
import argparse

#This script transforms the original ChIPSeq TSV files into bed files separated per TF and tissue.
#The number of bound samples is not reduced. The number of unbound samples is reduced to the number of present bound samples.
#
#arg1: Path to the ChIP-seq tsv files provided at Synapse
#arg2: Path to write the balanced files to, splitted per TF and Tissue.

def main():
	parser=argparse.ArgumentParser(prog="Split_and_Balance_ChIP-seq_TSV_files.py")                                                                                                               
	parser.add_argument("source",nargs=1,help="Path to the ChIP-seq tsv files provided at synapse")
	parser.add_argument("destination",nargs=1,help="Path to write the balanced files to, splitted per TF and Tissue")
	args=parser.parse_args() 

	command="mkdir "+str(args.destination[0])
	subprocess.call(command,shell=True)
	
	ChIP_Labels=os.listdir(args.source[0])
	for f in ChIP_Labels:
		infile=open(args.source[0]+f,"r")
		header=infile.readline()
		tissues=header.split()[3:]
		print(tissues)
		counter=4
		infile.close()
		for t in tissues:
			print f.split(".")[0]+" in Tissue "+t
			command="awk '{if ($"+str(counter)+"== \"B\") print $0}' "+args.source[0]+f+" | wc -l "
			output=subprocess.check_output(command,shell=True)
			command="awk '{if ($"+str(counter)+"== \"U\") print $0}' "+args.source[0]+f+" | shuf  > Negative_Temp.txt" 
			subprocess.call(command,shell=True)
			command="head -n "+str(output).strip()+" Negative_Temp.txt > Negative_Temp_Cutted.txt"
			subprocess.call(command,shell=True)
			command="awk '{if ($"+str(counter)+"== \"B\") print $0}' "+args.source[0]+f+" > Positive_Temp.txt"
			subprocess.call(command,shell=True)
			command="cat Positive_Temp.txt Negative_Temp_Cutted.txt | cut -f 1,2,3,"+str(counter)+" > "+args.destination[0]+str(f.split(".")[0])+"."+t+".Balanced.bed"
			subprocess.call(command,shell=True)
			command="rm Positive_Temp.txt"
			subprocess.call(command,shell=True)
			command="rm Negative_Temp.txt"
			subprocess.call(command,shell=True)
			command="rm Negative_Temp_Cutted.txt"
			subprocess.call(command,shell=True)
			counter+=1



main()

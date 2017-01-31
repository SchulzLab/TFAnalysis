import os
import subprocess
import sys
import argparse
from sets import Set

#This script faciliates computing the DNase Coverage in the bins specified by the provided bed files
#Here, the coverage data is generated for training, leaderboard and test data sets
#arg1: Path to the bam files
#arg2: Path to the bed files representing the balanced ChIP-seq data for training
#arg3: Path to the leaderboard regions
#arg4: Path to the test regions
#arg5: Path to store the results

def main():
	parser=argparse.ArgumentParser(prog="Compute_DNase_Coverage.py")                                                                                                               
	parser.add_argument("bam",nargs=1,help="Path to the DNase bam files provided at synapse")
	parser.add_argument("bed",nargs=1,help="Path to the ChIP-seq bed files that should be used for intersecting")
	parser.add_argument("leaderboard",nargs=1,help="Path to the Leaderboard regions")
	parser.add_argument("test",nargs=1,help="Path to the test regions")
	parser.add_argument("destination",nargs=1,help="Path to write the bed files too, subfolders are created automatically")
	args=parser.parse_args() 

	#Generating folders
	command="mkdir "+str(args.destination[0])
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training/Center"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training/Left"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard/Center"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard/Left"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Center"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Left"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Median"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Median/Left"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Test/Median/Middle"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Test/Median/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Test/Median/Left"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Test/Median/Middle"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Test/Median/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training/Median"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Training/Median/Left"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Training/Median/Middle"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Training/Median/Right"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard/Median"
	subprocess.call(command,shell=True)

	command="mkdir "+str(args.destination[0])+"Leaderboard/Median/Left"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Leaderboard/Median/Middle"
	subprocess.call(command,shell=True)
	
	command="mkdir "+str(args.destination[0])+"Leaderboard/Median/Right"
	subprocess.call(command,shell=True)

	BAM_files=os.listdir(args.bam[0])
	bed_files=os.listdir(args.bed[0])
	leaderTissues=["K562","liver","MCF-7","GM12878","H1-hESC","HepG2"]
	testTissues=["PC-3","induced_pluripotent_stem_cell","K562","liver"]

	#Generate left and right neighbour bed files
	for t in bed_files:
		if ("sorted" not in t):
			ts=t.split(".")
			command="awk '{if ($2-50 < 0) print($1\"\t\"0\"\t\"$3); else print($1\"\t\"$2-50\"\t\"$3-50)}' "+args.bed[0]+t+" > "+args.bed[0]+ts[0]+"."+ts[1]+".Left.bed"
			print(command)
			subprocess.call(command,shell=True)
			command="awk '{print($1\"\t\"$2+50\"\t\"$3+50)}' "+args.bed[0]+t+" > "+args.bed[0]+ts[0]+"."+ts[1]+".Right.bed"
			print(command)
			subprocess.call(command,shell=True)

	command="awk '{if ($2-50 < 0) print($1\"\t\"0\"\t\"$3); else print($1\"\t\"$2-50\"\t\"$3-50)}' "+args.leaderboard[0]+" > "+args.leaderboard[0].replace(".bed",".Left.bed")
	print(command)
	subprocess.call(command,shell=True)
	command="awk '{print($1\"\t\"$2+50\"\t\"$3+50)}' "+args.leaderboard[0]+" > "+args.leaderboard[0].replace(".bed",".Right.bed")
	print(command)
	subprocess.call(command,shell=True)

	command="awk '{if ($2-50 < 0) print($1\"\t\"0\"\t\"$3); else print($1\"\t\"$2-50\"\t\"$3-50)}' "+args.test[0]+" > "+args.test[0].replace(".bed",".Left.bed")
	print(command)
	subprocess.call(command,shell=True)
	command="awk '{print($1\"\t\"$2+50\"\t\"$3+50)}' "+args.test[0]+" > "+args.test[0].replace(".bed",".Right.bed")
	print(command)
	subprocess.call(command,shell=True)

	for f in BAM_files:
		fs=f.split(".")
		for t in bed_files:
			if ("sorted" not in t) and ("Left" not in t) and ("Right" not in t):
				ts=t.split(".")
				if (fs[1] == ts[1]):
					command="bedtools coverage -a "+args.bed[0]+t+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4,5 > "+args.destination[0]+"Training/Center/"+ts[0]+"."+fs[1]+"."+fs[2]+"."+fs[3]+".temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sed -i 's/chr//g' "+args.destination[0]+"Training/Center/"+ts[0]+"."+fs[1]+"."+fs[2]+"."+fs[3]+".temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.destination[0]+"Training/Center/"+ts[0]+"."+fs[1]+"."+fs[2]+"."+fs[3]+".temp.bed > "+args.destination[0]+"Training/Center/"+ts[0]+"."+fs[1]+".Middle."+fs[2]+"."+fs[3]+".bed"
					print(command)
					subprocess.call(command,shell=True)
					command="rm "+args.destination[0]+"Training/Center/"+ts[0]+"."+fs[1]+"."+fs[2]+"."+fs[3]+".temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="bedtools coverage -a "+args.bed[0]+ts[0]+"."+ts[1]+".Left.bed -b "+args.bam[0]+f+" | cut -f 1,2,3,4,5 > "+args.destination[0]+"Training/Left/"+ts[0]+"."+fs[1]+".Left."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sed -i 's/chr//g' "+args.destination[0]+"Training/Left/"+ts[0]+"."+fs[1]+".Left."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.destination[0]+"Training/Left/"+ts[0]+"."+fs[1]+".Left."+fs[2]+"."+fs[3]+"temp.bed > "+args.destination[0]+"Training/Left/"+ts[0]+"."+fs[1]+".Left."+fs[2]+"."+fs[3]+".bed"
					print(command)
					subprocess.call(command,shell=True)
					command="rm "+args.destination[0]+"Training/Left/"+ts[0]+"."+fs[1]+".Left."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="bedtools coverage -a "+args.bed[0]+ts[0]+"."+ts[1]+".Right.bed -b "+args.bam[0]+f+" | cut -f 1,2,3,4,5 > "+args.destination[0]+"Training/Right/"+ts[0]+"."+fs[1]+".Right."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sed -i 's/chr//g' "+args.destination[0]+"Training/Right/"+ts[0]+"."+fs[1]+".Right."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
					command="sort -s -V -k 1,1 -k 2,2 -k 3,3 "+args.destination[0]+"Training/Right/"+ts[0]+"."+fs[1]+".Right."+fs[2]+"."+fs[3]+"temp.bed > "+args.destination[0]+"Training/Right/"+ts[0]+"."+fs[1]+".Right."+fs[2]+"."+fs[3]+".bed"
					print(command)
					subprocess.call(command,shell=True)
					command="rm "+args.destination[0]+"Training/Right/"+ts[0]+"."+fs[1]+".Right."+fs[2]+"."+fs[3]+"temp.bed"
					print(command)
					subprocess.call(command,shell=True)
		if (fs[1] in leaderTissues):
			command="bedtools coverage -a "+args.leaderboard[0]+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Leaderboard/Center/Leaderboard."+fs[1]+"."+fs[2]+".Middle."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
			command="bedtools coverage -a "+args.leaderboard[0].replace(".bed",".Left.bed")+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Leaderboard/Left/Leaderboard."+fs[1]+"."+fs[2]+".Left."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
			command="bedtools coverage -a "+args.leaderboard[0].replace(".bed",".Right.bed")+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Leaderboard/Right/Leaderboard."+fs[1]+"."+fs[2]+".Right."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
		if (fs[1] in testTissues):
			command="bedtools coverage -a "+args.test[0]+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Test/Center/Test."+fs[1]+"."+fs[2]+".Middle."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
			command="bedtools coverage -a "+args.test[0].replace(".bed",".Left.bed")+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Test/Left/Test."+fs[1]+"."+fs[2]+".Left."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
			command="bedtools coverage -a "+args.test[0].replace(".bed",".Right.bed")+" -b "+args.bam[0]+f+" | cut -f 1,2,3,4 > "+args.destination[0]+"Test/Right/Test."+fs[1]+"."+fs[2]+".Right."+fs[3]+".bed"
			print(command)
			subprocess.call(command,shell=True)
	#Computing median coverage for Training Files
	trainingFiles=os.listdir(args.destination[0]+"Training/Center")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
				for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Training/Center/"+str(element)+" "
			outputFile=str(args.destination[0])+"Training/Median/Middle/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Center.Median.Coverage.bed"
			command="Rscript computeMedianCoverageTrain.R "+fileList+" "+outputFile
			print(command)
			subprocess.call(command,shell=True)
				
	trainingFiles=os.listdir(args.destination[0]+"Training/Left")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Training/Left/"+str(element)+" "
			outputFile=str(args.destination[0])+"Training/Median/Left/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Left.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)

	trainingFiles=os.listdir(args.destination[0]+"Training/Right")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Training/Right/"+str(element)+" "
			outputFile=str(args.destination[0])+"Training/Median/Right/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Right.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)

	#Computing median coverage for Leaderboard Files
	trainingFiles=os.listdir(args.destination[0]+"Leaderboard/Center")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Leaderboard/Center/"+str(element)+" "
			outputFile=str(args.destination[0])+"Leaderboard/Median/Middle/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Center.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			print(command)
			subprocess.call(command,shell=True)
			
	trainingFiles=os.listdir(args.destination[0]+"Leaderboard/Left")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Leaderboard/Left/"+str(element)+" "
			outputFile=str(args.destination[0])+"Leaderboard/Median/Left/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Left.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)

	trainingFiles=os.listdir(args.destination[0]+"Leaderboard/Right")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Leaderboard/Right/"+str(element)+" "
			outputFile=str(args.destination[0])+"Leaderboard/Median/Right/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Right.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)


	#Computing median coverage for Test Files
	trainingFiles=os.listdir(args.destination[0]+"Test/Center")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Test/Center/"+str(element)+" "
			outputFile=str(args.destination[0])+"Test/Median/Middle/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Center.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			print(command)
			subprocess.call(command,shell=True)
				
	trainingFiles=os.listdir(args.destination[0]+"Test/Left")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Test/Left/"+str(element)+" "
			outputFile=str(args.destination[0])+"Test/Median/Left/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Left.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)

	trainingFiles=os.listdir(args.destination[0]+"Test/Right")
	usedSet=set()
	for tFile in trainingFiles:
		fittingFile=set()
		stFile=tFile.split(".")
		if (tFile not in usedSet):
			usedSet.add(tFile)
			fittingFile.add(tFile)
			for tFile2 in trainingFiles:
				if (tFile2 not in usedSet):
					if (tFile != tFile2):
						stFile2=tFile2.split(".")
						if (stFile[0:3]==stFile2[0:3]):
							usedSet.add(tFile2)
							fittingFile.add(tFile2)
		if (len(fittingFile)> 0):
			fileList=""
			for element in list(fittingFile):
				fileList+=str(args.destination[0])+"Test/Right/"+str(element)+" "
			outputFile=str(args.destination[0])+"Test/Median/Right/"+stFile[0]+"."+stFile[1]+"."+stFile[2]+".Right.Median.Coverage.bed"
			command="Rscript computeMedianCoverage.R "+fileList+" "+outputFile
			subprocess.call(command,shell=True)



main()

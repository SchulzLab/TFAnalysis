import sys
import os
import argparse

#This script performs post processing of the random forest output. 

#arg1 Path to the random forest classification results for either Leaderboard or Test data.
#arg2 Path to the files holding the intersected data that was not overlapping with any DHS sites
#arg3 Directory where the results should be stored
#arg4 Label which is either L for Leaderboard or F for Finalround submission.


def main():
	parser=argparse.ArgumentParser(prog="Prepare_Predictions_For_Submission.py")
	parser.add_argument("Classification_Results_Non_Zero",nargs=1,help="Path to random forest results classification results produced for Leaderboard or Test data")
	parser.add_argument("Files_Without_DHS",nargs=1,help="Path to the files produced by the Intersect_Bins_And_TF_Predictions.py script holding the regions without DHS sites")
	parser.add_argument("Processed_Files",nargs=1,help="Path to store the processed files to. Subfolders are created automatically")
	parser.add_argument("Round",nargs=1,help="Flag to select the submission round. F for Final round submisisons, L for Leaderboard submissions")
	args=parser.parse_args()

	#Removing duplicate bins from the classified data, taking the highest probability of the duplicated bins as the resulting probability.
	srcdir=args.Classification_Results_Non_Zero[0]
	tardir=args.Processed_Files[0]
	zerodir=args.Files_Without_DHS[0]
	typ=args.Round[0]
	if (typ != "L") and (typ != "F"):
		print ("Invalid value of typ. Either L (Leaderboard) or F (Final Round submission)")
		return 0

	command="mkdir "+tardir
	os.system(command)
	command="mkdir "+tardir+"Non_Zero"
	os.system(command)
	originalFiles=os.listdir(srcdir)
	for f in originalFiles:
		print("Removing duplicate bins in "+f)
		valueDict={}
		infile=open(srcdir+f,"r")
		for l in infile:
			if ("NA" not in l):
				s=l.split()
				key=s[0]+" "+s[1]+" "+s[2]
				if (valueDict.has_key(key)):
					valueDict[key]=max(float(s[3]),valueDict[key])
				else:
					valueDict[key]=float(s[3])
		infile.close()
	
		outfile=open(tardir+"Non_Zero/"+f,"w")
		for key in valueDict.keys():
			ks=key.split()
			outfile.write(ks[0]+"\t"+ks[1]+"\t"+ks[2]+"\t"+str(valueDict[key])+"\n")
		outfile.close()


	#Adding Probabilities of 0.0 to the bin without overlapping DNase data.
	command="mkdir "+tardir+"Zero"
	os.system(command)
	zeroFiles=os.listdir(zerodir)
	for f in zeroFiles:
		print("Adding a probabilities of value 0.0 to "+f)
		original=open(zerodir+f,"r")
		newfile=open(tardir+"Zero/"+f,"w")
		for l in original:
			s=l.split()
			temp=s[0]+"\t"+s[1]+"\t"+s[2]+"\t0.0\n"
			newfile.write(temp)		
		original.close()
		newfile.close()


	#Merging Non-Zero and Zero files, sorting them such that the order fits the format required for scoring.
	print("Generating final output files")
	originalFiles=os.listdir(srcdir)
	command="mkdir "+tardir+typ
	os.system(command)
	for f in originalFiles:
		print("Processing "+f)
		s=f.split("_")
		tissue_f=str(s[1].split(".")[0])
		for t in zeroFiles:
			if (tissue_f in t):
				name=typ+"."+s[0]+"."+tissue_f.replace("HEPG2","HepG2")+".tab"
 				command="cat "+tardir+"Non_Zero/"+f+" "+tardir+"Zero/"+t+" | sort -k 1,1 -k 2,2n -k 3,3n  > "+tardir+typ+"/"+name
				os.system(command)

main()

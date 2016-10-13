import sys
import os
import argparse
from sets import Set

#This script classifies the files in the specified source path using the trained random forest models
#
#
#arg1: Path to the folder containing the trained random forests.
#arg2: Name of the TF for which the predictions should be made.
#arg3: Output folder for the predictions.

def main():
	parser=argparse.ArgumentParser(prog="Predict_TF_Binding.py")
	parser.add_argument("Tissue",nargs=1,help="Path to the TF annotation file on which TF binding should be predicted")
	parser.add_argument("RandomForests",nargs=1,help="Path to the trained random forest models")
	parser.add_argument("TF",nargs=1,help="Name of the TF for which the binding predictions should be made")
	parser.add_argument("Destination",nargs=1,help="Path to write the results to")
	args=parser.parse_args()

	if (not os.path.exists(args.Destination[0])):
		command="mkdir "+args.Destination[0]
		os.system(command)

	command="R3script Internal-Rscripts/Predict_TF_Binding_Using_Random_Forest_Classifiers.R " +args.TF[0]+" "+args.Tissue[0]+" "+args.Destination[0]+args.TF[0]+".txt "+args.RandomForests[0]
	print(command)
	os.system(command)
		
		

main()

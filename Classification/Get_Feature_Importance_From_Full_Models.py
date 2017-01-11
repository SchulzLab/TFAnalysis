import sys
import os
import argparse
from sets import Set

#This script invokes the R-script that extracts the union of the top features that should be used to retrain models on the reduced feature space.
#The randomForest R-Package must be available.
#
#arg1: Path to store the feature importance
#arg2: Path to the integrated files (txt) on full feature space
#arg3: Path to the RData file that should be processed
#arg4: TF that should be analysed

def main():
	parser=argparse.ArgumentParser(prog="Get_Feature_Importance_From_Full_Models.py")
	parser.add_argument("Destination",nargs=1,help="Path to store the feature importance")
	parser.add_argument("Training",nargs=1,help="Path to the integrated files (txt) holding the training data with full feature space")
	parser.add_argument("RDataFile",nargs=1,help="RDataFile that should be processed")
	parser.add_argument("TF",nargs=1,help="Name of the processed TF")

	args=parser.parse_args()

	if (not os.path.exists(args.Destination[0])):
		command="mkdir "+args.Destination[0]
		os.system(command)

	command="R3script Internal-Rscripts/Get_Feature_Importance_From_Full_Models.R "+args.RDataFile[0]+" 20 "+args.TF[0]+" "+args.Training[0]+" "+args.Destination[0]
	print(command)
	os.system(command)

		
		

main()

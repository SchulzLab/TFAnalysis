import sys
import os
import argparse
from sets import Set

#This script invokes the R-script that handles learning of the random forest models on the reduced feature space.
#The randomForest R-Package must be available.
#
#arg1:Path to the RData files to that hold training data on the reduced feature space.
#arg2: Output folder to store the trained random forest models.

def main():
	parser=argparse.ArgumentParser(prog="Train_Random_Forest_Classifiers_Reduced_Feature_Space.py")
	parser.add_argument("Training",nargs=1,help="Path to the RData files holding the training data with reduced feature space")
	parser.add_argument("Destination",nargs=1,help="Path to store the final Random Forest models")
	args=parser.parse_args()

	if (not os.path.exists(args.Destination[0])):
		command="mkdir "+args.Destination[0]
		os.system(command)

	files=os.listdir(args.Training[0])	
	for f in files:
		if ("Features" in f):
			command="R3script Internal-Rscripts/Train_Random_Forest_Models_On_Reduced_Feature_Space.R " + args.Training[0]+f+ " "+args.Training[0]+f.replace("Features","Response")+" "+args.Destination[0]+f.split("_")[0]
			print(command)
			os.system(command)


		
		

main()

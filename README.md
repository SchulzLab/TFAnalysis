# TFAnalysis
This project contains our code used to generate the leaderboard, conference and final round submissions to the _ENCODE DREAM in vivo Transcription Factor Binding Site Prediction Challenge_.
The master branch reflects the code we used for the final round submissions. Tree 53508fd4b0 reflects the state of the code for the conference round.
The following description  is valid for the final round submission only.

##Required software
In order to operate our code on a linux system, the following software must be installed:
- [bedtools](https://github.com/arq5x/bedtools2) (minimum version 2.25.0)
- R (minimum version 3.x.x)
- The _randomForest_ R-package
- Python (minimum version 2.7)
- [TEPIC](https://github.com/SchulzLab/TEPIC)

Note that _TEPIC_  has additional dependencies. A link to the respective repository is included in this project.

##Required data
To run our scripts, the following data from Synapse must be available in decompressed form:
- The file *training_data.ChIPseq.tar*
- The file *training_data.annotations.tar*
- All DNase bam files stored in the [DNase bams folder at synapse](https://www.synapse.org/#!Synapse:syn6176232)

In addition, the human reference genome in fasta format, version *hg19*, must be available. 
Position Frequency Matrices (PFMs), obtained from Jaspar, Hocomoco, and Uniprobe are already included in the _TEPIC_ repository.

##Step by step guide
In the following sections, the usage of our pipeline is described step by step.
Please add a **/** after foldernames in the command line arguments.

###Data preprocessing
####Processing TF ChIP-seq label tsv data
The provided TF ChIP-seq label tsv files are separated by TF and tissue. Further, the training data is balanced by randomly choosing
just as many samples from the unbound class as there are for the bound class. 
Use the script `Preprocessing/Split_and_Balance_ChIP-seq_TSV_files.py` to perform these tasks. 

In the Preprocessing folder, the command line is:
```
python Split_and_Balance_ChIP-seq_TSV_files.py <Folder containing the TF ChIP-seq label tsv files> <Target directory>
```

###Computing DNase coverage in Bins
We compute the DNase coverage in all bins used for training, testing, and the leaderboard data using the python script `Preprocessing/Compute_DNase_Coverage.py`
To compute the coverage, execute the following command in the Preprocessing folder.
```
python Compute_DNase_Coverage.py <Path to the DNase bam files> <Path to the directory containing the balanced ChIP-seq labels> <File containing the leaderboard regions> <File containing the test regions>  <Target directory>
```

We use the _bedtools coverage_ tool to compute the DNase coverage in the bins from the DNase bam files. 
In case that several DNase replicates are available for one tissue, the median coverage over all replicates will be computed. 
This is done by the Rscript `Preprocessing/computeMedianCoverage.R`.
In addition to the actual bins, we compute the DNase coverage for their left and right neighbouring bins. To simplify the merging process later on,
we generate additional files that contain the coordinates of the right and the left bins with respect to the original file and compute the coverage for those bins too.

Note that this computation can take several hours; it also requires at least 500GB of main memory, as some DNase bam files are very large.

###Computing Transcription Factor affinities using TEPIC
Transcription factor binding affinities are calculated using the [TEPIC](https://github.com/SchulzLab/TEPIC) method. 
These affinities will be later used in a random forest model as features to predict the binding of a distinct TF.
*TEPIC* has to be started manually on all labelled ChIP-seq bed files as well as on the leaderboard and test data bins.
Please check the TEPIC repository for details on the method. 

Starting TEPIC as follows produces all files for one TF which are necessary for its further processing:
```
bash TEPIC.sh -g <Reference genome> -b <Bed file> -o <Prefix of the output files (including the path)> -p <Position frequency matrices> -c <Number of cores>
```

###Merging Transcription Factor affinities and DNase data for Model training.
We provide a Python script to combine the TEPIC annotations with the DNase coverage data:
`Preprocessing/IntegrateTraining.py`

To integrate the Test data, use the following command in the Preprocessing folder:
```
python IntegrateTraining.py <Path to the TEPIC annotations of the training data> <Path to the DNase coverage data for the middle bins> <Path to the DNase coverage data for the left bins> <Path to the DNase coverage data for the right bins> <Target directory>
```
The files `Preprocessing/headerC.txt`, `Preprocessing/headerC_TL.txt`,`Preprocessing/headerL.txt`, and `Preprocessing/headerR.txt` are required to generate the correct headers while merging the data. 
Both leaderboard data and test data will be integrated later.


###Predicting Transcription Factor binding in bins using the full feature set
####Step 1.1 Generating RData files
Before the random forest models can be trained, the training data files need to be reformatted. 
To shorten the time required for loading the data, the reformatted data is stored as a RData file.
This is done by the script `Preprocessing/Dump_Training_Data_As_RData.R`.

The command to run the script is:
```
Rscript Dump_Training_As_RData.R <Folder holding the subfolders with the training data for all TFs> <Target directory for the RData files>
```
####Step 1.2 Training Random Forests
To train the random forests, the script `Classification/Train_Random_Forest_Classifiers_Full_Feature_Space.py` can be used.

We learn 4500 trees and use the default values for cross validation. 
We had to reduce the amount of training data to 30,000 bound and unbound samples of each class to make the learning feasible in terms of memory usage and
Fortran memory limitations.

The command is:
```
python Train_Random_Forest_Classifiers_Full_Feature_Space.py  <Folder containing the RData files containing features with the full feature space, produced in Step 1.1> <Target directory to store the output>
```
Due to space constraints, we can not use the full feature space for predictions on leaderboard and test data. 
Therefore, we use the feature importance of the learned models to determine which features should be used subsequently.
For each tissue that is avaiable as a training data set, we consider the top 20 features. The union of those will be used later to learn a model for that particular TF.
This script learns the models on all RData files that are present in the given directory.

###Determine the top features
To determine the top features, use the script `Classification/Get_Feature_Importance_From_Full_Models.py`.
The features are extracted from the RFs trained in Step 1.2.

The command is:
```
python Get_Feature_Importance_From_Full_Models.py <Target directory> <Path to the integrated files (txt) on full feature space> <Path to the RData file that should be processed> <Name of the TF that should be analysed>
```
Note that this must be called individually on all RData files and TFs for which the reduced feature space should be produced.

###Shrink the feature space
We use the files containing the top TFs to generate the final TF features for our models. We have three scripts to extract the suitable
data from training, leaderboard and test files: `Preprocessing/CutTrainingData.py`, `Preprocessing/CutLeaderboardData.py` , `Preprocessing/CutTestData.py`

To shrink the training data run the following command in the Preprocessing folder:
```
python CutTrainingData.py <Path to the complete TF annotations used for training> <Path to the files containing the TFs that should be kept> < Target directory>
```

To generate the TF data for the leaderboard round run the following command:
```
python CutLeaderboardData.py <Path containing the complete TF annotation of the leaderboard data> <Path to the files containing the TFs that should be kept> < Target directory>
```

To generate the TF data for the final round run the following command:
```
python CutTestData.py <Path containing the complete TF annotation of the test data> <Path to the files containing the TFs that should be kept> < Target directory>
```

###Merge TF annotations and DNase data for Training data, Leaderboard data, and Test data
Before we can retrain the models and apply them to the Leadeboard and the Test data, we have to merge the TF affinities and the DNase data again.
We provide three individual Python scripts to combine the TEPIC annotations with the DNase coverage data:
`Preprocessing/IntegrateTraining.py`, `Preprocessing/IntegrateLeaderboard.py`, `Preprocessing/IntegrateTest.py`

To integrate the new Training data, use the following command in the Preprocessing folder:
```
python IntegrateTraining.py <Path to the reduced TEPIC annotations of the training data> <Path to the DNase coverage data for the middle bins computed in the training regions> <Path to the DNase coverage data for the left bins computed in the training regions> <Path to the DNase coverage data for the right bins computed in the training regions> <Target directory>
```

To integrate the Leaderboard data, use the following command in the Preprocessing folder:
```
python IntegrateLeaderboard.py <Path to the reduced TEPIC annotations of the leaderboard data> <Path to the DNase coverage data for the middle bins computed in the leaderboard regions> <Path to the DNase coverage data for the left bins computed in the leaderboard regions> <Path to the DNase coverage data for the right bins computed in the leaderboard regions> <Target directory>
```

To integrate the Test data, use the following command in the Preprocessing folder:
```
python IntegrateTest.py <Path to the reduced TEPIC annotations of the test data> <Path to the DNase coverage data for the middle bins computed in the test regions> <Path to the DNase coverage data for the left bins computed in the training regions> <Path to the DNase coverage data for the right bins computed in the test regions> <Target directory>
```

###Computing maximisied TF features
In addition to shrink the feature space, we found that the performance of the random forests are improved when one considers the maximum affinity value for a TF in all adjacent bound training samples instead of the original values.
This transformation is performed by the script `Preprocessing/ConvertTrainingDataToMaxAffinityFormat.py`.

The command line to run this script is:
```
python ConvertTrainingDataToMaxAffinityFormat.py <Path to the shrunken, integrated, Training data sets> <Target directory>
```

Similar to the maximum affinity transformation we perform on the Training data, we also reprocessed the Leaderboard and Test data. 
Here, for a center bin _i_ we determine a new value by searching for the maximum value in the 2 upstream bins _i-2_, _i-1_, in the downstream bins _i+1_, and  _i+2_ as well as in bin 
_i_ itself.

This is done using a first in first out queue in the script `Preprocessing/ConvertMaxLeaderboardTest.py`
```
python ConvertMaxLeaderboardTest.py <Path to either the shrunken, integrated, Test or Leaderboard Files> <Target directory>
```
Note that this script runs about 14 hours on the test data.

###Retrain the models
####Step 2.1 Generating RData files
As above, before the random forest models can be trained, the training data files need to be reformatted and RData files are created.
Again, this is done by the script `Preprocessing/Dump_Training_Data_As_RData.R`.

The command to run the script is:
```
Rscript Dump_Training_As_RData.R <Folder holding the subfolders with the shrunken training data for all TFs> <Target directory for the RData files>
```

####Step 2.2 Learn models
To train the random forests, the script `Classification/Train_Random_Forest_Classifiers_Reduced_Feature_Space.py` can be used.
We use the same parameteres as above.

The command is:
```
python Train_Random_Forest_Classifiers_Reduced_Feature_Space.py <Folder containing the RData files produced in Step 2.1> <Target directory to store the learned models>
```
This learns models for all RData files that are present in the given directory.

###Apply them to Leaderboard data and Test data
To make predictions on the leaderboard and test data sets, the script `Classification/Predict_TF_Binding.py` can be used. 
This scripts has to be started manually for all files that should be classified.

The command to run the script for one such file is:
```
python Predict_TF_Binding.py <File to be classified> <Folder containing the trained random forest models from Step 2.2> <Name of the TF for which binding should be predicted> <Target directory to store the predictions> 
```

###Preparing data for submission
In order to reformat the data such that it sufficies the requirements of the challenge, the classification results are reformatted using the script 
`Postprocessing/Submission_Format.bash`.
Here, the data is sorted, renamed and stored according to the challenge conventions.

The command to run the script is:
```
bash Submission_Format.bash <TF name> <Tissue name> <File to reformat> <F for Final round submission, L for Leaderboard submission>
```
##Contact
Please contact *fbejhati[at]mmci.uni-saarland.de* or *fschmidt[at]mmci.uni-saarland.de* in case of questions.

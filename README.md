# TFAnalysis
This project contains our code used to generate the conference round submissions to the _ENCODE DREAM in vivo Transcription Factor Binding Site Prediction Challenge_.

##Required software
In order to operate our code on a linux system, the following software must be installed:
- [bedtools](https://github.com/arq5x/bedtools2)
- R (minimum version 3.x.x)
- The _randomForest_ R-package
- Python (minimum version 2.7)
- [TEPIC](https://github.com/SchulzLab/TEPIC)
- [JAMM](https://github.com/mahmoudibrahim/JAMM/releases) version 1.0.7.2
Note that _TEPIC_ and _JAMM_ have additional dependencies. Links to the respective repositories are set up in this project.

##Required data
To run our scripts, the following data from synapse must be available:
- The file *training_data.ChIPseq.tar*
- The file *training_data.DNASE_wo_bams.tar*
- The file *training_data.annotations.tar*
- All DNase bam files stored in the [DNase bams folder at synapse](https://www.synapse.org/#!Synapse:syn6176232)

In addition, the human reference genome in fasta format, version *hg19* must be available. All required Position Frequency Matrices are included in the _TEPIC_ repository.
##Step by step guide
###Data preprocessing

###Computing Transcription Factor affinities using TEPIC

###Predicting Transcription Factor binding in bins

###Preparing the data for submission

##References

##Contact

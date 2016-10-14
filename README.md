# TFAnalysis
This project contains our code used to generate the conference round submissions to the _ENCODE DREAM in vivo Transcription Factor Binding Site Prediction Challenge_.

##Required software
In order to operate our code on a linux system, the following software must be installed:
- [bedtools](https://github.com/arq5x/bedtools2) (minimum version 2.25.0)
- R (minimum version 3.x.x)
- The _randomForest_ R-package
- Python (minimum version 2.7)
- [TEPIC](https://github.com/SchulzLab/TEPIC)
- [JAMM](https://github.com/mahmoudibrahim/JAMM/releases) version 1.0.7.2

Note that _TEPIC_ and _JAMM_ have additional dependencies. Links to the respective repositories are set up in this project.

##Required data
To run our scripts, the following data from Synapse must be available:
- The file *training_data.ChIPseq.tar*
- The file *training_data.DNASE_wo_bams.tar*
- The file *training_data.annotations.tar*
- All DNase bam files stored in the [DNase bams folder at synapse](https://www.synapse.org/#!Synapse:syn6176232)

In addition, the human reference genome in fasta format, version *hg19*, must be available. A corresponding [genome size file](Preprocessing/Genome_Size_File_For_JAMM.txt), required by *JAMM*,
is included in the *Preprocessing* folder. 
Position Frequency Matrices (PFMs), obtained from Jaspar, Hocomoco, and Uniprobe are already included in the _TEPIC_ repository.

##Step by step guide
In the following sections, the usage of our pipeline is described step by step.

###Data preprocessing

####Processing TF ChIP-seq label tsv data
The provided TF ChIP-seq label tsv files have to separated by TF and tissue. Further, the training data is balanced by randomly choosing
just as many samples from the unbound class as there are for the bound class. 
Use the script `Preprocessing/Split_and_Balance_ChIP-seq_TSV_files.py` to perform these tasks. 

In the Preprocessing folder, the command line is:
```
python Split_and_Balance_ChIP-seq_TSV_files.py <Folder containing the TF ChIP-seq label tsv files> <Target directory>
```

####Identifiying DNase hypersensitive sites using JAMM
#####Step 1
To run *JAMM* the DNase bam files have to be converted to bed files. As we do not use the replicate mode of JAMM, but call peaks in all available samples
independently, the bed files have to be distributed in individual folders. This task is carried out by the script `Preprocessing/Convert_Bam_To_Bed.py`.
This script uses the *bamToBed* tool of *bedtools*.

In the Preprocessing folder, the command line is:
```
python Convert_Bam_To_Bed.py <Folder containing the DNase Bam files> <Target directory>
```

#####Step 2
To start the actual peak calling, the script `Preprocessing/Call_DHS_Peaks_using_JAMM.py` can be used. Note that you have to put this script either in the *JAMM* folder
or the script `JAMM.sh` must be in your path. 

To run this script, use the command:
```
python Call_DHS_Peaks_using_JAMM.py <Target directory used in Convert_Bam_To_Bed.py> <Target directory for the peak calls> <Genome size file> <Number of corse to use (default 4)>
```

#####Step 3
Once the peak calling using *JAMM* is finished, the individual peak calls per tissue have to be merged and stored in one file. This can be achieved by running the script
`Preprocessing/Combine_DHS_Peaks.py`. Note that the script has to be started manually for all tissues. Merging the peaks is done by the *bedtools* *merge* command. 

The command line for this tool is:
```
python Combine_DHS_Peaks.py <Output folder for the merged peak set of the tissue of interest> <1th peak file of the tissue of interest> ... <nth peak file of the tissue of interest>
```

###Computing Transcription Factor affinities using TEPIC
####Step 1
Transcription factor binding affinities are calculated using the [TEPIC](https://github.com/SchulzLab/TEPIC) method. This has to be started manually on all files containing the merged DHS sites.
Please check the TEPIC repository for details on the method. 

An example call how TEPIC can be started is:
```
bash TEPIC.sh -g <Reference genome> -b <Merged DHS bed file> -o <Prefix of the output files (including the path)> -p <Position Frequency matrices> -c <Number of cores>
```

####Step 2
The output of TEPIC needs to be transformed to a bed file like structure. In addition, the files containing the DNaseI coverage in DHS sites and the unscaled TF affinities have to be merged to one file.
This is done by the script `Preprocessing/Prepare_TEPIC_Output_For_Intersection.py`.

The command to run the script is:
```
python Prepare_TEPIC_Output_For_Intersection.py <Folder containing the output files of TEPIC>
```

####Step 3
Before Transcription Factor (TF) binding can be predicted, the merged TF scores calcuated in DHS sites identified by JAMM have to be intersected with the binned training, leaderboard, and test data sets.
This can be done by running the script `Preprocessing/Intersect_Bins_And_TF_Predictions.py`. 
Using *bedtools* *intersect* and the *left outer join* option, each bin will be assigned to the corresponding TF affinities computed within the intersecting DHS.

The command to run the script is:
```
python Intersect_Bins_And_TF_Predictions.py <Folder holding TF affinities in bed format> <Folder containing the balanced training regions of all tissues and TFs> <Bed file holding the leaderboard regions as provided on synapse> <Bed file holding the test regions as provided on Synapse> <Target directory to write the intersected files to>
```

###Predicting Transcription Factor binding in bins


###Preparing the data for submission


##References


##Contact

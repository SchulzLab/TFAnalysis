############################################################################################################
############################################################################################################
### Prepare the prediction files for the DREAM challenge submission
## arg1: The TF name, e.g, JUND
## arg2: The tissue name, e.g, HepG2
## arg3: The path to the file that should be reformatted.
## arg4: Flag indicating whether predictions are made for final submission or leaderboard round.
## The resulting file is stored in the directory where this script has been invoked.
############################################################################################################
############################################################################################################
#! /bin/bash
TF=$1
tissue=$2
path=$3
flag=$4
sed 's/\:/\t/' $path | sed 's/-/\t/' | awk '{print "chr"$1"\t"$2"\t"$3"\t"$4}' | sort -k 1,1 -k 2,2n > $flag"."$TF"."$tissue".tab"
gzip $flag"."$TF"."$tissue".tab"

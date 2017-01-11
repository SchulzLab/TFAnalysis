## This script extracts the top features from the models learned before in Train_Random_Forest_Models_On_Full_Feature_Space.R. 

## args[1]: RData File produced by Train_Random_Forest_Models_On_Full_Feature_Space.py
## args[2]: Numer of top features to be considered
## args[3]: TF that should be analysed
## args[4]: Path to the integrated files (txt) on full feature space
## args[5]: Output path

args <- commandArgs(trailingOnly=T)
input <- args[1]
topTFs <- args[2]
TF <- args[3]
path2tissues <- args[4]
Output<-args[5]
output<-paste(Output,TF,sep="")
tissues <- list.files(path=paste(path2tissues,TF,"/",sep=""))

exist.var <- function(ls_files,var){
  return(length(which(ls_files == var)))
}

topTFs <- as.numeric(topTFs)
load(input)
if(topTFs == 0)
  topTFs <- max(sapply(seq(length(rfs)),function(i)length(rfs[[i]]$importance)))
ls_files <- ls()
ensemble_falg <- length(final_rfs)
ensemble_confusion <- NULL
if(ensemble_falg){
  ensemble_confusion <- final_rfs[[1]]$confusion
  ensemble_importance <- final_rfs[[1]]$importance
}

tissue.cnt <- length(rfs)
indiv_confusion <- NULL
indiv_importance <- matrix(NA,ncol=tissue.cnt,nrow=topTFs)
tissue.names <- NULL
all.TFs <- NULL
for(i in seq(tissue.cnt)){
    ord <- order(rfs[[i]]$importance,decreasing=T)
    tissue <- unlist(strsplit(tissues[i],split="\\."))[2]
    tissue.names <- c(tissue.names,tissue)
    all.TFs <- c(all.TFs,names(rfs[[i]]$importance[ord[seq(topTFs)],1]))
    indiv_importance[,i] <- paste(names(rfs[[i]]$importance[ord[seq(topTFs)],]),rfs[[i]]$importance[ord[seq(topTFs)],1],sep="*__*")
  }
table.TFs <- table(all.TFs)
common.TFs <- names(table.TFs[table.TFs > 1])
unique.TFs <- names(table.TFs[table.TFs == 1])

writeLines(text=as.character(unique(all.TFs)),paste(output,"_union_top_",topTFs,"TFs.txt",sep=""))

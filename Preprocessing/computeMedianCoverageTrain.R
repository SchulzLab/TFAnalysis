args<-commandArgs(TRUE)

#This script computes the median coverage values over the replicates of a certain tissue.
#It is called internally in Compute_DNase_CoverageMedian.py

data<-list(list())
argSize<-length(args)
output<-args[argSize]
medianVector<-c()
for (i in c(1:(argSize-1))){
	data[[i]]<-read.table(args[i],header=FALSE,stringsAsFactors=FALSE)
	medianVector<-cbind(medianVector,data[[i]][,5])
}
medianData<-cbind(data[[1]][,1:4],apply(medianVector,1,median))
write.table(medianData,file=output,quote=FALSE,row.names=FALSE,col.names=FALSE)

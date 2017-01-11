#This script is used to compute TF binding predictions on leaderboard and on test data using the RF models learned on the reduced feature space. 
#args1 Name of the TF that should be predicted.
#args2 Name of the test data file. 
#args3 Name of the output file.
#args4 Path to load the random forest models from.


args <- commandArgs(T)
tf_name <- args[1]
tf_test_path <- args[2]
out_path <- args[3]
rfs_path <- args[4]

################################# Function ###############################
##########################################################################
accuracy <- function(conf.mat){
  conf.mat <- conf.mat[c(1,2),c(1,2)]
  return((conf.mat[1,1] + conf.mat[2,2])/(sum(conf.mat)))
}
##########################################################################
trimLine <- function(l){
  tokens <- strsplit(l,"\t")[[1]]
  line.numeric <- as.numeric(tokens[-c(1,2,3)])
  if(length(which(is.na(line.numeric))) > 0)
    return(list(reg=tokens[c(1,2,3)],features=rep(0,times=length(line.numeric))))
  return(list(reg=tokens[c(1,2,3)],features=line.numeric))

}
##########################################################################
trimLine2 <- function(l){
  tokens <- strsplit(l,"\t")[[1]]
  line.numeric <- as.numeric(tokens[-c(1,2,3)])
  if(length(which(is.na(line.numeric))) > 0)
    return(rep(0,times=length(line.numeric)))
  return(line.numeric)

}
##########################################################################
get_predictions <- function(trainedRFs,data_X,fTFs.cnt,i){
  library(parallel)
  allResps <- NULL
  tiss.cnt <- length(trainedRFs)
  preds_across_models <- NULL
  if(F){
   for(m in seq(tiss.cnt)){
    pred <- predict(object=trainedRFs[[m]],newdata=data_X,type="prob")
    preds_across_models <- cbind(preds_across_models,pred[,2])
  	}
   }
  preds_across_models_list <- mclapply(trainedRFs,function(rfs){
    pred <- predict(object=rfs,newdata=data_X,type="prob")[,2]
  },mc.cores=32)
  preds_across_models <- matrix(unlist(preds_across_models_list),ncol=length(preds_across_models_list),byrow=F)
  allPreds <- preds_across_models
  
  print(paste("allPreds",dim(allPreds)))
  print(names(allPreds))
  return(list(allPreds=allPreds))
}
##########################################################################
get_best_RF <- function(rfs){
  best_RF <- NULL
  best.acc <- Inf
  for(i in seq(length(rfs))){
    acc <- accuracy(rfs[[i]]$confusion);
    if(best.acc > acc){
      best_RF <- rfs[[i]];
      best.acc <- acc;
    }
  }
  return(best_RF)
}
##########################################################################
process_and_predict_testFile = function(filepath){
  con = file(filepath, "r")
  d <- system(paste("wc -l",filepath),intern=T)
  preAloc <- as.numeric(strsplit(d,split=" ")[[1]][1]) - 1###The file contained header
  tissue.cnt <- length(rfs)
  ensemble_pred <- matrix(NA,nrow=preAloc,ncol=2)
  x <- read.table(filepath,header=T,stringsAsFactors=F)#,nrow=10^5)
  n <- nrow(x)
  pred <- NULL
  print(paste("Done reading",filepath))
  test_data <- list(reg=rownames(x),features=as.matrix(x))
  print(c("test_data$features",dim(test_data$features)))

  if(length(final_rfs) > 0){
    maxLines <- 10^5
    chunks <- seq(1,n,by=maxLines)
    for(i in seq(length(chunks))){
      start.idx <- chunks[i]
      end.idx <- start.idx + maxLines -1
      if(end.idx > n){
        end.idx <- n
      }
      intermediate_pred <- get_predictions(rfs,test_data$features[seq(start.idx,end.idx),],fTFs.cnt,1)
      ensemble_pred[seq(start.idx,end.idx),] <- predict(final_rfs[[1]],intermediate_pred$allPreds,type="prob")
    }
    res <- cbind(test_data$reg,ensemble_pred[,1])
    return(res)
  }
  pred <- vector(mode="numeric",length=preAloc)
  rf <- rfs[[1]]
  maxLines <- 10^5
  chunks <- seq(1,n,by=maxLines)
  for(i in seq(length(chunks))){
    start.idx <- chunks[i]
    end.idx <- start.idx + maxLines -1
    if(end.idx > n){
      end.idx <- n
    }
    pred[seq(start.idx,end.idx)] <- predict(rf,test_data$features[seq(start.idx,end.idx),],type="prob")[,1]
  }
  res <- cbind(test_data$reg,pred)
  return(res)
}
##########################################################################
process_and_predict_testFile2 = function(filepath,rf) {
  con = file(filepath, "r")
  d <- system(paste("wc -l",filepath),intern=T)
  preAloc <- as.numeric(strsplit(d,split=" ")[[1]][1])
  res <- matrix(NA,nrow=preAloc,ncol=4)
  i <- 1
  while( T ){
      line = readLines(con, n = 1)
      if ( length(line) == 0 ) {
              break
          }
      if(i == 1){
        i <- i + 1
        next;### first line is the header line
      }
      test_data <- trimLine(line)
      if(sum(abs(test_data$features)) == 0){
        res[i] <- 0;
        i <- i + 1;
        next;
      }
      pred <- predict(rf,test_data$features,type="prob")
      res[i,] <- c(test_data$reg,pred[1,1])
      i <- i + 1
      if(i %% 10^6 == 0)
        print(i)
    }
    close(con)
    return(res)
}
##########################################################################
##########################################################################
##########################################################################

tf_rf_path <- Sys.glob(paste(rfs_path,tf_name,"*4500*.RData",sep=""))
load(tf_rf_path)
print(ls())
library(randomForest)
print(rfs[[1]]$confusion)
preds <- process_and_predict_testFile(tf_test_path)
write.table(preds,out_path,sep="\t",quote=F,row.names=F,col.names=F)

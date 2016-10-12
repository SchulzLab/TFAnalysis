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
process_and_predict_testFile = function(filepath,rf) {
  x <- read.table(filepath,header=F,skip=1)
  n <- nrow(x)
  colnames(x) <- NULL
  pred <- NULL
  print(paste("Done reading",filepath))
  #test_data <- sapply(seq(nrow(x)),function(i)trimLine(x[i,]))
  test_data <- list(reg=x[,c(1,2,3)],features=x[,-c(1,2,3)])
  print(c("test_data$features",dim(test_data$features)))
  maxLines <- 500*10^3
  chunks <- seq(1,n,by=maxLines)
  for(i in seq(length(chunks))){
    start.idx <- chunks[i]
    end.idx <- start.idx + maxLines -1
    if(end.idx > n){
      end.idx <- n
    }
    pred <- rbind(pred,predict(rf,test_data$features[seq(start.idx,end.idx),],type="prob"))
  }
  res <- cbind(test_data$reg,pred[,1])
  return(res)
}

##########################################################################
process_and_predict_testFile2 = function(filepath,rf) {
  con = file(filepath, "r")
  d <- system(paste("wc -l",filepath),intern=T)
  preAloc <- as.numeric(strsplit(d,split=" ")[[1]][1])
  print(c("preAloc",preAloc))
  #preAloc <- 8*10^6
  res <- matrix(NA,nrow=preAloc,ncol=4)
  #res <- vector(mode="numeric",length=preAloc)
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
      #res[i] <- pred
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

tf_rf_path <- Sys.glob(paste(rfs_path,tf_name,"*",sep=""))
print(tf_rf_path)
load(tf_rf_path)
print(ls())
library(randomForest)
rf <- get_best_RF(rfs)
print(rf$confusion)
preds <- process_and_predict_testFile(tf_test_path,rf)
print("Done predicting. Starting to write the data.")
write.table(preds,out_path,sep="\t",quote=F,row.names=F,col.names=F)
#writeLines(as.character(preds),out_path)

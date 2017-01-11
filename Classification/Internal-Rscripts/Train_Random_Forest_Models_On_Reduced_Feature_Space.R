## This script is used to learn RF models on the reduced feature space
############################
## args[1]: path to features
## args[2]: path to response
## args[3]: Output path
############################
args<-commandArgs(TRUE)
ntree <- 4500
set.seed(1)
#################################################################################
################################### FUNCTIONS ###################################
#################################################################################
generate_X <- function(dim1,dim2,param1,param2,rand_fun){
  mat <- matrix((do.call(rand_fun,list(dim1*dim2,param1,param2))),nrow=dim1,ncol=dim2,byrow = T)
  return(mat)
}

generate_Y <- function(len){
  return(round(runif(len,0,1)))
}
#################################################################################

#################################################################################
################################### FUNCTIONS ###################################
#################################################################################
library(parallel)
library(randomForest)
RF_all_tissues <- function(data_X,data_Y,fTFs.cnt,i){
  if(class(data_X[[i]]) == "list")
    tiss.cnt <- length(data_X[[i]])
  else
    tiss.cnt <- 1
  all.rfs <- list()
  for(j in seq(tiss.cnt)){
    rf <- randomForest(y=as.factor(data_Y[[i]][[j]]),x=data_X[[i]][[j]],ntree=ntree)
    all.rfs[[j]] <- rf
  }
  return(all.rfs)
}
#################################################################################
RF_all_tissues_parallel <- function(data_X,data_Y,fTFs.cnt,i){
  if(class(data_X[[i]]) == "list")
    tiss.cnt <- length(data_X[[i]])
  else
    tiss.cnt <- 1
  cluster <- makeCluster(tiss.cnt,"FORK")
  all.rfs <- list()
  all.rfs <- parLapply(cluster,seq(tiss.cnt),function(j){
    rf <- randomForest(y=as.factor(data_Y[[i]][[j]]),x=data_X[[i]][[j]],ntree=ntree)
  })
  return(all.rfs)
}
#################################################################################
RF_all_fTFs <- function(data_X,data_Y,fTFs.cnt){
  tiss.cnt <- length(data_X[[1]])
  allfTF.rfs <- list()
  cluster <- makeCluster(tiss.cnt,"FORK")
  allfTF.rfs <- parLapply(cluster,seq(tiss.cnt),function(i){
    RF_all_tissues(data_X,data_Y,fTFs.cnt,1)
  })
  return(allfTF.rfs)
}
#################################################################################
combine_classifiers <- function(pred_mat,resp){
  return(randomForest(y=as.factor(resp),x=pred_mat))
}
#################################################################################
get_predictions <- function(trainedRFs,data_X,data_Y,fTFs.cnt,i){
  all <- NULL
  allPreds <- NULL
  allResps <- NULL
  if(class(data_X[[i]]) == "list")
    tiss.cnt <- length(data_X[[i]])
  else
    tiss.cnt <- 1
  for(t in seq(tiss.cnt)){
    preds_across_models <- NULL
    for(m in seq(tiss.cnt)){
      pred <- predict(object=trainedRFs[[m]],newdata=data_X[[i]][[t]],type="prob")
      preds_across_models <- cbind(preds_across_models,pred[,2])
    }
    allPreds <- rbind(allPreds,preds_across_models)
    allResps <- c(allResps,data_Y[[i]][[t]])
  }
  return(list(allPreds=allPreds,allResps=allResps))
}
#################################################################################
#################################################################################
removeFaultySamples <- function(x,y){
  sums <- rowSums(abs(x))
  zeros <- which(sums == 0)
  faulties <- which(y[zeros] == "B")
  if(length(faulties) == 0)
    return(list(X=x,Y=y))
  return(list(X=x[-faulties,],Y=y[-faulties]))
}
#################################################################################
#################################################################################
print(paste("Loading features",args[1]))
load(file=args[1])
print(paste("Loading response",args[2]))
load(file=args[2])
print("Data completly loaded")
shrunk_X <- list();shrunk_Y <- list()
test_X <- list();test_Y <- list()
for(i in seq(length(allfTFs_X))){
  x <- list()
  y <- list()
  x_test <- list()
  y_test <- list()
    if(class(allfTFs_X[[i]]) == "list"){
        for(j in seq(length(allfTFs_X[[i]]))){
          filtered <- removeFaultySamples(allfTFs_X[[i]][[j]],allfTFs_Y[[i]][[j]])
          X <- filtered$X
          Y <- filtered$Y
          print(dim(X))
          y_B <- which(Y == "B");
          y_U <- which(Y == "U");


          nonTrivialUnbounds <- which(rowSums(X[y_U,]) > 0)
          shrink_U <- shrink_B <- 30000

          if(length(y_B) < shrink_B){
            print("the specified shrinkage factor causes array out of boundary problem. The length(y_B) is taken for the shrinking factor instead!")
            shrink_B <- length(y_B)
          }
          if(length(nonTrivialUnbounds) < shrink_U){
            print("the specified shrinkage factor causes array out of boundary problem. The length(y_U) is taken for the shrinking factor instead!")
            shrink_U <- length(nonTrivialUnbounds)
          }
          shrink_idx <- c(y_B[seq(shrink_B)],y_U[nonTrivialUnbounds[seq(shrink_U)]])
          x[[j]] <- X[shrink_idx,];
          y[[j]] <- Y[shrink_idx];
          x_test[[j]] <- X[-shrink_idx,];
          y_test[[j]] <- Y[-shrink_idx];

        }
    }else{
          filtered <- removeFaultySamples(allfTFs_X[[i]],allfTFs_Y[[i]])
          X <- filtered$X
          Y <- filtered$Y
          y_B <- which(Y[[i]] == "B");
          y_U <- which(Y[[i]] == "U");
          shrink_U <- shrink_B <- 30000
          if(length(y_B) < shrink_B){
            print("the specified shrinkage factor causes array out of boundary problem. The length(y_B) is taken for the shrinking factor instead!")
            shrink_B <- length(y_B)
          }
          if(length(nonTrivialUnbounds) < shrink_U){
            print("the specified shrinkage factor causes array out of boundary problem. The length(y_U) is taken for the shrinking factor instead!")
            shrink_U <- length(nonTrivialUnbounds)
          }
          shrink_idx <- c(y_B[seq(shrink_B)],y_U[nonTrivialUnbounds[seq(shrink_U)]])
          x[[i]] <- X[[i]][shrink_idx,];
          y[[i]] <- Y[[i]][shrink_idx];
          x_test[[j]] <- X[-shrink_idx,];
          y_test[[j]] <- Y[-shrink_idx];
      }
      shrunk_X[[i]] <- x;
      shrunk_Y[[i]] <- y;
      test_X[[i]] <- x_test
      test_Y[[i]] <- y_test
}

################################################################################
################################################################################
data_X <- shrunk_X
data_Y <- shrunk_Y
save(test_X,test_Y,file=paste(args[3],"_test.RData",sep=""))
fTFs.cnt <- length(data_X)
print("Learning tissue specific RFs")
rfs <- RF_all_tissues(data_X,data_Y,fTFs.cnt,1)
class(rfs)
final_rfs <- list()
if(length(data_X[[1]]) > 1){##If there are more than one tissue for the input flag TF, perform the combine_classifier
  all.TFs.preds <- get_predictions(rfs,new_data_X,data_Y,fTFs.cnt,i)
  print("Learning Ensemble RF")
  final_rfs[[i]] <- combine_classifiers(all.TFs.preds$allPreds,all.TFs.preds$allResps)
}
outputPath <- strsplit(args[3],".RData")
outputPath <- paste(args[3],"_",ntree,"_U_",shrink_U,"_B_",shrink_B,"_MaxBin.RData",sep="")
save(rfs,final_rfs,file=outputPath)
################################################################################
################################################################################

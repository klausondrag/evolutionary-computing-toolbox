library(ggplot2)
library(plyr)
library(dplyr)
library(stringr)

# Set number of generations
gens = 50

# Give appropriate labels
measures_names = c("branching","connectivity1","connectivity2","coverage","effective_joints","length_ratio","sensors","symmetry","total_components")
measures_labels = c("Branching","Limbs","Length limbs","Coverage","Joints","Proportion","Sensors","Symmetry","Size")

# Set wds
setwd(getwd())
outputfolder = paste(getwd(),"/graphs", sep="")
dir.create(file.path(outputfolder), showWarnings = T)
dirs <-list.dirs(recursive = F)
dirs = dirs[-length(dirs)]
numdir = length(dirs)

# Initialize final dataframe
final.df <- NULL

# Loop through directories to get 
for(dir in dirs) {
  df = read.table(paste(dir,"/measures.txt", sep = ""),header=T)
  id = c()
  fitness = c()
  for(i in c(1:gens)) {
    curGen = paste(dir,"/offspringpop",i,sep="")
    files = list.files(curGen, "fitness_")
    for(file in files) {
      filePath <- paste(curGen, "/", file,sep="")
      id <- append(id,as.numeric(gsub("\\D", "", file)))
      fitness <- append(fitness,read.table(filePath)[[1]])
    }
  }
  fitness.df <- data.frame(id,fitness)
  colnames(fitness.df) <- c("idgenome","fitness")
  df <- merge(df,fitness.df, by="idgenome",all.x = T)
  if(!is.null(final.df)) {
    final.df <- rbind(final.df, df)
  } else {
    final.df <- df
  }
}


###

# Set experiment number for merging
final.df$exp = c(1:length(final.df$idgenome))
final.df$exp = final.df$exp %/% (length(final.df$idgenome) / numdir) + 1

# Get id's of all selected bodies with fitness
allfiles = c()
for(dir in dirs) {
  # Get names of selected individuals per experiment
  for(i in c(1:gens)) {
    curGen = paste(dir, "/selectedpop", i, sep="")       #selectedpop
    files = list.files(curGen, "body_")
    allfiles = c(allfiles, files)
  }
}

# Strip ids from strings
selected = data.frame()
for(row in c(1:length(allfiles))) {
  id = as.integer(str_split(allfiles[row], "[:punct:]")[[1]][2])
  selected = rbind(selected, id)
}

# Extract all selected data
selected = cbind(selected, c(1:nrow(selected)))
colnames(selected) = c("idgenome", "exp #")
selected$expr = selected$expr %/% (nrow(selected)/numdir)+ 1

# Merge selected data with fitness values
selectedFitness.df = data.frame()
for(exp in c(1,2,3)) {
  x = merge(selected[which(selected$expr == exp),], final.df[which(final.df$exp == exp),], by= "idgenome")
  selectedFitness.df = rbind(selectedFitness.df, x)
}

#selectedFitness.df = selectedFitness.df[,-2]
selectedFitness.df = selectedFitness.df[,-13]
#final.df = final.df[,-13]

#final.df <- na.omit(final.df)
#selectedFitness.df <- na.omit(selectedFitness.df)

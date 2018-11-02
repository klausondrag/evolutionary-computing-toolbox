library(ggplot2)
library(plyr)
library(dplyr)
library(stringr)
library(trend)

this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)


df <- read.table("outputTestFinal.txt", header=T)
df_sum <- group_by(df,generation)
df_sum <- summarize(df_sum,mean(number_of_limbs),sd(number_of_limbs))
colnames(df_sum) <- c("generation", "number_of_limbs", "sd")
mk.test(df_sum$number_of_limbs)

g <- ggplot(df_sum[df_sum$generation > 1,], aes(x=generation, y=number_of_limbs)) +
  geom_line(color = "blue") +
  labs(x = "Generation/Abs Size", y="Number Of Limbs")
ggsave("all_generations.png", g, device="png", height=10,width=15, units="cm")

g2 <- ggplot(df_sum[df_sum$generation > 1,][df_sum$generation<=50,], aes(x=generation, y=number_of_limbs)) +
  geom_line(color = "blue") +
  labs(x = "Generation/Abs Size", y="Number Of Limbs")
ggsave("50_generations.png", g2, device="png", height=10,width=15,units="cm")

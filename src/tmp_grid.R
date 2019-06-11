library(tidyverse)
library(gridExtra)
source("lib/functions.R")
d = read_csv(data_file("gridsearch.csv"))

d2 = d %>% group_by_at(vars(experiment:epoch)) %>% summarise_at(vars(acc:cortot), list(mean=mean, sd=sd), na.rm=T) %>% ungroup()

d2

d2 %>% group_by(depth_hidden) %>% summarize(acc_max=max(acc_mean), acc_mean=mean(acc_mean)) %>% gather(-depth_hidden, key = "stat", value = "value") %>% 
  ggplot(aes(x=depth_hidden, y=value, colour=stat)) + geom_line()

d2 %>% group_by(n_hidden) %>% summarize(acc_max=max(acc_mean), acc_mean=mean(acc_mean)) %>% gather(-n_hidden, key = "stat", value = "value") %>% 
  ggplot(aes(x=n_hidden, y=value, colour=stat)) + geom_line()


var = "loss"
plots = list()
for(var in colnames(d2 %>% select(depth_hidden:epoch))) {
  d2$target = if (class(d2[[var]]) == "character") as.numeric(as.factor(d2[[var]])) else as.numeric(d2[[var]])
  plots[[var]] = d2 %>% group_by(target) %>% summarize(acc_max=max(acc_mean), acc_mean=mean(acc_mean)) %>% gather(-target, key = "stat", value = "value") %>% 
    ggplot(aes(x=target, y=value, colour=stat)) + geom_line() + xlab(var) + ggtitle(str_c("Effect of ", var)) + scale_color_discrete(guid=F)
  
}

grid.arrange(
  grobs = plots,
  nrow=4)

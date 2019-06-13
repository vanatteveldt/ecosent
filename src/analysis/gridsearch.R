library(tidyverse)
library(gridExtra)
source("lib/functions.R")

raw = purrr::map_df(data_file(str_c("gridsearch_", 1:5, ".csv")), read_csv)


d = raw %>% mutate(loss=fct_recode(loss, MAE="mean_absolute_error", "BCE"="binary_crossentropy", MSE="mean_squared_error"),
                train_embedding=ifelse(train_embedding, "Y", "N")) 

d2 = d %>% group_by_at(vars(experiment:epoch)) %>% summarise_at(vars(acc:cortot), list(mean=mean, sd=sd), na.rm=T) %>% ungroup()



vars = colnames(d2 %>% select(depth_hidden:epoch))
vars = vars[1:3]

theme_xy = theme_minimal() + theme(legend.position="none")
theme = theme_xy + theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.ticks.x=element_blank(),
                                axis.title.y=element_blank(),axis.text.y=element_blank(),axis.ticks.y=element_blank())
theme_x = theme_xy + theme(axis.title.x=element_blank(),axis.text.x=element_blank(),axis.ticks.x=element_blank())
theme_y = theme_xy + theme(axis.title.y=element_blank(),axis.text.y=element_blank(),axis.ticks.y=element_blank())

labels = c(depth_hidden="Hidden Layer Depth", learning_rate="Learning Rate", loss="Loss", n_hidden="# of Hidden Layers", output_dim="Output Dimensionality", train_embedding="Retrain Embedding Layer?", epoch="# Epochs")

d2 = d2 %>% mutate(value=acc_mean, sd=acc_sd)
d2 = d2 %>% mutate(value=cor_mean, sd=cor_sd)
plots = list()
for(var1 in vars) {
  d2$target1 = as.factor(d2[[var1]])
  for (var2 in vars) {
    d2$target2 = as.factor(d2[[var2]])
    if (var1 == var2) {
      plot = 
        d2 %>% select(target1, value, sd) %>% na.omit %>% group_by(target1) %>% summarize(value=max(value), sd=sd[which.max(value)]) %>% 
        ggplot(aes(x=target1, y=value, ymin=value-sd, ymax=value+sd)) + geom_point() + geom_errorbar() 
    } else {
      
      data = d2 %>% select(target1, target2, value, sd) %>% na.omit  %>% group_by(target1, target2) %>% summarize(value=max(value)) %>% arrange(-value)
      plot=  ggplot(data=data, aes(x=target2, y=target1, fill=value, label=str_replace(format(value, digits=2), "0\\.", "."))) + geom_tile() + 
        geom_text(aes(alpha=sqrt(value)), color="white") + geom_text(data=head(data,1), color="darkred", fontface = "bold") + 
        scale_fill_gradient(low="white", high="steelblue", guide=F)+ylab(var1)+xlab(var2) + guides(alpha=FALSE)
      
    }
    plot =plot +ylab(labels[var1]) + xlab(labels[var2])
    left = var2 == vars[1]
    bottom = var1 == vars[length(vars)]
    if (left && bottom) plot = plot + theme_xy
    if (left && !bottom) plot = plot + theme_x
    if (!left && bottom) plot = plot + theme_y
    if (!left && !bottom) plot = plot + theme
    plots[[length(plots)+1]] =  plot
  }
}

pdf("/tmp/cor.pdf", width = 20, height = 20)
grid.arrange(grobs=plots, nrow=length(vars))
dev.off()

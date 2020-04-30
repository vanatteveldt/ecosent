#! /usr/bin/env Rscript
#DESCRIPTION: Get crowd coding data from figure-8 exports
#CREATES: data/intermediate/crowdcodings.csv
#DEPENDS: data/raw/f1345162.csv, data/raw/f1386488.csv
#OPTIONAL: TRUE

library(dplyr)
library(readr)

source("src/lib/functions.R")

read_crowd = function(filename) read_csv(filename, col_types=cols_only(id="i", `_golden`="l", `_trust`="d", sentiment="i")) %>%
  filter(!`_golden`) %>% select(id, trust=`_trust`, value=sentiment)

files = c("1345162"="data/raw/f1345162.csv", "1386488"="data/raw/f1386488.csv")

crowd = purrr::map_df(files, read_crowd, .id="job")
# A couple of sentences had >5 coders, so choose 5 random ones:
set.seed(1)
crowd = crowd %>% arrange(sample(xtfrm(id))) %>% 
  group_by(id) %>% mutate(coder=row_number()) %>% filter(coder <= 5) 
crowd %>% select(id, job, coder, trust, value) %>% arrange(id) %>% 
  write_csv("data/intermediate/crowdcodings.csv")




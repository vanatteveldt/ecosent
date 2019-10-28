#! /usr/bin/env Rscript
#DESCRIPTION: Get crowd coding data from figure-8 exports
#CREATES: data/intermediate/crowdcodings.csv
#DEPENDS: data/raw/f1345162.csv, data/raw/f1386488.csv
#OPTIONAL: TRUE

library(dplyr)
library(readr)

read_crowd = function(filename) read_csv(filename, col_types=cols_only(id="i", `_golden`="l", `_trust`="d", sentiment="i")) %>%
  filter(!`_golden`) %>% select(id, trust=`_trust`, tone=sentiment)

files = c("1345162"="data/raw/f1345162.csv", "1386488"="data/raw/f1386488.csv")

crowd = purrr::map_df(files, read_crowd, .id="job")

write_csv(crowd, "data/intermediate/crowdcodings.csv")

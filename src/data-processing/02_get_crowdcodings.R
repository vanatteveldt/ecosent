#! /usr/bin/env Rscript
#DESCRIPTION: Get crowd coding data from figure-8
#CREATES: data/intermediate/crowdcodings.csv
#DEPENDS: data/raw-private/figure8_api_key, data/intermediate/gold.csv
#OPTIONAL: TRUE

# Note: Requires the figure 8 API key 
library(tidyverse)
key = read_file("data/raw-private/figure8_api_key")
figr8::set.api.key(key)

gold = read_csv("data/intermediate/gold.csv")

crowd = figr8::results(1345162) %>% as_tibble
crowd = crowd %>% filter(id %in% gold$id) %>% select(id, tone=sentiment) %>% mutate(id=as.integer(id), tone=as.numeric(tone))
write_csv(crowd, "data/intermediate/crowdcodings.csv")

#! /usr/bin/env Rscript
#DESCRIPTION: Get gold standard data from google sheets
#CREATES: data/intermediate/gold.csv

library(googlesheets)
library(tidyverse)

gs_gap_key() %>% gs_key()
# Key gives read-only access to public data
sheet = gs_key("1xLV9HMSn8bTmpxIqBEdTyQekMm5RBmPMa4_ILv0vxCM")
gold1 = gs_read(sheet, "first set")
gold2 = gs_read(sheet, "second set - combined")

gold1 = gold1 %>% select(id, gold=`gold final`, mb, mvdv, wva) %>% mutate(gold_set=1)
gold2 = gold2 %>% select(id, gold=`gold final`, mb, mvdv, wva) %>% mutate(gold_set=2)
gold = bind_rows(gold1, gold2)
gold = gold %>% filter(!is.na(gold)) %>% select(id, value=gold) %>%
  arrange(id)
write_csv(gold, "data/intermediate/gold.csv")

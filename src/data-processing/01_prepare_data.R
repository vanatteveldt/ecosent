#! /usr/bin/env Rscript
#DESCRIPTION: Prepare manual codings values and metadata
#CREATES: data/intermediate/metadata.csv, data/intermediate/sentences_ml.csv
#DEPENDS: data/raw-private/Inhoudsanalyse_AllesMerged_noICR_Wouter.sav, data/raw/icr_data.csv, data/intermediate/gold.csv

### Gather article metadata and manual codings
# Requires access to the SPSS file from Boukes et al.. Metadata and codings are saved to (public) intermediate folder)
source("src/lib/functions.R")
library(stringr)
library(readr)
library(tibble)

d_raw = haven::read_sav("data/raw-private/Inhoudsanalyse_AllesMerged_noICR_Wouter.sav")
d = d_raw %>% mutate(ID=as.integer(ID), 
                     medium=value_labels(outlet), 
                     medtype=value_labels(Source), 
                     tone_raw=value_labels(Toon_Kop),
                     is_icr=FALSE) %>% 
  select(id=ID, date, medtype, medium, headline, coder=Codeur, is_icr, is_economy=Economisch, tone_raw) %>%
  mutate(tone_raw=str_remove(tone_raw, "\\s*\\(.*"), 
         value=recode_tone(tone_raw),
         is_economy=as.integer(is_economy),
         coder=as.integer(coder))

d2_raw =read_csv2("data/raw/icr_data.csv", col_types = cols_only(ID="i", Codeur="i", outlet="i", Source="i", Toon_Kop="i", headline="c", Economisch="i", date="c"))
d2_raw = d2_raw %>% filter(Source != 1) # Remove television
if (any(is.na(d2_raw$ID))) stop("Missing identifiers in icr_data.csv")
d2 = d2_raw %>% mutate(medium=value_labels(outlet, labels_col=d_raw$outlet), 
                       medtype=value_labels(Source, labels_col=d_raw$Source), 
                       tone_raw=value_labels(Toon_Kop, labels_col=d_raw$Toon_Kop),
                       is_icr=TRUE) %>%
    select(id=ID, date, medtype, medium, headline, coder=Codeur, is_icr, is_economy=Economisch, tone_raw) %>% 
    mutate(tone_raw=str_remove(tone_raw, "\\s*\\(.*"), 
           value=recode_tone(tone_raw), 
           date=as.POSIXct(date, format="%m/%d/%Y %H:%M:%S"))

# combine d (SPSS data containing codings except for Boukes 2019 ICR data) with d2 (csv of codings for ICR data)
d2 = d2 %>% anti_join(d, by=c("id", "coder"))
d = bind_rows(d, d2) %>% arrange(id)

# Output 1: Article metadata
# Note: timestamp can differ for same ID in both data sets (tz issues?), so keep only first ID
meta = d %>% select(id, date, medtype, medium, headline) %>% 
  group_by(id) %>% filter(row_number()==1, !is.na(headline)) %>%  ungroup() %>% arrange(id)
write_csv(meta, "data/intermediate/metadata.csv")


# Output 2: Machine Learning training sentences
gold = read_csv("data/intermediate/gold.csv") %>% 
  select(id, value) %>% 
  add_column(gold=TRUE)
codings = d %>% filter(!is_icr, !is.na(value), !id %in% gold$id) %>% 
  select(id, value) %>% 
  add_column(gold=FALSE)

sentences = inner_join(meta, bind_rows(codings, gold))
lemmata = lemmatize(sentences)
sentences_ml = inner_join(sentences, lemmata)
write_csv(sentences_ml, "data/intermediate/sentences_ml.csv")

# Output 3: Gold sentences
d %>% semi_join(gold) %>% na.omit() %>% select(id, coder, value) %>% arrange(id) %>% write_csv("data/intermediate/manual_coding.csv")

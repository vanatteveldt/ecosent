#! /usr/bin/env Rscript
#DESCRIPTION: Prepare manual codings values and metadata
#CREATES: data/intermediate/metadata.csv, data/intermediate/manual_codings.csv
#DEPENDS: data/raw-private/Inhoudsanalyse_AllesMerged_noICR_Wouter.sav, data/raw/icr_data.csv

### Article metadata and manual codings
# Requires access to the SPSS file from Boukes et al.. Metadata and codings are saved to (public) intermediate folder)
source("src/lib/functions.R")

d_raw = haven::read_sav("data/raw-private/Inhoudsanalyse_AllesMerged_noICR_Wouter.sav")
d = d_raw %>% mutate(ID=as.integer(ID), 
                     medium=value_labels(outlet), 
                     medtype=value_labels(Source), 
                     tone_raw=value_labels(Toon_Kop),
                     is_icr=FALSE) %>% 
  select(id=ID, date, medtype, medium, headline, coder=Codeur, is_icr, is_economy=Economisch, tone_raw) %>%
  mutate(tone_raw=str_remove(tone_raw, "\\s*\\(.*"), 
         tone=recode_tone(tone_raw),
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
           tone=recode_tone(tone_raw), 
           date=as.POSIXct(date, format="%m/%d/%Y %H:%M:%S"))

d2 = d2 %>% anti_join(d, by=c("id", "coder"))

d = bind_rows(d, d2) %>% arrange(id)

# Note: timestamp can differ for same ID in both data sets (tz issues?), so keep only first ID
d %>% select(id, date, medtype, medium, headline) %>% group_by(id) %>% filter(row_number()==1, !is.na(headline)) %>%  write_csv("data/intermediate/metadata.csv")
d %>% select(id, coder, is_icr, is_economy, tone_raw, tone) %>% unique %>% write_csv("data/intermediate/manual_codings.csv")

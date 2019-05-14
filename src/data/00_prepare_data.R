source("lib/functions.R")

### Get gold data
# Requires access to the google sheet, resulting gold data is saved to (public) intermediate folder
library(googlesheets)
sheet = gs_key("1xLV9HMSn8bTmpxIqBEdTyQekMm5RBmPMa4_ILv0vxCM")
gold1 = gs_read(sheet, "first set")
gold2 = gs_read(sheet, "second set - combined")

gold1 %<>% select(id, gold=`gold final`, mb, mvdv, wva) %>% mutate(gold_set=1)
gold2 %<>% select(id, gold=`gold final`, mb, mvdv, wva) %>% mutate(gold_set=2)
gold = bind_rows(gold1, gold2)
write_csv(gold, "../data/intermediate/gold.csv")

### Article metadata and manual codings
# Requires access to the SPSS file from Boukes et al.. Metadata and codings are saved to (public) intermediate folder)
library(haven)

d_raw = haven::read_sav("../data/private/Inhoudsanalyse_AllesMerged_noICR_Wouter.sav")
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

d2_raw = read_csv2("../data/raw/icr_data.csv")
d2 = d2_raw %>% mutate(medium=value_labels(outlet, labels_col=d_raw$outlet), 
                       medtype=value_labels(Source, labels_col=d_raw$Source), 
                       tone_raw=value_labels(Toon_Kop, labels_col=d_raw$Toon_Kop),
                       is_icr=TRUE) %>%
    select(id=ID, date, medtype, medium, headline, coder=Codeur, is_icr, is_economy=Economisch, tone_raw) %>% 
    mutate(tone_raw=str_remove(tone_raw, "\\s*\\(.*"), 
           tone=recode_tone(tone_raw), 
           date=as.POSIXct(date, format="%m/%d/%Y %H:%M:%S"))

d2 = d2 %>% anti_join(d, by=c("id", "coder"))

d = bind_rows(d, d2)

# Note: timestamp can differ for same ID in both data sets (tz issues?), so keep only first ID
d %>% select(id, date, medtype, medium, headline) %>% group_by(id) %>% filter(row_number()==1) %>% write_csv("../data/intermediate/metadata.csv")
d %>% select(id, coder, is_icr, is_economy, tone_raw, tone) %>% unique %>% write_csv("../data/intermediate/manual_codings.csv")

### Get crowd data
# Note: Requires the figure 8 API key to be set using figr8::set.api.key(...)
# source(path.expand("~/Dropbox/tmp/.figure8_api_key.R"))

library(figr8)
crowd = results(1345162) %>% as.tibble
crowd %<>% filter(id %in% gold$id) %>% select(id, tone=sentiment) %>% mutate(id=as.integer(id), tone=as.numeric(tone))
write_csv(crowd, "../data/intermediate/crowdcodings.csv")

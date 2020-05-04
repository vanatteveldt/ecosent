#! /usr/bin/env Rscript
#DESCRIPTION: Apply dictionary analysis using R/Quanteda
#DEPENDS: data/raw/{gold_sentences.csv,dictionaries/{dictionary_muddiman_combined.csv,db_nl.yml,{db,muddiman}_{google,deepl}.yml}}
#CREATES: data/intermediate/dictionary_output_quanteda.csv

library(quanteda)
library(tidyverse)

# Create the dfm

df <- read_csv("data/raw/gold_sentences.csv")
nl_dfm <- df %>% corpus(docid_field="id", text_field="dutch_lemmas") %>% dfm()
google_dfm <- df %>% corpus(docid_field="id", text_field="google_lemmas") %>% dfm()
deepl_dfm <- df %>% corpus(docid_field="id", text_field="deepl_lemmas") %>% dfm()


# Define Custom dictionaries:

# Muddiman approach
muddiman <- read_csv("data/raw/dictionaries/dictionary_muddiman_combined.csv") %>%
  mutate(majvote_pos = rowSums(.[c(3,5,7)], na.rm = T),
         majvote_neg = rowSums(.[c(4,6,8)], na.rm = T))

muddiman_nl <- dictionary(list(positive = muddiman$words[muddiman$majvote_pos>1],
                               negative = muddiman$words[muddiman$majvote_neg>1]))

nrc <- read_csv("data/raw/dictionaries/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.csv") %>%
  select(c(Eng = `English (en)`, NL = `Dutch (nl)`, Positive, Negative, Fear, Trust))

# Define set of Dutch and English dictionaries
dutch_dictionaries <- list(
  "nrc"=dictionary(list(positive = nrc$NL[nrc$Positive==1],
                        negative = nrc$NL[nrc$Negative==1],
                        fear = nrc$NL[nrc$Fear==1],
                        trust = nrc$NL[nrc$Trust==1])),
  "db"=dictionary(file="data/raw/dictionaries/db_nl.yml"), # Damstra & Boukes
  "muddiman"=muddiman_nl)

# For English, take standard dictionaries plus dicts translated by deepl and google
english_dictionaries  <-  list(
  "nrc"=dictionary(list(positive = nrc$Eng[nrc$Positive==1],
                        negative = nrc$Eng[nrc$Negative==1],
                        fear = nrc$Eng[nrc$Fear==1],
                        trust = nrc$Eng[nrc$Trust==1])),
  "LMD" = quanteda.dictionaries::data_dictionary_LoughranMcDonald[1:2],
  "AFINN" = quanteda.dictionaries::data_dictionary_AFINN,
  "HuLiu" = quanteda.dictionaries::data_dictionary_HuLiu,
  "LSD" = data_dictionary_LSD2015[1:2],
  "GenInq" = quanteda.dictionaries::data_dictionary_geninqposneg,
  "RID" = quanteda.dictionaries::data_dictionary_RID$EMOTIONS[c("POSITIVE_AFFECT", "ANXIETY", "SADNESS", "GLORY")]
)

# Manually translated dictionaries
google_dictionaries <- c(english_dictionaries, list(
  "db"=dictionary(file="data/raw/dictionaries/db_google.yml"),
  "muddiman"=dictionary(file="data/raw/dictionaries/muddiman_google.yml")))
  
deepl_dictionaries <- c(english_dictionaries, list(
  "db"=dictionary(file="data/raw/dictionaries/db_deepl.yml"),
  "muddiman"=dictionary(file="data/raw/dictionaries/muddiman_deepl.yml")))

# Apply the dictionaries

#' Helper function that applies a dictionary and converts to 'long' results format, padding with zeroes as needed
apply_dictionary <- function(dictionary, dfm) {
  rownames(dfm)
  counts = dfm %>% dfm_lookup(dictionary, valuetype = "glob") %>% 
    convert(to="tripletlist") %>% 
    as_tibble() %>%
    rename(id=document, value=frequency) %>%
    mutate(id=as.numeric(id), 
           feature=str_replace_all(tolower(feature), "[ \\.]", "_"))
  zeros = expand_grid(id=as.numeric(rownames(dfm)), feature=names(dictionary)) %>% 
    anti_join(counts, by=c("id", "feature")) %>% add_column(value=0)
  rbind(counts, zeros)
}

# Apply dictionaries
results_nl = purrr::map(dutch_dictionaries, apply_dictionary, nl_dfm) %>% bind_rows(.id="dictionary")
results_google = purrr::map(google_dictionaries, apply_dictionary, google_dfm) %>% bind_rows(.id="dictionary")
results_deepl= purrr::map(deepl_dictionaries, apply_dictionary, deepl_dfm) %>% bind_rows(.id="dictionary")
results = bind_rows(nl=results_nl, google=results_google, deepl=results_deepl, .id="language")

# Compute sentiment and emotionality scores from counts
sentiment = results %>% 
  pivot_wider(id_cols = language:id, names_from = feature, values_fill=list(value=0)) %>%
  mutate(value=case_when(dictionary=="nrc" ~ (trust + positive) - (fear + negative),
                         dictionary=="db" ~ hope - fear,
                         dictionary=="RID" ~ positive_affect - anxiety,
                         T ~ positive - negative)) %>% 
  select(language:id, value) %>% 
  mutate(variable=str_c(dictionary, language, sep = "_")) %>%
  select(id, variable, everything()) %>%
  arrange(id, variable)

write_csv(sentiment, "data/intermediate/dictionary_output_quanteda.csv")

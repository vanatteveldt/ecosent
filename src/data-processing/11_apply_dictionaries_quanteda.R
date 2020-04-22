library(quanteda)
library(tidyverse)

# Define Custom dictionaries:

# Muddiman approach
muddiman <- read_csv("data/raw/dictionaries/dictionary_muddiman_combined.csv") %>%
  mutate(majvote_pos = rowSums(d2[,c(3,5,7)], na.rm = T),
         majvote_neg = rowSums(d2[,c(4,6,8)], na.rm = T))

muddiman_nl <- dictionary(list(positive = muddiman$words[d2$majvote_pos>1],
                                 negative = muddiman$words[d2$majvote_neg>1]))

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

#' Helper function that applies a dictionary and converts to 'long' results format
apply_dictionary <- function(dictionary, dfm) {
  dfm %>% dfm_lookup(dictionary, valuetype = "glob") %>% 
    convert(to="tripletlist") %>% 
    as_tibble() %>%
    rename(id=document) %>%
    mutate(id=as.numeric(id), 
           feature=str_replace_all(tolower(feature), "[ \\.]", "_"))
}

# Apply dictionaries
results_nl = purrr::map(dutch_dictionaries, apply_dictionary, nl_dfm) %>% bind_rows(.id="dictionary")
results_google = purrr::map(google_dictionaries, apply_dictionary, google_dfm) %>% bind_rows(.id="dictionary")
results_deepl= purrr::map(deepl_dictionaries, apply_dictionary, deepl_dfm) %>% bind_rows(.id="dictionary")
results = bind_rows(nl=results_nl, google=results_google, deepl=results_deepl, .id="language")

write_csv(results, "data/intermediate/dictionary_output2.csv")

# Compute sentiment and emotionality scores from counts
sentiment = results %>% 
  pivot_wider(id_cols = language:id, names_from = feature, values_from = frequency, values_fill=list(frequency=0)) %>%
  mutate(sentiment=case_when(! dictionary %in% c("db", "RID") ~ positive - negative),
         emotionality=case_when(dictionary=="nrc" ~ trust - fear,
                                dictionary=="db" ~ hope - fear,
                                dictionary=="RID" ~ positive_affect - anxiety)) 

gold = read_csv("data/intermediate/gold.csv") %>%  select(id, gold)
setdiff(results$id, gold$id)
setdiff(gold$id, results$id)

# bivariate correlation sentiment (-> to be moved to analysis script)
inner_join(gold %>% na.omit(),
           sentiment %>% select(language, dictionary, id, sentiment) %>% na.omit() %>% 
             pivot_wider(names_from=c("language", "dictionary"), values_from=sentiment, values_fill=list(sentiment=0))) %>% select(-id) %>% cor()

inner_join(gold %>% na.omit(),
           sentiment %>% select(language, dictionary, id, emotionality) %>% na.omit() %>% 
             pivot_wider(names_from=c("language", "dictionary"), values_from=emotionality, values_fill=list(emotionality=0))) %>% select(-id) %>% cor()


inner_join(gold %>% na.omit(),
          sentiment %>% select(language, dictionary, id, sentiment) %>% na.omit() %>% 
            pivot_wider(names_from=c("language", "dictionary"), values_from=sentiment, values_fill=list(sentiment=0))) %>% View


# meta = read_csv("data/intermediate/metadata.csv")

source("src/lib/functions.R")

gold = read_csv("data/intermediate/gold.csv") %>% select(id, gold=value)

# Combine dictionary output from python and R 
dict1 = read_csv("data/intermediate/dictionary_output.csv") %>% add_column(method="dictionary", .after="id")
dict2 = read_csv("data/intermediate/dictionary_output_quanteda.csv") %>% add_column(method="dictionary", .after="id")
dict = dict1 %>% add_column(language="nl", dictionary=dict1$variable, .after="variable") %>% bind_rows(dict2)

# Read manual coding from training data
set.seed(1)
manual_raw = read_csv("data/intermediate/manual_coding.csv") %>%  
  arrange(id, sample(xtfrm(id))) %>% group_by(id) %>% mutate(repetition=row_number())
# For single-coded, take only first (random) coder per article as most articles are only coded once
manual1 = manual_raw %>% filter(repetition==1) %>% select(-repetition) %>% ungroup() %>% 
  add_column(method="manual", variable="manual1", .after="id")
# For majority voting, take only aarticles with at least 3 coders and take only first three (random) coders
manual3 = manual_raw %>% filter(n()>=3, repetition<=3) %>% vote(thres=2, tie=0) %>% rename(confidence=support) %>% 
  add_column(method="manual", variable="manual3", .after="id")
manual = bind_rows(manual1, manual3) %>% select(-coder)

# Read crowd coding data and add voting for 3 and 5 coders
crowd1 = read_csv("data/intermediate/crowdcodings.csv") %>% rename(confidence=trust) %>% 
  add_column(method="crowd", variable="crowd1", .after="id")
crowd5 = vote(crowd1, thres=3, tie=0) %>% rename(confidence=support) %>% add_column(method="crowd", variable="crowd5", .after="id")
# Compute majority votes for n=3 for all permutations of coders
permutations = combn(1:5, 3, simplify = FALSE)
do_vote = function (coders) vote(crowd1 %>% filter(coder %in% coders), thres = 2, tie=0) %>% rename(confidence=support)
crowd3 = purrr::map_df(permutations, do_vote, .id="permutation") %>% mutate(repetition=as.numeric(permutation), permutation=NULL) %>% 
  add_column(method="crowd", variable="crowd3", .after="id")
crowd = bind_rows(rename(crowd1, repetition=coder), crowd3, crowd5) %>% select(-job)

# Read ML predictions
ml = bind_rows(read_csv("data/intermediate/svm_predictions.csv") %>% add_column(method="ml", variable="svm", .after="id"),
               read_csv("data/intermediate/cnn_predictions.csv") %>% add_column(method="ml", variable="cnn", .after="id"))

scores = bind_rows(dict, manual, crowd, ml) %>% semi_join(gold)
# To check N per method
# scores %>% group_by(method, variable, repetition) %>% summarize(n=n(), nart=length(unique(id))) %>% View
write_csv(scores, "data/intermediate/combined_predictions.csv")





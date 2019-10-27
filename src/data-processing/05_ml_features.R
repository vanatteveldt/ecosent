#! /usr/bin/env Rscript
#DESCRIPTION: Lemmatize sentences and combine with gold data to create ML training set 
#CREATES: data/intermediate/sentences_ml.csv
#DEPENDS: data/intermediate/gold.csv, data/intermediate/metadata.csv, data/intermediate/manual_codings.csv
#OPTIONAL: TRUE

# Creates the data/intermediate/sentences_ml.csv file
# This contains headline (raw and lemmatized) and coding for both train and gold
# It requires the files from 00_prepare_data.R and that proycon/lamachine can be called via docker

library(tidyverse)

meta = read_csv("data/intermediate/metadata.csv")
gold = read_csv("data/intermediate/gold.csv") %>% 
  select(id, tone=gold) %>% 
  filter(!is.na(tone)) %>% 
  mutate(gold=TRUE)
codings = read_csv("data/intermediate/manual_codings.csv") %>% 
  filter(!is_icr, !is.na(tone), !id %in% gold$id) %>% 
  select(id, tone) %>% 
  mutate(gold=FALSE)
codings = inner_join(meta, bind_rows(codings, gold))

# Lemmatize the headlines using frogger.
# Step 1: save the files to a temporary folder 
tmpdir = tempdir()
indir = tempfile("frog", tmpdir = tmpdir)
dir.create(indir)
for (id in codings$id) {
  outf = file.path(indir, id)
  fileConn<-file(outf)
  writeLines(codings$headline[codings$id == id], fileConn)
  close(fileConn)
}
# Step 2: call frog via lamachine docker
# Note: if you get permission denied it might be better to run the command in a terminal rather than through system(.)
outdir = tempfile("frog-out", tmpdir = tmpdir)
dir.create(outdir)
cmd = paste0("docker run -v ",tmpdir,":",tmpdir," proycon/lamachine frog --testdir ", indir, " --outputdir ", outdir)
message(cmd)
system(cmd)

# Step 3: read frog output
results = list()
for (id in codings$id) {
  if (id %in% names(results)) next
  fn = file.path(outdir, paste0(id, ".out"))
  tokens = read_delim(fn, "\t", col_types = "iccccdccic", col_names=c("token", "word", "lemma", "morph", "POS", "conf", "NER", "chunk", "head", "rel"), quote="") %>%
    mutate(pos2 = str_remove(POS, "\\(.*")) %>%
    filter(!pos2 %in% c("LID", "LET"))
  lemmapos = paste(tokens$pos2,tokens$lemma, sep = "_", collapse=" ")
  lemmata = paste(tokens$lemma, sep = "_", collapse=" ")
  results[[as.character(id)]] = data.frame(id=id, lemmapos = lemmapos, lemmata=lemmata, stringsAsFactors = F)
}

lemmata = bind_rows(results) %>% as.tibble

codings = left_join(codings, lemmata)
if (any(is.na(codings$lemmapos))) stop("Not all sentences were lemmatized")

write_csv(codings, "data/intermediate/sentences_ml.csv")

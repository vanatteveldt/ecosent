library(dplyr)

#' Majority voting for multiple coders. Assumes that columns id and value point to a unique doc id and the coded value, respectively
vote = function(data, thres) {
  votes = data %>% group_by(id, value) %>% summarize(n=n()) %>% mutate(support=max(n)) %>% filter(support >= thres, n == support)
  if (length(unique(votes$id)) != nrow(votes)) stop("!")
  votes %>% select(id, value, support)
}

#' Compare two sets of predictions and give coverage, accuracy, and alpha
compare = function(crowd, gold, ...) {
  d = crowd %>% rename(crowd=tone) %>% left_join(gold, by="id") %>% ungroup()
  stats = d %>% summarize(n=n(), acc=mean(crowd == tone))
  alpha =d %>% select(crowd, tone) %>% as.matrix() %>% t %>% irr::kripp.alpha("ordinal")
  tibble(..., cov=stats$n/nrow(gold), acc=stats$acc, alpha=alpha$value)
}

#' Get the value labels from a (SPSS) column
value_labels = function(x, labels_col=x) {
  labels = attr(labels_col, "labels") 
  names(labels)[match(x, labels)]
}

#' Recode the 'raw' tone into -1 .. 1
recode_tone = function(tone) {
  recode(tone, "vooral negatief"=-1, "vooral positief"=1, "de kop is niet van toepassing op de economie"=NA_real_, .default=0)
}

#' Lemmatize words with frog. Doing this with docker is not the most elegant way, but it seems to work.
#' @param data data frame with id and headline column
lemmatize = function(data) {
  # Step 1: save the files to a temporary folder 
  tmpdir = tempdir()
  indir = tempfile("frog", tmpdir = tmpdir)
  dir.create(indir)
  for (id in data$id) {
    outf = file.path(indir, id)
    fileConn<-file(outf)
    writeLines(data$headline[data$id == id], fileConn)
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
  for (id in data$id) {
    if (id %in% names(results)) next
    fn = file.path(outdir, paste0(id, ".out"))
    tokens = read_delim(fn, "\t", col_types = "iccccdccic", col_names=c("token", "word", "lemma", "morph", "POS", "conf", "NER", "chunk", "head", "rel"), quote="") %>%
      mutate(pos2 = str_remove(POS, "\\(.*")) %>%
      filter(!pos2 %in% c("LID", "LET"))
    lemmapos = paste(tokens$pos2,tokens$lemma, sep = "_", collapse=" ")
    lemmata = paste(tokens$lemma, sep = "_", collapse=" ")
    results[[as.character(id)]] = data.frame(id=id, lemmapos = lemmapos, lemmata=lemmata, stringsAsFactors = F)
  }
  bind_rows(results) %>% as_tibble()
}

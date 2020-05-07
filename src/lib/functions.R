library(dplyr)

#' Majority voting for multiple coders. Assumes that columns id and value point to a unique doc id and the coded value, respectively
#' @param data data frame coltaining id and value columns
#' @param thres threshol for accepting a value
#' @param tie what to do when no value meets the threshold: NULL to omit the record or any other value (NA, 0) to insert that
vote = function(data, thres, tie=NULL) {
  votes = data %>% group_by(id, value) %>% summarize(n=n()) %>% mutate(support=max(n)) %>% filter(support >= thres, n == support)
  if (length(unique(votes$id)) != nrow(votes)) stop("!")
  votes = votes %>% select(id, value, support)
  if (!is.null(tie))
    votes = bind_rows(votes, tibble(id=setdiff(data$id, votes$id), support=0, value=tie))
  votes
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

### Auxilliary functions for perfomance calculation
#' trichotomize a score into -1, 0, 1, taking +/- 0.5 as boundary point
trichotomize = function(value) case_when(value>.5 ~ 1, value < -.5 ~ -1, T ~ 0) 

#' Compute precision for given values and target class
precision = function(predicted, actual, class) (sum(predicted == class & actual == class) / sum(predicted == class)) %>% replace_na(0)
#' Compute recall for given values and target class
recall = function(predicted, actual, class) sum(predicted == class & actual == class) / sum(actual == class)
#' Compute F1 score from precision and recall
f1 = function(precision, recall) ifelse(precision+recall==0, 0, 2*precision*recall / (precision + recall))
#' Compute Krippendorff's alpha from given values
alpha = function(predicted, actual) irr::kripp.alpha(rbind(predicted, actual), method = "ordinal")$value

#' Render a template using jinja2 command line tool
render_j2 = function(template, output, data, auto_unbox=TRUE, na="string") {
  data = jsonlite::toJSON(data, pretty=TRUE, auto_unbox=auto_unbox, na=na)
  system(glue::glue("env/bin/j2 --format json {template} -o {output}"), input=data)
}


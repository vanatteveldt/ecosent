.project_root = getwd()
while (!str_ends(.project_root, "/src")) .project_root = normalizePath(file.path(.project_root, ".."))
.project_root = normalizePath(file.path(.project_root, ".."))

data_file = function(filename, folder="intermediate") {
   normalizePath(file.path(.project_root, "data", folder, filename))   
}


#' Majority voting for multiple coders. Assumes that columns id and tone point to a unique doc id and the coded tone, respectively
vote = function(data, thres) {
  votes = data %>% group_by(id, tone) %>% summarize(n=n()) %>% mutate(support=max(n)) %>% filter(support >= thres, n == support)
  if (length(unique(votes$id)) != nrow(votes)) stop("!")
  votes %>% select(id, tone, support)
}

#' Compare two sets of predictions and give coverage, accuracy, and alpha
compare = function(crowd, gold, ...) {
  d = crowd %>% rename(crowd=tone) %>% left_join(gold, by="id") %>% ungroup()
  stats = d %>% summarize(n=n(), acc=mean(crowd == tone))
  alpha =d %>% select(crowd, tone) %>% as.matrix() %>% t %>% irr::kripp.alpha("ordinal")
  tibble(..., cov=stats$n/nrow(gold), acc=stats$acc, alpha=alpha$value)
}

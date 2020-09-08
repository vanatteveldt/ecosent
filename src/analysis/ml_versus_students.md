Performance of ML versus student coding
================

The analysis below shows the performance of the machine learning methods
validated against the original student coding rather than then gold
standard. Since performance is very similar to the outcomes based on the
gold standard, this shows that the ML methods did not suffer from a
systematic mismatch between the gold standard coding procedure and the
original student coding.

# Data

``` r
library(tidyverse)
library(here)
source(here("src/lib/functions.R"))
gold = read_csv(here("data/intermediate/gold.csv")) %>% rename(gold=value)
scores = read_csv(here("data/intermediate/combined_predictions.csv"), col_types = "iccccddd")
scores = scores %>% filter(is.na(language) | language != "google", variable != "recessie", variable != "boukes")  %>% mutate(value=trichotomize(value))
names = read_csv(here("src/analysis/report_names.csv"))
```

# New gold Standard

Alternative gold standard: voted outcome for headlines coded by 3
students plus simple value for other
headlines:

``` r
mgold3 = scores %>% filter(variable == "manual3") %>% select(id, gold=value)
mgold1 = scores %>% filter(variable == "manual1") %>% anti_join(mgold3, by="id") %>% select(id, gold=value)
mgold = bind_rows(mgold1, mgold3)
```

# Performance

Compute performance against these values:

``` r
table = scores %>% filter(method == "ml") %>% inner_join(mgold) %>% 
  mutate(correct=gold == value)%>% 
  group_by(method, language, variable, repetition) %>% 
  summarize(acc=mean(correct), #cor=cor(gold, value), 
            alpha=alpha(gold, value), 
            pos_precision=precision(value, gold, 1), pos_recall=recall(value, gold, 1), pos_f1=f1(pos_precision, pos_recall),
            neut_precision=precision(value, gold, 0), neut_recall=recall(value, gold, 0), neut_f1=f1(neut_precision, neut_recall),
            neg_precision=precision(value, gold, -1), neg_recall=recall(value, gold, -1), neg_f1=f1(neg_precision, neg_recall)) %>%  
  summarize_at(vars(acc:last_col()), mean) %>% 
  arrange(match(method, c("dictionary", "ml", "crowd", "manual")), language, variable ) %>% 
  ungroup() %>% left_join(names) %>% select(section, name, acc:neg_f1)

knitr::kable(table, digits=2)
```

| section          | name |  acc | alpha | pos\_precision | pos\_recall | pos\_f1 | neut\_precision | neut\_recall | neut\_f1 | neg\_precision | neg\_recall | neg\_f1 |
| :--------------- | :--- | ---: | ----: | -------------: | ----------: | ------: | --------------: | -----------: | -------: | -------------: | ----------: | ------: |
| Machine Learning | CNN  | 0.60 |  0.46 |           0.69 |        0.50 |    0.57 |            0.57 |         0.72 |     0.63 |           0.62 |        0.53 |    0.57 |
| Machine Learning | NB   | 0.56 |  0.38 |           0.74 |        0.35 |    0.47 |            0.51 |         0.78 |     0.62 |           0.59 |        0.44 |    0.50 |
| Machine Learning | SVM  | 0.58 |  0.41 |           0.72 |        0.39 |    0.50 |            0.53 |         0.77 |     0.63 |           0.61 |        0.48 |    0.54 |

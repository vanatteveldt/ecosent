Confusion Matrices
================

# Confusion Matrices

Below are the confusion matrices for all automatic sentiment analysis
methods tested in the article.

## Data

``` r
library(tidyverse)
library(here)
source(here("src/lib/functions.R"))
gold = read_csv(here("data/intermediate/gold.csv")) %>% rename(gold=value)
scores = read_csv(here("data/intermediate/combined_predictions.csv"), col_types = "iccccddd")
scores = scores %>% filter(is.na(language) | language != "google", variable != "recessie", variable != "boukes")  %>% mutate(value=trichotomize(value))
names = read_csv(here("src/analysis/report_names.csv"))
```

# Code

``` r
library(glue)
cm_output = NULL
for (section in setdiff(unique(names$section), "Gold Standard")) {
  cm_output = c(cm_output, glue("## {section}"))
  for (v in names$variable[names$section == section]) {
    cm_output = c(cm_output, glue("### Confusion matrix for: {v}\n"))
    cm = inner_join(scores, gold) %>% filter(variable==v) %>% 
      group_by(value, gold) %>% summarize(n=n()) %>% rename(actual='gold') %>% 
      pivot_wider(names_from="value", values_from="n", values_fill=0) %>% arrange(actual)
    cm_output = c(cm_output, knitr::kable(cm))
}
}
```

# Results

## Manual Coding

### Confusion matrix for: manual1

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  79 | 20 |  0 |
|      0 |  12 | 87 |  9 |
|      1 |   3 |  7 | 63 |

### Confusion matrix for: manual3

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  27 |  5 |  0 |
|      0 |   4 | 36 |  1 |
|      1 |   0 |  3 | 31 |

## Crowd-Coding

### Confusion matrix for: crowd1

| actual | \-1 |   0 |   1 |
| -----: | --: | --: | --: |
|    \-1 | 387 |  98 |  10 |
|      0 | 106 | 326 | 128 |
|      1 |   5 |  52 | 308 |

### Confusion matrix for: crowd3

| actual | \-1 |   0 |   1 |
| -----: | --: | --: | --: |
|    \-1 | 802 | 182 |   6 |
|      0 | 159 | 730 | 231 |
|      1 |   3 |  76 | 651 |

### Confusion matrix for: crowd5

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  79 | 20 |  0 |
|      0 |  15 | 73 | 24 |
|      1 |   0 |  7 | 66 |

## Machine Learning

### Confusion matrix for: cnn

| actual | \-1 |   0 |   1 |
| -----: | --: | --: | --: |
|    \-1 | 567 | 336 |  87 |
|      0 | 162 | 869 |  89 |
|      1 |  69 | 304 | 357 |

### Confusion matrix for: nb

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  47 | 46 |  6 |
|      0 |  16 | 93 |  3 |
|      1 |   9 | 39 | 25 |

### Confusion matrix for: svm

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  48 | 46 |  5 |
|      0 |  17 | 88 |  7 |
|      1 |  10 | 36 | 27 |

## Dictionaries

### Confusion matrix for: DANEW

| actual | \-1 |   0 | 1 |
| -----: | --: | --: | -: |
|    \-1 |   4 |  95 | 0 |
|      0 |   1 | 109 | 2 |
|      1 |   0 |  67 | 6 |

### Confusion matrix for: db\_nl

| actual |   0 | 1 |
| -----: | --: | -: |
|    \-1 |  99 | 0 |
|      0 | 111 | 1 |
|      1 |  68 | 5 |

### Confusion matrix for: muddiman\_nl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  39 | 53 |  7 |
|      0 |  22 | 72 | 18 |
|      1 |  12 | 33 | 28 |

### Confusion matrix for: nrc\_nl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  46 | 31 | 22 |
|      0 |  24 | 49 | 39 |
|      1 |   8 | 26 | 39 |

### Confusion matrix for: pattern

| actual | \-1 |   0 | 1 |
| -----: | --: | --: | -: |
|    \-1 |   3 |  95 | 1 |
|      0 |   4 | 101 | 7 |
|      1 |   1 |  66 | 6 |

### Confusion matrix for: polyglot

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  33 | 58 |  8 |
|      0 |  20 | 62 | 30 |
|      1 |   9 | 41 | 23 |

## English Dictionaries (translated using deepl)

### Confusion matrix for: AFINN\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  38 | 47 | 14 |
|      0 |  19 | 56 | 37 |
|      1 |   9 | 36 | 28 |

### Confusion matrix for: db\_deepl

| actual | \-1 |   0 | 1 |
| -----: | --: | --: | -: |
|    \-1 |   2 |  96 | 1 |
|      0 |   0 | 110 | 2 |
|      1 |   0 |  67 | 6 |

### Confusion matrix for: GenInq\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  47 | 36 | 16 |
|      0 |  27 | 42 | 43 |
|      1 |  13 | 33 | 27 |

### Confusion matrix for: HuLiu\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  40 | 50 |  9 |
|      0 |  18 | 70 | 24 |
|      1 |   4 | 47 | 22 |

### Confusion matrix for: LMD\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  43 | 53 |  3 |
|      0 |  16 | 89 |  7 |
|      1 |  10 | 53 | 10 |

### Confusion matrix for: LSD\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  41 | 47 | 11 |
|      0 |  17 | 61 | 34 |
|      1 |   8 | 36 | 29 |

### Confusion matrix for: muddiman\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  30 | 58 | 11 |
|      0 |  14 | 79 | 19 |
|      1 |   9 | 36 | 28 |

### Confusion matrix for: nrc\_deepl

| actual | \-1 |  0 |  1 |
| -----: | --: | -: | -: |
|    \-1 |  39 | 27 | 33 |
|      0 |  23 | 36 | 53 |
|      1 |   7 | 21 | 45 |

### Confusion matrix for: RID\_deepl

| actual | \-1 |   0 | 1 |
| -----: | --: | --: | -: |
|    \-1 |   9 |  89 | 1 |
|      0 |   0 | 109 | 3 |
|      1 |   2 |  71 | 0 |

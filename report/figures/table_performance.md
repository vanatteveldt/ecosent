# Table 2: Overall Performance of the Tested Sentiment Analysis Approaches

|section              |name             |  acc| alpha| pos_precision| pos_recall| pos_f1| neut_precision| neut_recall| neut_f1| neg_precision| neg_recall| neg_f1|
|:--------------------|:----------------|----:|-----:|-------------:|----------:|------:|--------------:|-----------:|-------:|-------------:|----------:|------:|
|English Dictionaries |AFINN            | 0.43|  0.27|          0.35|       0.38|   0.37|           0.40|        0.50|    0.45|          0.58|       0.38|   0.46|
|English Dictionaries |DamstraBoukes    | 0.42|  0.07|          0.67|       0.08|   0.15|           0.40|        0.98|    0.57|          1.00|       0.02|   0.04|
|English Dictionaries |GenInq           | 0.41|  0.26|          0.31|       0.37|   0.34|           0.38|        0.38|    0.38|          0.54|       0.47|   0.51|
|English Dictionaries |HuLiu            | 0.46|  0.34|          0.40|       0.30|   0.34|           0.42|        0.62|    0.50|          0.65|       0.40|   0.50|
|English Dictionaries |LoughranMcDonald | 0.50|  0.29|          0.50|       0.14|   0.22|           0.46|        0.79|    0.58|          0.62|       0.43|   0.51|
|English Dictionaries |LSD              | 0.46|  0.33|          0.39|       0.40|   0.39|           0.42|        0.54|    0.48|          0.62|       0.41|   0.50|
|English Dictionaries |Muddiman         | 0.48|  0.27|          0.48|       0.38|   0.43|           0.46|        0.71|    0.55|          0.57|       0.30|   0.39|
|English Dictionaries |NRC              | 0.42|  0.23|          0.34|       0.62|   0.44|           0.43|        0.32|    0.37|          0.57|       0.39|   0.46|
|English Dictionaries |RID              | 0.42|  0.06|          0.00|       0.00|   0.00|           0.41|        0.97|    0.57|          0.82|       0.09|   0.16|
|Dictionaries         |DANEW            | 0.42|  0.10|          0.75|       0.08|   0.15|           0.40|        0.97|    0.57|          0.80|       0.04|   0.08|
|Dictionaries         |DamstraBoukes    | 0.41|  0.05|          0.83|       0.07|   0.13|           0.40|        0.99|    0.57|          0.00|       0.00|   0.00|
|Dictionaries         |Muddiman         | 0.49|  0.31|          0.53|       0.38|   0.44|           0.46|        0.64|    0.53|          0.53|       0.39|   0.45|
|Dictionaries         |NRC              | 0.47|  0.32|          0.39|       0.53|   0.45|           0.46|        0.44|    0.45|          0.59|       0.46|   0.52|
|Dictionaries         |Pattern          | 0.39|  0.07|          0.43|       0.08|   0.14|           0.39|        0.90|    0.54|          0.38|       0.03|   0.06|
|Dictionaries         |Polyglot         | 0.42|  0.26|          0.38|       0.32|   0.34|           0.39|        0.55|    0.45|          0.53|       0.33|   0.41|
|Machine Learning     |CNN              | 0.63|  0.50|          0.68|       0.49|   0.56|           0.58|        0.78|    0.66|          0.72|       0.57|   0.63|
|Machine Learning     |NB               | 0.58|  0.39|          0.74|       0.34|   0.47|           0.52|        0.83|    0.64|          0.65|       0.47|   0.55|
|Machine Learning     |SVM              | 0.57|  0.41|          0.69|       0.37|   0.48|           0.52|        0.79|    0.62|          0.64|       0.48|   0.55|
|Crowd-Coding         |Single Coder     | 0.72|  0.75|          0.69|       0.84|   0.76|           0.69|        0.58|    0.63|          0.78|       0.78|   0.78|
|Crowd-Coding         |Vote (3 Coders)  | 0.77|  0.81|          0.73|       0.89|   0.80|           0.74|        0.65|    0.69|          0.83|       0.81|   0.82|
|Crowd-Coding         |Vote (5 Coders)  | 0.77|  0.81|          0.73|       0.90|   0.81|           0.73|        0.65|    0.69|          0.84|       0.80|   0.82|
|Manual Coding        |Single Coder     | 0.82|  0.82|          0.88|       0.86|   0.87|           0.76|        0.81|    0.78|          0.84|       0.80|   0.82|
|Manual Coding        |Vote (3 Coders)  | 0.88|  0.90|          0.97|       0.91|   0.94|           0.82|        0.88|    0.85|          0.87|       0.84|   0.86|

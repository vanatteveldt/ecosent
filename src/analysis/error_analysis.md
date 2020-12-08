Economic Sentiment: Error analysis
================

Read performance data

``` r
source(here("src/lib/functions.R"))
headlines = read_csv(here("data/raw/gold_sentences.csv")) %>% select(id, headline)
headlines_eng = read_csv(here("data/raw/gold_sentences.csv")) %>% select(id, deepl)
gold = read_csv(here("data/intermediate/gold.csv")) %>% rename(gold=value)
scores = read_csv(here("data/intermediate/combined_predictions.csv"), col_types = "iccccddd")
scores = scores %>% filter(is.na(language) | language != "google", variable != "recessie", variable != "boukes")  %>% mutate(value=trichotomize(value))
names = read_csv(here("src/analysis/report_names.csv"))
sections = setNames(nm=unique(names$section))
variables = setNames(nm=unique(names$variable))
perf = inner_join(scores, gold) %>% inner_join(headlines)
```

# Error analysis of CNN / Deep learning

``` r
cperf = perf %>% filter(variable=="cnn") %>% 
  group_by(id, gold, headline) %>% summarize(acc=mean(value==gold), value=mean(value), conf=mean(confidence)) 
```

Sentences misclassified as
positive

``` r
cperf %>% filter(gold!=1, value >= 0.8) %>% arrange(-conf)%>% knitr::kable()
```

|        id | gold | headline                                                                                                     | acc | value |      conf |
| --------: | ---: | :----------------------------------------------------------------------------------------------------------- | --: | ----: | --------: |
|     25859 |  \-1 | Meer faillissementen in maart                                                                                | 0.0 |   1.0 | 0.9995072 |
| 163464814 |  \-1 | Onverwachte stijging Griekse werkloosheid                                                                    | 0.0 |   1.0 | 0.9993119 |
| 148571717 |    0 | Help\! De prijzen dalen\!; Staat van de Nederlandse economie Bestendige groei, hoge werkloosheid en deflatie | 0.0 |   1.0 | 0.9987277 |
| 150280548 |    0 | Economie is gebaat bij rust; Brief van de Dag                                                                | 0.0 |   1.0 | 0.9950542 |
|     33235 |    0 | Beurshandel in teken Grieks marathonoverleg                                                                  | 0.0 |   1.0 | 0.9565173 |
| 150282119 |    0 | Moeders werken dankzij de omas; Ouders creatief in omzeilen dure kinderopvang                                | 0.1 |   0.9 | 0.8590326 |

Sentences misclassified as
negative

``` r
cperf %>% filter(gold!=-1, value <= -0.8) %>% arrange(-conf)%>% knitr::kable()
```

|        id | gold | headline                                                                  | acc | value |      conf |
| --------: | ---: | :------------------------------------------------------------------------ | --: | ----: | --------: |
| 150286193 |    0 | Breng gevaren fondsen in kaart                                            | 0.0 | \-1.0 | 0.9997255 |
| 150285464 |    0 | De extra bezuinigingen in 2013 waren niet nodig, maar ook niet schadelijk | 0.0 | \-1.0 | 0.9995977 |
| 150280829 |    1 | Huizenkoper grijpt kans; Hypotheekrente nooit zo laag                     | 0.0 | \-1.0 | 0.9945355 |
| 150285949 |    0 | Vergrijzing remt huizenprijzen                                            | 0.0 | \-1.0 | 0.9940527 |
| 150292964 |    1 | Met groei van de economie daalt aantal daklozen                           | 0.1 | \-0.8 | 0.9762979 |
| 150287154 |    0 | Zweedse centrale bank stapt over op negatieve rente                       | 0.1 | \-0.9 | 0.9513101 |
|     16609 |    0 | Wankel herstel van wereldeconomie, zegt het IMF                           | 0.1 | \-0.9 | 0.9507178 |
| 164107322 |    0 | V\&D : geen loonoffer, wel 400 ontslagen                                  | 0.1 | \-0.9 | 0.9495658 |
| 150285235 |    0 | Rechtsbijstand                                                            | 0.1 | \-0.9 | 0.9412491 |
|     13997 |    1 | Rechter draait loonsverlaging thuiszorgbedrijf terug                      | 0.0 | \-0.9 | 0.9379185 |
| 150287160 |    0 | \`Britse inflatie zal verder dalen                                        | 0.2 | \-0.8 | 0.8973732 |
|     13921 |    0 | Familiebedrijf is niet uit op snelle winst                                | 0.1 | \-0.9 | 0.8516181 |

Sentences misclassified as neutral (high
confidence)

``` r
cperf %>% filter(gold!=0, abs(value) <= .2) %>% arrange(-conf) %>% head(10) %>% knitr::kable()
```

|        id | gold | headline                                                                                        | acc | value |      conf |
| --------: | ---: | :---------------------------------------------------------------------------------------------- | --: | ----: | --------: |
| 150281956 |  \-1 | Verkoop van huizen daalt                                                                        | 0.5 |   0.0 | 0.9080192 |
| 150286325 |  \-1 | Ziek van vrijhandel                                                                             | 0.5 |   0.0 | 0.8918451 |
|     12681 |  \-1 | EU-ministers nog niet tevreden over Griekenland                                                 | 0.3 |   0.2 | 0.8471033 |
| 150285160 |  \-1 | Werkgevers torpederen caos                                                                      | 0.5 | \-0.1 | 0.8464804 |
| 150281763 |  \-1 | Grieken zijn weer platzak                                                                       | 0.4 |   0.1 | 0.8106839 |
| 148572626 |  \-1 | \[Bankroet Amsterdam. Het aantal bedrijven dat faill…\]\*                                       | 0.3 |   0.2 | 0.8042551 |
| 148572607 |    1 | Opwaartse spiraal                                                                               | 0.3 | \-0.1 | 0.7472221 |
| 150285424 |    1 | Marktwaarde op Japanse beurs overschrijdt piek van 1989; Tokio breekt een haast mythisch record | 0.3 |   0.1 | 0.7128543 |
|     10367 |  \-1 | Dijsselbloem pessimistisch over snelle stappen Grieken                                          | 0.4 |   0.0 | 0.7093660 |
| 150282126 |  \-1 | Banen weg door inzet postscooter                                                                | 0.3 | \-0.1 | 0.6885384 |

Sentences misclassified as neutral (low
confidence)

``` r
cperf %>% filter(gold!=0, abs(value) <= .2) %>% arrange(conf) %>% head(10) %>% knitr::kable()
```

|        id | gold | headline                                                  | acc | value |      conf |
| --------: | ---: | :-------------------------------------------------------- | --: | ----: | --------: |
| 150285229 |    1 | Dijsselbloem maakt voortgang met Grieken                  | 0.0 |   0.0 | 0.4485938 |
| 150281749 |    1 | Ruim 6000 banen erbij                                     | 0.0 |   0.0 | 0.4637317 |
|     27865 |    1 | Kansen in Duits vastgoed                                  | 0.0 |   0.0 | 0.4732392 |
|     31787 |  \-1 | Dubbelfout bij crisistaks                                 | 0.0 |   0.0 | 0.4819777 |
| 148572371 |    1 | Ondernemers, daar is wat te halen                         | 0.0 | \-0.2 | 0.4938424 |
| 150284575 |  \-1 | Grieken krijgen wind eurogroep van voren                  | 0.1 | \-0.1 | 0.4947177 |
| 150291453 |    1 | Partijen doen beloften alsof crisis er nooit is geweest   | 0.2 |   0.2 | 0.5008970 |
| 150760402 |  \-1 | Beleggers trekken hun geld weg van Turkse kapitaalmarkten | 0.0 |   0.0 | 0.5019708 |
|     18231 |  \-1 | Hulpprogramma Griekenland wordt niet verlengd             | 0.0 |   0.0 | 0.5025472 |
| 163416476 |  \-1 | WW teruggeschroefd                                        | 0.0 |   0.0 | 0.5031935 |

To check embeddings vectors (run in python)

    import gensim
    embeddings = gensim.models.Word2Vec.load("data/tmp/w2v_320d")
    
    def isin(w):
        try:
            embeddings.wv[w]
            return True
        except KeyError:
            return False
    
    isin("dubbelfout")
    embeddings.wv.similar_by_word("dubbelfout")

# Error analysis of NRC dictionary

Get dictionary, use corpustools to apply at token
level

``` r
nrc <- read_csv(here("data/raw/dictionaries/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.csv")) %>%
  select(c(Eng = `English (en)`, NL = `Dutch (nl)`, Positive, Negative, Fear, Trust))
d = quanteda::dictionary(list(positive = c(nrc$NL[nrc$Positive==1], nrc$NL[nrc$Trust==1]),
                    negative = c(nrc$NL[nrc$Negative==1], nrc$NL[nrc$Fear==1])))

df <- read_csv(here("data/raw/gold_sentences.csv"))
tc = corpustools::create_tcorpus(df %>% select(doc_id=id, text=dutch_lemmas))
tc$code_dictionary(d)
```

Texts that were misclassified as
positive

``` r
fp = perf %>% filter(variable == "nrc_nl", value ==1,  gold==-1) %>% pull(id)
corpustools::browse_texts(tc$subset(copy=T, subset_meta=doc_id %in% fp), category="code") 
```

Texts that were misclassified as
negative

``` r
fn = perf %>% filter(variable == "nrc_nl", value ==-1,  gold==1) %>% pull(id)
corpustools::browse_texts(tc$subset(copy=T, subset_meta=doc_id %in% fn), category="code") 
```

List of mismatched tokens and sentences in gold standard: misclassified
as
positive

``` r
matched_tokens = tc$tokens %>% filter(!is.na(code)) %>% group_by(doc_id, token, code) %>% summarize(n=n()) %>% 
  mutate(id=as.numeric(as.character(doc_id))) %>% ungroup() %>% select(-doc_id)

perf %>% filter(variable == "nrc_nl", value ==1,  gold==-1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(code, token) %>% mutate(n=sum(n)) %>% arrange(-n) %>% filter(code=="positive") %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                                                                                                                 | token     | code     | n |
| --------: | ---: | ----: | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------- | -: |
|     18463 |  \-1 |     1 | Nieuwe maatregelen in China na vrije val beurs                                                                                                           | beurs     | positive | 4 |
| 150285850 |  \-1 |     1 | Afwachtende Fed en matige groei drukken beurzen VS                                                                                                       | beurs     | positive | 4 |
| 150290282 |  \-1 |     1 | Cijfers uit VS drukken sentiment op beurzen                                                                                                              | beurs     | positive | 4 |
| 150761497 |  \-1 |     1 | Griekse beurs ook dicht                                                                                                                                  | beurs     | positive | 4 |
|     10367 |  \-1 |     1 | Dijsselbloem pessimistisch over snelle stappen Grieken                                                                                                   | snel      | positive | 2 |
| 150284144 |  \-1 |     1 | Vaste baan is niet langer de norm                                                                                                                        | vast      | positive | 2 |
| 150285850 |  \-1 |     1 | Afwachtende Fed en matige groei drukken beurzen VS                                                                                                       | groei     | positive | 2 |
| 150286500 |  \-1 |     1 | De kosten van een \`Grexit zijn veel groter dan slechts financieel                                                                                       | groot     | positive | 2 |
| 150286797 |  \-1 |     1 | Afnemende groei hypotheken                                                                                                                               | groei     | positive | 2 |
| 150287082 |  \-1 |     1 | Griekenland loopt zonder steun al snel financieel vast; De regering in Athene staat onder grote druk. Begin maart moeten de Grieken al leningen aflossen | groot     | positive | 2 |
| 150287082 |  \-1 |     1 | Griekenland loopt zonder steun al snel financieel vast; De regering in Athene staat onder grote druk. Begin maart moeten de Grieken al leningen aflossen | snel      | positive | 2 |
| 150287082 |  \-1 |     1 | Griekenland loopt zonder steun al snel financieel vast; De regering in Athene staat onder grote druk. Begin maart moeten de Grieken al leningen aflossen | vast      | positive | 2 |
|     12363 |  \-1 |     1 | Deutsche Bank bezuinigt miljarden na megaboete                                                                                                           | Bank      | positive | 1 |
|     13105 |  \-1 |     1 | Bonden bezorgd over flirt tussen Delhaize en Ahold                                                                                                       | flirt     | positive | 1 |
|     18463 |  \-1 |     1 | Nieuwe maatregelen in China na vrije val beurs                                                                                                           | maatregel | positive | 1 |
|     18463 |  \-1 |     1 | Nieuwe maatregelen in China na vrije val beurs                                                                                                           | vrij      | positive | 1 |
|     20099 |  \-1 |     1 | Gesprekken met Griekenland weer zonder resultaat afgebroken                                                                                              | gesprek   | positive | 1 |
|     20099 |  \-1 |     1 | Gesprekken met Griekenland weer zonder resultaat afgebroken                                                                                              | resultaat | positive | 1 |
|     28489 |  \-1 |     1 | Kabinet moet banendestructie aanpakken                                                                                                                   | kabinet   | positive | 1 |
| 150284144 |  \-1 |     1 | Vaste baan is niet langer de norm                                                                                                                        | baan      | positive | 1 |
| 150284575 |  \-1 |     1 | Grieken krijgen wind eurogroep van voren                                                                                                                 | krijgen   | positive | 1 |
| 150285322 |  \-1 |     1 | Coevorder voetbalclubs voorzien ondergang                                                                                                                | voorzien  | positive | 1 |
| 150285850 |  \-1 |     1 | Afwachtende Fed en matige groei drukken beurzen VS                                                                                                       | matig     | positive | 1 |
| 150287082 |  \-1 |     1 | Griekenland loopt zonder steun al snel financieel vast; De regering in Athene staat onder grote druk. Begin maart moeten de Grieken al leningen aflossen | maart     | positive | 1 |
| 150287082 |  \-1 |     1 | Griekenland loopt zonder steun al snel financieel vast; De regering in Athene staat onder grote druk. Begin maart moeten de Grieken al leningen aflossen | steun     | positive | 1 |
| 150290155 |  \-1 |     1 | Profclubs nog in rode cijfers                                                                                                                            | cijfer    | positive | 1 |
| 150290282 |  \-1 |     1 | Cijfers uit VS drukken sentiment op beurzen                                                                                                              | Cijfer    | positive | 1 |
| 150291782 |  \-1 |     1 | In een dag 300 mln. aan spaargeld weg                                                                                                                    | spaargeld | positive | 1 |
| 150291802 |  \-1 |     1 | Kans op tijdige oplossing Griekse crisis minimaal                                                                                                        | kans      | positive | 1 |
| 150291802 |  \-1 |     1 | Kans op tijdige oplossing Griekse crisis minimaal                                                                                                        | oplossing | positive | 1 |
| 150291802 |  \-1 |     1 | Kans op tijdige oplossing Griekse crisis minimaal                                                                                                        | tijdig    | positive | 1 |
| 150760402 |  \-1 |     1 | Beleggers trekken hun geld weg van Turkse kapitaalmarkten                                                                                                | geld      | positive | 1 |
| 150760402 |  \-1 |     1 | Beleggers trekken hun geld weg van Turkse kapitaalmarkten                                                                                                | trekken   | positive | 1 |
| 164107712 |  \-1 |     1 | Blok creÌÇert tweedeling op gereguleerde huurmarkt                                                                                                       | reguleren | positive | 1 |
| 164107913 |  \-1 |     1 | Slik die bittere Europese pil, zegt Cyprus                                                                                                               | pil       | positive | 1 |

List of mismatched tokens and sentences in gold standard: misclassified
as
negative

``` r
perf %>% filter(variable == "nrc_nl", value ==-1,  gold==1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(code, token) %>% mutate(n=sum(n)) %>% arrange(-n) %>% filter(code=="negative")  %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                                                                                                                                            | token       | code     | n |
| --------: | ---: | ----: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- | -: |
|     11745 |    1 |   \-1 | Cyprus heft laatste restricties op na crisis                                                                                                                                        | crisis      | negative | 2 |
| 150291453 |    1 |   \-1 | Partijen doen beloften alsof crisis er nooit is geweest                                                                                                                             | crisis      | negative | 2 |
|     11745 |    1 |   \-1 | Cyprus heft laatste restricties op na crisis                                                                                                                                        | laat        | negative | 1 |
|     17355 |    1 |   \-1 | Consumenten besteden wederom meer. Hun vertrouwen stijgt ook wee                                                                                                                    | wee         | negative | 1 |
| 150284544 |    1 |   \-1 | Minder woningen onder water                                                                                                                                                         | onder       | negative | 1 |
| 150285424 |    1 |   \-1 | Marktwaarde op Japanse beurs overschrijdt piek van 1989; Tokio breekt een haast mythisch record                                                                                     | breken      | negative | 1 |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | bezuiniging | negative | 1 |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | dwingen     | negative | 1 |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | last        | negative | 1 |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | oneerlijk   | negative | 1 |
| 150761828 |    1 |   \-1 | Deflatiespook verdwenen                                                                                                                                                             | verdwijnen  | negative | 1 |
| 163464790 |    1 |   \-1 | Geen lagere belastingen maar banen                                                                                                                                                  | belasting   | negative | 1 |

# Error analysis of English NRC dictionary

``` r
de = quanteda::dictionary(list(positive = c(nrc$Eng[nrc$Positive==1], nrc$Eng[nrc$Trust==1]),
                    negative = c(nrc$Eng[nrc$Negative==1], nrc$Eng[nrc$Fear==1])))

tce = corpustools::create_tcorpus(df %>% select(doc_id=id, text=deepl_lemmas))
tce$code_dictionary(de)
```

Texts that were misclassified as
positive

``` r
fp = perf %>% filter(variable == "nrc_deepl", value ==1,  gold==-1) %>% pull(id)
corpustools::browse_texts(tce$subset(copy=T, subset_meta=doc_id %in% fp), category="code") 
```

Texts that were misclassified as
negative

``` r
fn = perf %>% filter(variable == "nrc_deepl", value ==-1,  gold==1) %>% pull(id)
corpustools::browse_texts(tce$subset(copy=T, subset_meta=doc_id %in% fn), category="code") 
```

List of mismatched tokens and sentences in gold standard: misclassified
as
positive

``` r
matched_tokens = tce$tokens %>% filter(!is.na(code)) %>% group_by(doc_id, token, code) %>% summarize(n=n()) %>% 
  mutate(id=as.numeric(as.character(doc_id))) %>% ungroup() %>% select(-doc_id)

perf %>% filter(variable == "nrc_deepl", value ==1,  gold==-1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(code, token) %>% mutate(n=sum(n)) %>% arrange(-n) %>% filter(code=="positive") %>% 
  inner_join(headlines_eng) %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                                                                                 | token        | code     | n | deepl                                                                                                |
| --------: | ---: | ----: | :----------------------------------------------------------------------------------------------------------------------- | :----------- | :------- | -: | :--------------------------------------------------------------------------------------------------- |
|     18203 |  \-1 |     1 | Duizenden banen weg bij Air France                                                                                       | job          | positive | 6 | Thousands of jobs away from Air France                                                               |
|     25057 |  \-1 |     1 | Best Buy schrapt 1500 banen                                                                                              | job          | positive | 6 | Best Buy deletes 1500 jobs                                                                           |
|     28489 |  \-1 |     1 | Kabinet moet banendestructie aanpakken                                                                                   | job          | positive | 6 | Cabinet needs to tackle job destruction                                                              |
| 150759520 |  \-1 |     1 | Help, waar zijn al die banen?                                                                                            | job          | positive | 6 | Help, where are all these jobs?                                                                      |
| 150760005 |  \-1 |     1 | Geen loonoffer, wel 400 banen weg bij V\&D                                                                               | job          | positive | 6 | No wage sacrifice, as many as 400 jobs away from V\&D                                                |
| 164107572 |  \-1 |     1 | V\&D schrapt 400 banen, lonen hoeven niet omlaag                                                                         | job          | positive | 6 | V\&D deletes 400 jobs, wages do not have to be reduced                                               |
|     26857 |  \-1 |     1 | Spaarrente duikt onder 1 procent                                                                                         | savings      | positive | 3 | Savings interest dives below 1 percent                                                               |
| 150290043 |  \-1 |     1 | Air France en KLM moeten op zoek naar nieuwe besparingen                                                                 | savings      | positive | 3 | Air France and KLM need to look for new savings                                                      |
| 150291782 |  \-1 |     1 | In een dag 300 mln. aan spaargeld weg                                                                                    | savings      | positive | 3 | 300 million in savings in one day away                                                               |
|     17403 |  \-1 |     1 | Griekse minister: we hebben het geld niet voor volgende IMF-beta                                                         | money        | positive | 2 | Greek Minister: We dont have the money for next IMF beta                                             |
|     26857 |  \-1 |     1 | Spaarrente duikt onder 1 procent                                                                                         | interest     | positive | 2 | Savings interest dives below 1 percent                                                               |
| 150281726 |  \-1 |     1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                     | exchange     | positive | 2 | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts |
| 150281726 |  \-1 |     1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                     | interest     | positive | 2 | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts |
| 150290282 |  \-1 |     1 | Cijfers uit VS drukken sentiment op beurzen                                                                              | exchange     | positive | 2 | US figures print sentiment on stock exchanges                                                        |
| 150760402 |  \-1 |     1 | Beleggers trekken hun geld weg van Turkse kapitaalmarkten                                                                | money        | positive | 2 | Investors withdraw their money from Turkish capital markets                                          |
|     12363 |  \-1 |     1 | Deutsche Bank bezuinigt miljarden na megaboete                                                                           | Bank         | positive | 1 | Deutsche Bank cuts billions after megaboete                                                          |
|     12681 |  \-1 |     1 | EU-ministers nog niet tevreden over Griekenland                                                                          | satisfied    | positive | 1 | EU ministers not yet satisfied with Greece                                                           |
|     18231 |  \-1 |     1 | Hulpprogramma Griekenland wordt niet verlengd                                                                            | aid          | positive | 1 | The aid programme for Greece will not be extended                                                    |
|     18231 |  \-1 |     1 | Hulpprogramma Griekenland wordt niet verlengd                                                                            | extend       | positive | 1 | The aid programme for Greece will not be extended                                                    |
|     20099 |  \-1 |     1 | Gesprekken met Griekenland weer zonder resultaat afgebroken                                                              | discussion   | positive | 1 | Discussions with Greece again unsuccessfully broken off.                                             |
|     26193 |  \-1 |     1 | Wisselkoersen drukken winstgroei Michael Page                                                                            | Exchange     | positive | 1 | Exchange rates depressing earnings growth Michael Page                                               |
|     26193 |  \-1 |     1 | Wisselkoersen drukken winstgroei Michael Page                                                                            | growth       | positive | 1 | Exchange rates depressing earnings growth Michael Page                                               |
|     28489 |  \-1 |     1 | Kabinet moet banendestructie aanpakken                                                                                   | cabinet      | positive | 1 | Cabinet needs to tackle job destruction                                                              |
|     31705 |  \-1 |     1 | Laagopgeleide raakt verder achterop                                                                                      | educate      | positive | 1 | Low-educated gets further behind                                                                     |
| 150281726 |  \-1 |     1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                     | benefit      | positive | 1 | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts |
| 150281726 |  \-1 |     1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                     | bonus        | positive | 1 | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts |
| 150281726 |  \-1 |     1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                     | maximum      | positive | 1 | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts |
| 150282117 |  \-1 |     1 | Tik voor begroting door lage inflatie; Daling gasprijs is extra tegenvaller overheid                                     | extra        | positive | 1 | Tik voor begroting door lage inflatie; Daling gasprijs is extra tegenvaller overheid                 |
| 150285160 |  \-1 |     1 | Werkgevers torpederen caos                                                                                               | agreement    | positive | 1 | Employers torpedo collective agreements                                                              |
| 150285322 |  \-1 |     1 | Coevorder voetbalclubs voorzien ondergang                                                                                | football     | positive | 1 | Coevorder football clubs foresee ruin                                                                |
| 150285322 |  \-1 |     1 | Coevorder voetbalclubs voorzien ondergang                                                                                | foresee      | positive | 1 | Coevorder football clubs foresee ruin                                                                |
| 150285689 |  \-1 |     1 | IMF pleit voor wederopleving securitisaties voor mkbåÊ; Pogingen om deze markt nieuw leven in te blazen zijn onvoldoende | revival      | positive | 1 | IMF calls for revival of securitisations for SMEs; Attempts to revive this market are insufficient   |
| 150285689 |  \-1 |     1 | IMF pleit voor wederopleving securitisaties voor mkbåÊ; Pogingen om deze markt nieuw leven in te blazen zijn onvoldoende | revive       | positive | 1 | IMF calls for revival of securitisations for SMEs; Attempts to revive this market are insufficient   |
| 150286406 |  \-1 |     1 | Het lukt de AEX maar niet door de 500 puntengrens te breken +7,2% -9,3%                                                  | succeed      | positive | 1 | The AEX succeeds, but not by breaking the 500 point limit +7.2% -9.3%.                               |
| 150286500 |  \-1 |     1 | De kosten van een \`Grexit zijn veel groter dan slechts financieel                                                       | greater      | positive | 1 | The costs of a Grexit are much greater than just financial.                                          |
| 150286710 |  \-1 |     1 | Bronzen pensioenstelsel maakt Nederland gevaarlijk illiquide                                                             | system       | positive | 1 | Bronze pension system makes the Netherlands dangerously illiquid                                     |
| 150289787 |  \-1 |     1 | Lufthansa-piloten staken                                                                                                 | pilot        | positive | 1 | Lufthansa pilots strike                                                                              |
| 150290155 |  \-1 |     1 | Profclubs nog in rode cijfers                                                                                            | professional | positive | 1 | Professional clubs still in red figures                                                              |
| 150292287 |  \-1 |     1 | Duitse warenhuizen Karstadt staan voor drastische sanering                                                               | store        | positive | 1 | German department stores Karstadt stand for drastic restructuring                                    |
| 150760433 |  \-1 |     1 | Finse AAA-rating op de tocht bij kredietbeoordelaar Moodys                                                               | credit       | positive | 1 | Finnish AAA rating in question at Moodys credit rating agency                                        |
| 150760433 |  \-1 |     1 | Finse AAA-rating op de tocht bij kredietbeoordelaar Moodys                                                               | question     | positive | 1 | Finnish AAA rating in question at Moodys credit rating agency                                        |
| 163464814 |  \-1 |     1 | Onverwachte stijging Griekse werkloosheid                                                                                | increase     | positive | 1 | Unexpected increase in Greek unemployment                                                            |
| 164107712 |  \-1 |     1 | Blok creÌÇert tweedeling op gereguleerde huurmarkt                                                                       | create       | positive | 1 | Block creates dichotomy on regulated rental market                                                   |
| 164107712 |  \-1 |     1 | Blok creÌÇert tweedeling op gereguleerde huurmarkt                                                                       | regulate     | positive | 1 | Block creates dichotomy on regulated rental market                                                   |
| 164107913 |  \-1 |     1 | Slik die bittere Europese pil, zegt Cyprus                                                                               | pill         | positive | 1 | Take that bitter European pill, says Cyprus.                                                         |

List of mismatched tokens and sentences in gold standard: misclassified
as
negative

``` r
perf %>% filter(variable == "nrc_deepl", value ==-1,  gold==1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(code, token) %>% mutate(n=sum(n)) %>% arrange(-n) %>% filter(code=="negative")  %>% 
    inner_join(headlines_eng) %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                                                                                                                                            | token       | code     | n | deepl                                                                                                                                                            |
| --------: | ---: | ----: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------- | -: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 150281780 |    1 |   \-1 | Inflatiedoel in zicht; Geldontwaarding volgens ECB naar 1,8% in 2017                                                                                                                | inflation   | negative | 2 | Inflation target in sight; ECB monetary devaluation to 1.8% in 2017                                                                                              |
| 150287152 |    1 |   \-1 | Snelle daling van inflatie goed voor de koopkracht                                                                                                                                  | inflation   | negative | 2 | Rapid decline in inflation good for purchasing power                                                                                                             |
|     11745 |    1 |   \-1 | Cyprus heft laatste restricties op na crisis                                                                                                                                        | crisis      | negative | 1 | Cyprus removes latest restrictions after crisis                                                                                                                  |
|     11745 |    1 |   \-1 | Cyprus heft laatste restricties op na crisis                                                                                                                                        | remove      | negative | 1 | Cyprus removes latest restrictions after crisis                                                                                                                  |
|     11745 |    1 |   \-1 | Cyprus heft laatste restricties op na crisis                                                                                                                                        | restriction | negative | 1 | Cyprus removes latest restrictions after crisis                                                                                                                  |
| 150281053 |    1 |   \-1 | Hypotheken weer hot; Investeerders keren terug via nieuwe aanbieders                                                                                                                | Mortgage    | negative | 1 | Mortgages hot again; Investors return via new providers                                                                                                          |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | austerity   | negative | 1 | Greece is perfectly capable of bearing the burden of high public debt; It is unfair to claim that the troika has forced Greece into excessive austerity measures |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | bear        | negative | 1 | Greece is perfectly capable of bearing the burden of high public debt; It is unfair to claim that the troika has forced Greece into excessive austerity measures |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | debt        | negative | 1 | Greece is perfectly capable of bearing the burden of high public debt; It is unfair to claim that the troika has forced Greece into excessive austerity measures |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | force       | negative | 1 | Greece is perfectly capable of bearing the burden of high public debt; It is unfair to claim that the troika has forced Greece into excessive austerity measures |
| 150287132 |    1 |   \-1 | Griekenland is heel goed in staat om last van hoge overheidsschuld te dragen; Het is oneerlijk om te beweren dat de trojka Griekenland tot excessieve bezuinigingen heeft gedwongen | unfair      | negative | 1 | Greece is perfectly capable of bearing the burden of high public debt; It is unfair to claim that the troika has forced Greece into excessive austerity measures |
| 150287152 |    1 |   \-1 | Snelle daling van inflatie goed voor de koopkracht                                                                                                                                  | decline     | negative | 1 | Rapid decline in inflation good for purchasing power                                                                                                             |
| 150761828 |    1 |   \-1 | Deflatiespook verdwenen                                                                                                                                                             | Deflation   | negative | 1 | Deflation ghost disappeared                                                                                                                                      |
| 150761828 |    1 |   \-1 | Deflatiespook verdwenen                                                                                                                                                             | disappear   | negative | 1 | Deflation ghost disappeared                                                                                                                                      |
| 150761828 |    1 |   \-1 | Deflatiespook verdwenen                                                                                                                                                             | ghost       | negative | 1 | Deflation ghost disappeared                                                                                                                                      |
| 163464790 |    1 |   \-1 | Geen lagere belastingen maar banen                                                                                                                                                  | lower       | negative | 1 | No lower taxes but jobs                                                                                                                                          |
| 163464790 |    1 |   \-1 | Geen lagere belastingen maar banen                                                                                                                                                  | tax         | negative | 1 | No lower taxes but jobs                                                                                                                                          |

List of sentences misclassified by translated that were correct in
original

``` r
nl_correct = perf %>% filter(variable == "nrc_nl", value == gold)
trans_error = perf %>% filter(variable == "nrc_deepl", value != gold) %>% semi_join(nl_correct, by="id") %>% select(id, gold, value_deepl=value, headline) %>% inner_join(headlines_eng)
knitr::kable(trans_error)
```

|        id | gold | value\_deepl | headline                                                                                                                                                                            | deepl                                                                                                                                                                                    |
| --------: | ---: | -----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     10273 |    0 |            1 | Dijsselbloem wil met Griekenland naar oplossing zoeken                                                                                                                              | Dijsselbloem wants to find a solution with Greece                                                                                                                                        |
|     13623 |    0 |            1 | Rabobank verhoogt hypotheekrente                                                                                                                                                    | Rabobank increases mortgage interest rates                                                                                                                                               |
|     14315 |    0 |            1 | PvdA, D66: verder praten; PVV: nu Grexit                                                                                                                                            | PvdA, D66: talking more; PVV: now Grexit                                                                                                                                                 |
|     15261 |    0 |          \-1 | Inflatie gedaald naar laagste niveau in 27 jaar: nul procent                                                                                                                        | Inflation dropped to lowest level in 27 years: zero percent                                                                                                                              |
|     16435 |    0 |            1 | Dijsselbloem wil nog niet zeggen wanneer ABN wel naar beurs kan                                                                                                                     | Dijsselbloem does not yet mean when ABN can go public.                                                                                                                                   |
|     17825 |  \-1 |            0 | Griekenland en schuldeisers: meer onderhandelingen nodig                                                                                                                            | Greece and creditors: more negotiations needed                                                                                                                                           |
|     18203 |  \-1 |            1 | Duizenden banen weg bij Air France                                                                                                                                                  | Thousands of jobs away from Air France                                                                                                                                                   |
|     18231 |  \-1 |            1 | Hulpprogramma Griekenland wordt niet verlengd                                                                                                                                       | The aid programme for Greece will not be extended                                                                                                                                        |
|     18751 |  \-1 |            0 | Duizenden Grieken protesteren in Athene tegen bezuinigingen                                                                                                                         | Thousands of Greeks protest in Athens against austerity measures                                                                                                                         |
|     26615 |    0 |          \-1 | TSN Thuiszorg wil 650 medewerkers kwijt                                                                                                                                             | TSN Home care wants to lose 650 employees                                                                                                                                                |
|     26857 |  \-1 |            1 | Spaarrente duikt onder 1 procent                                                                                                                                                    | Savings interest dives below 1 percent                                                                                                                                                   |
|     31705 |  \-1 |            1 | Laagopgeleide raakt verder achterop                                                                                                                                                 | Low-educated gets further behind                                                                                                                                                         |
|     33235 |    0 |            1 | Beurshandel in teken Grieks marathonoverleg                                                                                                                                         | Stock exchange trade in sign Greek marathon meeting                                                                                                                                      |
|     40067 |  \-1 |            0 | 82 werknemers weg bij crÌÄå¬ches door signalen bij screening                                                                                                                        | 82 employees away from crches by signals at screening                                                                                                                                   |
|     40877 |    0 |            1 | Is rentestijging een raadsel?                                                                                                                                                       | Is rising interest rates a mystery?                                                                                                                                                      |
|     42729 |    0 |          \-1 | Belastingplan: btw gaat op veel producten naar 21 procent                                                                                                                           | Tax plan: VAT goes to 21 percent on many products                                                                                                                                        |
| 148572304 |  \-1 |            0 | Opeens waren ze blut bij de Riagg                                                                                                                                                   | Suddenly they were broke with the Riagg                                                                                                                                                  |
| 150280743 |    0 |            1 | Huizenprijzen blijven stijgen                                                                                                                                                       | House prices continue to rise                                                                                                                                                            |
| 150281391 |    1 |            0 | Sterk begin Wall Street                                                                                                                                                             | Strong beginning Wall Street                                                                                                                                                             |
| 150281460 |    0 |            1 | Na eerste aanmaning stoppen geen optie; INTERVIEW Staatssecretaris Wiebes (FinanciÌÇn)                                                                                              | No option to stop after the first reminder; INTERVIEW State Secretary Wiebes (Finance)                                                                                                   |
| 150281689 |    1 |            0 | Mkb krijgt meer                                                                                                                                                                     | SMEs get more                                                                                                                                                                            |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     |
| 150282123 |  \-1 |            0 | Werk in zorg onmogelijk door bezuinigingen                                                                                                                                          | Work in health care impossible due to budget cuts                                                                                                                                        |
| 150285232 |    1 |            0 | Webwinkel Zalando boekt eerste winst                                                                                                                                                | Webshop Zalando makes first profit                                                                                                                                                       |
| 150285235 |    0 |            1 | Rechtsbijstand                                                                                                                                                                      | Legal aid                                                                                                                                                                                |
| 150285237 |    0 |          \-1 | OZB-aanslag                                                                                                                                                                         | OZB attack                                                                                                                                                                               |
| 150285689 |  \-1 |            1 | IMF pleit voor wederopleving securitisaties voor mkbåÊ; Pogingen om deze markt nieuw leven in te blazen zijn onvoldoende                                                            | IMF calls for revival of securitisations for SMEs; Attempts to revive this market are insufficient                                                                                       |
| 150285703 |    0 |            1 | Spaargrens                                                                                                                                                                          | Savings limit                                                                                                                                                                            |
| 150285890 |    0 |            1 | Waartoe dient het handelsverdrag?                                                                                                                                                   | What is the purpose of the trade agreement?                                                                                                                                              |
| 150285942 |  \-1 |            0 | Brussel ligt dwars bij nieuw instituut voor hypotheken                                                                                                                              | Brussels is bordering on new institute for mortgages                                                                                                                                     |
| 150285949 |    0 |          \-1 | Vergrijzing remt huizenprijzen                                                                                                                                                      | Ageing inhibits house prices                                                                                                                                                             |
| 150286193 |    0 |          \-1 | Breng gevaren fondsen in kaart                                                                                                                                                      | Map dangers funds                                                                                                                                                                        |
| 150286406 |  \-1 |            1 | Het lukt de AEX maar niet door de 500 puntengrens te breken +7,2% -9,3%                                                                                                             | The AEX succeeds, but not by breaking the 500 point limit +7.2% -9.3%.                                                                                                                   |
| 150286710 |  \-1 |            1 | Bronzen pensioenstelsel maakt Nederland gevaarlijk illiquide                                                                                                                        | Bronze pension system makes the Netherlands dangerously illiquid                                                                                                                         |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? |
| 150287152 |    1 |          \-1 | Snelle daling van inflatie goed voor de koopkracht                                                                                                                                  | Rapid decline in inflation good for purchasing power                                                                                                                                     |
| 150287154 |    0 |            1 | Zweedse centrale bank stapt over op negatieve rente                                                                                                                                 | Swedish central bank switches to negative interest rate                                                                                                                                  |
| 150287733 |  \-1 |            0 | FNV pleit voor crisispakket pensioenfondsen                                                                                                                                         | FNV advocates crisis package for pension funds                                                                                                                                           |
| 150287797 |    0 |            1 | Zo word je een succesvolle huisjesmelker                                                                                                                                            | This is how you become a successful cottage grower…                                                                                                                                      |
| 150287829 |    0 |            1 | Advies: verzacht de bezuiniging op cultuur                                                                                                                                          | Advice: softens the cutbacks on culture                                                                                                                                                  |
| 150290321 |    0 |            1 | Vaak ander doel vakantiegeld                                                                                                                                                        | Often different purpose holiday pay                                                                                                                                                      |
| 150290550 |    0 |            1 | Beurs blijft lokken; Nieuwe site over beursgeschiedenis                                                                                                                             | Stock market continues to attract; New site on stock market history                                                                                                                      |
| 150290728 |    0 |            1 | SER: eerder hulp bij zoeken baan                                                                                                                                                    | SER: earlier job search assistance                                                                                                                                                       |
| 150290740 |    1 |            0 | ECB geeft Grieken lucht                                                                                                                                                             | ECB gives Greece air                                                                                                                                                                     |
| 150292328 |    1 |            0 | Europa krijgt zijn prestigieuze investeringsfonds                                                                                                                                   | Europe gets its prestigious investment fund                                                                                                                                              |
| 150292763 |    0 |            1 | Werken aan de Nieuwe Zijderoute                                                                                                                                                     | Working on the New Silk Road                                                                                                                                                             |
| 150759335 |    1 |            0 | Pensioenen iets beter                                                                                                                                                               | Pensions slightly better                                                                                                                                                                 |
| 150759764 |    0 |            1 | Pon koopt in VS fietsfabrikant                                                                                                                                                      | Pon buys in US bike manufacturer                                                                                                                                                         |
| 150760005 |  \-1 |            1 | Geen loonoffer, wel 400 banen weg bij V\&D                                                                                                                                          | No wage sacrifice, as many as 400 jobs away from V\&D                                                                                                                                    |
| 150760433 |  \-1 |            1 | Finse AAA-rating op de tocht bij kredietbeoordelaar Moodys                                                                                                                          | Finnish AAA rating in question at Moodys credit rating agency                                                                                                                            |
| 150760841 |    0 |          \-1 | Beleggers wachten op referendum                                                                                                                                                     | Investors are waiting for a referendum                                                                                                                                                   |
| 150761515 |    0 |            1 | EU-geld voor werkloosheid                                                                                                                                                           | EU money for unemployment                                                                                                                                                                |
| 150761558 |    0 |            1 | Lage rente houdt aan                                                                                                                                                                | Low interest rate continues                                                                                                                                                              |
| 150762167 |  \-1 |            0 | Meeste pensioenen onder water                                                                                                                                                       | Most pensions under water                                                                                                                                                                |

Browser

``` r
tce$meta
```

    ##      doc_id
    ##   1:  10273
    ##   2:  10367
    ##   3:  10881
    ##   4:  11191
    ##   5:  11745
    ##  ---       
    ## 296:  42729
    ## 297:  43227
    ## 298:  43269
    ## 299:  43589
    ## 300:  43757

``` r
tce$set_meta("gold_value", gold$gold[match(tce$get_meta("doc_id"), as.character(gold$id))])
tce$set_meta("nrc_deepl", trans_error$value_deepl[match(tce$get_meta("doc_id"), as.character(trans_error$id))])
corpustools::browse_texts(tce$subset(copy=T, subset_meta=doc_id %in% trans_error$id), category="code") 
```

Tokens

``` r
trans_error %>% 
  inner_join(matched_tokens) %>% group_by(code, token) %>% mutate(n=sum(n)) %>% arrange(-n) %>% filter(code=="positive") %>% 
  knitr::kable()
```

|        id | gold | value\_deepl | headline                                                                                                                                                                            | deepl                                                                                                                                                                                    | token        | code     | n |
| --------: | ---: | -----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- | :------- | -: |
|     13623 |    0 |            1 | Rabobank verhoogt hypotheekrente                                                                                                                                                    | Rabobank increases mortgage interest rates                                                                                                                                               | interest     | positive | 6 |
|     26857 |  \-1 |            1 | Spaarrente duikt onder 1 procent                                                                                                                                                    | Savings interest dives below 1 percent                                                                                                                                                   | interest     | positive | 6 |
|     40877 |    0 |            1 | Is rentestijging een raadsel?                                                                                                                                                       | Is rising interest rates a mystery?                                                                                                                                                      | interest     | positive | 6 |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     | interest     | positive | 6 |
| 150287154 |    0 |            1 | Zweedse centrale bank stapt over op negatieve rente                                                                                                                                 | Swedish central bank switches to negative interest rate                                                                                                                                  | interest     | positive | 6 |
| 150761558 |    0 |            1 | Lage rente houdt aan                                                                                                                                                                | Low interest rate continues                                                                                                                                                              | interest     | positive | 6 |
|     18203 |  \-1 |            1 | Duizenden banen weg bij Air France                                                                                                                                                  | Thousands of jobs away from Air France                                                                                                                                                   | job          | positive | 3 |
| 150280743 |    0 |            1 | Huizenprijzen blijven stijgen                                                                                                                                                       | House prices continue to rise                                                                                                                                                            | continue     | positive | 3 |
| 150290550 |    0 |            1 | Beurs blijft lokken; Nieuwe site over beursgeschiedenis                                                                                                                             | Stock market continues to attract; New site on stock market history                                                                                                                      | continue     | positive | 3 |
| 150290728 |    0 |            1 | SER: eerder hulp bij zoeken baan                                                                                                                                                    | SER: earlier job search assistance                                                                                                                                                       | job          | positive | 3 |
| 150760005 |  \-1 |            1 | Geen loonoffer, wel 400 banen weg bij V\&D                                                                                                                                          | No wage sacrifice, as many as 400 jobs away from V\&D                                                                                                                                    | job          | positive | 3 |
| 150761558 |    0 |            1 | Lage rente houdt aan                                                                                                                                                                | Low interest rate continues                                                                                                                                                              | continue     | positive | 3 |
|     18231 |  \-1 |            1 | Hulpprogramma Griekenland wordt niet verlengd                                                                                                                                       | The aid programme for Greece will not be extended                                                                                                                                        | aid          | positive | 2 |
|     26857 |  \-1 |            1 | Spaarrente duikt onder 1 procent                                                                                                                                                    | Savings interest dives below 1 percent                                                                                                                                                   | savings      | positive | 2 |
|     33235 |    0 |            1 | Beurshandel in teken Grieks marathonoverleg                                                                                                                                         | Stock exchange trade in sign Greek marathon meeting                                                                                                                                      | exchange     | positive | 2 |
|     33235 |    0 |            1 | Beurshandel in teken Grieks marathonoverleg                                                                                                                                         | Stock exchange trade in sign Greek marathon meeting                                                                                                                                      | trade        | positive | 2 |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     | exchange     | positive | 2 |
| 150285235 |    0 |            1 | Rechtsbijstand                                                                                                                                                                      | Legal aid                                                                                                                                                                                | aid          | positive | 2 |
| 150285703 |    0 |            1 | Spaargrens                                                                                                                                                                          | Savings limit                                                                                                                                                                            | savings      | positive | 2 |
| 150285890 |    0 |            1 | Waartoe dient het handelsverdrag?                                                                                                                                                   | What is the purpose of the trade agreement?                                                                                                                                              | trade        | positive | 2 |
|     10273 |    0 |            1 | Dijsselbloem wil met Griekenland naar oplossing zoeken                                                                                                                              | Dijsselbloem wants to find a solution with Greece                                                                                                                                        | solution     | positive | 1 |
|     13623 |    0 |            1 | Rabobank verhoogt hypotheekrente                                                                                                                                                    | Rabobank increases mortgage interest rates                                                                                                                                               | increase     | positive | 1 |
|     14315 |    0 |            1 | PvdA, D66: verder praten; PVV: nu Grexit                                                                                                                                            | PvdA, D66: talking more; PVV: now Grexit                                                                                                                                                 | talk         | positive | 1 |
|     15261 |    0 |          \-1 | Inflatie gedaald naar laagste niveau in 27 jaar: nul procent                                                                                                                        | Inflation dropped to lowest level in 27 years: zero percent                                                                                                                              | level        | positive | 1 |
|     16435 |    0 |            1 | Dijsselbloem wil nog niet zeggen wanneer ABN wel naar beurs kan                                                                                                                     | Dijsselbloem does not yet mean when ABN can go public.                                                                                                                                   | public       | positive | 1 |
|     18231 |  \-1 |            1 | Hulpprogramma Griekenland wordt niet verlengd                                                                                                                                       | The aid programme for Greece will not be extended                                                                                                                                        | extend       | positive | 1 |
|     18751 |  \-1 |            0 | Duizenden Grieken protesteren in Athene tegen bezuinigingen                                                                                                                         | Thousands of Greeks protest in Athens against austerity measures                                                                                                                         | measure      | positive | 1 |
|     31705 |  \-1 |            1 | Laagopgeleide raakt verder achterop                                                                                                                                                 | Low-educated gets further behind                                                                                                                                                         | educate      | positive | 1 |
| 150281460 |    0 |            1 | Na eerste aanmaning stoppen geen optie; INTERVIEW Staatssecretaris Wiebes (FinanciÌÇn)                                                                                              | No option to stop after the first reminder; INTERVIEW State Secretary Wiebes (Finance)                                                                                                   | option       | positive | 1 |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     | benefit      | positive | 1 |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     | bonus        | positive | 1 |
| 150281726 |  \-1 |            1 | Pensioenfonds klem door ECB; Van beursbonanza wordt niet maximaal geprofiteerd, lage rente doet pijn                                                                                | Pension fund clampdown by ECB; no maximum benefit from stock exchange bonus, low interest rate hurts                                                                                     | maximum      | positive | 1 |
| 150282123 |  \-1 |            0 | Werk in zorg onmogelijk door bezuinigingen                                                                                                                                          | Work in health care impossible due to budget cuts                                                                                                                                        | budget       | positive | 1 |
| 150285235 |    0 |            1 | Rechtsbijstand                                                                                                                                                                      | Legal aid                                                                                                                                                                                | legal        | positive | 1 |
| 150285689 |  \-1 |            1 | IMF pleit voor wederopleving securitisaties voor mkbåÊ; Pogingen om deze markt nieuw leven in te blazen zijn onvoldoende                                                            | IMF calls for revival of securitisations for SMEs; Attempts to revive this market are insufficient                                                                                       | revival      | positive | 1 |
| 150285689 |  \-1 |            1 | IMF pleit voor wederopleving securitisaties voor mkbåÊ; Pogingen om deze markt nieuw leven in te blazen zijn onvoldoende                                                            | IMF calls for revival of securitisations for SMEs; Attempts to revive this market are insufficient                                                                                       | revive       | positive | 1 |
| 150285890 |    0 |            1 | Waartoe dient het handelsverdrag?                                                                                                                                                   | What is the purpose of the trade agreement?                                                                                                                                              | agreement    | positive | 1 |
| 150285942 |  \-1 |            0 | Brussel ligt dwars bij nieuw instituut voor hypotheken                                                                                                                              | Brussels is bordering on new institute for mortgages                                                                                                                                     | institute    | positive | 1 |
| 150286406 |  \-1 |            1 | Het lukt de AEX maar niet door de 500 puntengrens te breken +7,2% -9,3%                                                                                                             | The AEX succeeds, but not by breaking the 500 point limit +7.2% -9.3%.                                                                                                                   | succeed      | positive | 1 |
| 150286710 |  \-1 |            1 | Bronzen pensioenstelsel maakt Nederland gevaarlijk illiquide                                                                                                                        | Bronze pension system makes the Netherlands dangerously illiquid                                                                                                                         | system       | positive | 1 |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? | income       | positive | 1 |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? | model        | positive | 1 |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? | rejoice      | positive | 1 |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? | show         | positive | 1 |
| 150286851 |    0 |            1 | `Noors model vertoont barstjes; Terwijl Nederland de aardgasbaten verjubelde, stopten de Noren de inkomsten uit olie in een speciaal fonds. Moeten`wij dat voorbeeld alsnog volgen? | The Norwegian model shows cracks; while the Netherlands rejoiced in the natural gas revenues, the Norwegians put the income from oil into a special fund. Should we follow that example? | special      | positive | 1 |
| 150287152 |    1 |          \-1 | Snelle daling van inflatie goed voor de koopkracht                                                                                                                                  | Rapid decline in inflation good for purchasing power                                                                                                                                     | good         | positive | 1 |
| 150287154 |    0 |            1 | Zweedse centrale bank stapt over op negatieve rente                                                                                                                                 | Swedish central bank switches to negative interest rate                                                                                                                                  | bank         | positive | 1 |
| 150287733 |  \-1 |            0 | FNV pleit voor crisispakket pensioenfondsen                                                                                                                                         | FNV advocates crisis package for pension funds                                                                                                                                           | advocate     | positive | 1 |
| 150287797 |    0 |            1 | Zo word je een succesvolle huisjesmelker                                                                                                                                            | This is how you become a successful cottage grower…                                                                                                                                      | successful   | positive | 1 |
| 150287829 |    0 |            1 | Advies: verzacht de bezuiniging op cultuur                                                                                                                                          | Advice: softens the cutbacks on culture                                                                                                                                                  | advice       | positive | 1 |
| 150287829 |    0 |            1 | Advies: verzacht de bezuiniging op cultuur                                                                                                                                          | Advice: softens the cutbacks on culture                                                                                                                                                  | culture      | positive | 1 |
| 150290321 |    0 |            1 | Vaak ander doel vakantiegeld                                                                                                                                                        | Often different purpose holiday pay                                                                                                                                                      | holiday      | positive | 1 |
| 150290321 |    0 |            1 | Vaak ander doel vakantiegeld                                                                                                                                                        | Often different purpose holiday pay                                                                                                                                                      | pay          | positive | 1 |
| 150290728 |    0 |            1 | SER: eerder hulp bij zoeken baan                                                                                                                                                    | SER: earlier job search assistance                                                                                                                                                       | assistance   | positive | 1 |
| 150292763 |    0 |            1 | Werken aan de Nieuwe Zijderoute                                                                                                                                                     | Working on the New Silk Road                                                                                                                                                             | silk         | positive | 1 |
| 150759764 |    0 |            1 | Pon koopt in VS fietsfabrikant                                                                                                                                                      | Pon buys in US bike manufacturer                                                                                                                                                         | manufacturer | positive | 1 |
| 150760433 |  \-1 |            1 | Finse AAA-rating op de tocht bij kredietbeoordelaar Moodys                                                                                                                          | Finnish AAA rating in question at Moodys credit rating agency                                                                                                                            | credit       | positive | 1 |
| 150760433 |  \-1 |            1 | Finse AAA-rating op de tocht bij kredietbeoordelaar Moodys                                                                                                                          | Finnish AAA rating in question at Moodys credit rating agency                                                                                                                            | question     | positive | 1 |
| 150761515 |    0 |            1 | EU-geld voor werkloosheid                                                                                                                                                           | EU money for unemployment                                                                                                                                                                | money        | positive | 1 |

# Naive Bayes features and error analysis

``` r
f = read_csv(here("data/intermediate/nb_features.csv")) %>% 
  pivot_longer(-feature, names_to="class") %>% mutate(p=exp(value))
intercept = f %>% filter(feature == "___INTERCEPT___") %>% select(class, p)
nbfeatures = f %>% filter(feature != "___INTERCEPT___") %>% inner_join(intercept, by="class", suffix=c("", "_cls")) %>% 
  mutate(pp=p*p_cls) %>% group_by(feature) %>% mutate(max=max(pp), sum=sum(pp)) %>% 
  filter(pp==max) %>% mutate(norm=pp/sum) %>% arrange(-norm) %>% 
  select(feature, class, norm)
nbfeatures %>% head(10) %>% knitr::kable()
```

| feature      | class |      norm |
| :----------- | :---- | --------: |
| agenda       | 0     | 0.9118748 |
| vandaag      | 0     | 0.8043035 |
| schrappen    | \-1   | 0.7935605 |
| dankzij      | 1     | 0.7929150 |
| duizend      | \-1   | 0.7870642 |
| optimistisch | 1     | 0.7723110 |
| dreigen      | \-1   | 0.7651621 |
| vrezen       | \-1   | 0.7471035 |
| positief     | 1     | 0.7342500 |
| waarschuwen  | \-1   | 0.7326269 |

Positive tokens in texts misclassified as
positive

``` r
matched_tokens = tc$tokens %>% inner_join(nbfeatures, by=c(token="feature")) %>% select(doc_id, token, class, norm) %>% 
   mutate(id=as.numeric(as.character(doc_id))) %>% ungroup() %>% select(-doc_id)
perf %>% filter(variable == "nb", value ==1,  gold==-1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(class, token) %>% arrange(-norm) %>% filter(class==1) %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                  | token         | class |      norm |
| --------: | ---: | ----: | :-------------------------------------------------------- | :------------ | :---- | --------: |
|     25859 |  \-1 |     1 | Meer faillissementen in maart                             | faillissement | 1     | 0.5762018 |
| 148572626 |  \-1 |     1 | \[Bankroet Amsterdam. Het aantal bedrijven dat faill…\]\* | aantal        | 1     | 0.5704208 |
| 150285322 |  \-1 |     1 | Coevorder voetbalclubs voorzien ondergang                 | voorzien      | 1     | 0.5292223 |
| 150287149 |  \-1 |     1 | Commerzbank voorziet nieuwe tegenslagen                   | voorzien      | 1     | 0.5292223 |
| 163464814 |  \-1 |     1 | Onverwachte stijging Griekse werkloosheid                 | stijging      | 1     | 0.4644110 |
| 163464814 |  \-1 |     1 | Onverwachte stijging Griekse werkloosheid                 | werkloosheid  | 1     | 0.4621316 |
| 150286797 |  \-1 |     1 | Afnemende groei hypotheken                                | groei         | 1     | 0.4577019 |

Negative tokens in texts misclassified as
negative

``` r
perf %>% filter(variable == "nb", value ==-1,  gold==1) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(class, token) %>% arrange(-norm) %>% filter(class==-1) %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                             | token   | class |      norm |
| --------: | ---: | ----: | :------------------------------------------------------------------- | :------ | :---- | --------: |
| 150281780 |    1 |   \-1 | Inflatiedoel in zicht; Geldontwaarding volgens ECB naar 1,8% in 2017 | zicht   | \-1   | 0.5669880 |
| 150284544 |    1 |   \-1 | Minder woningen onder water                                          | weinig  | \-1   | 0.5613787 |
| 150284544 |    1 |   \-1 | Minder woningen onder water                                          | water   | \-1   | 0.4848504 |
| 150284544 |    1 |   \-1 | Minder woningen onder water                                          | onder   | \-1   | 0.4760731 |
|     13997 |    1 |   \-1 | Rechter draait loonsverlaging thuiszorgbedrijf terug                 | rechter | \-1   | 0.4747719 |
|     13997 |    1 |   \-1 | Rechter draait loonsverlaging thuiszorgbedrijf terug                 | terug   | \-1   | 0.4635679 |
| 150291453 |    1 |   \-1 | Partijen doen beloften alsof crisis er nooit is geweest              | crisis  | \-1   | 0.4557090 |

Non-neutral tokens in misclassified neutral
texts

``` r
perf %>% filter(variable == "nb", value != 0,  gold==0) %>% select(id, gold, value, headline) %>% 
  inner_join(matched_tokens) %>% group_by(class, token) %>% arrange(-norm) %>% filter(class!=0) %>% 
  knitr::kable()
```

|        id | gold | value | headline                                                                                                     | token          | class |      norm |
| --------: | ---: | ----: | :----------------------------------------------------------------------------------------------------------- | :------------- | :---- | --------: |
| 150282119 |    0 |     1 | Moeders werken dankzij de omas; Ouders creatief in omzeilen dure kinderopvang                                | dankzij        | 1     | 0.7929150 |
| 150287154 |    0 |   \-1 | Zweedse centrale bank stapt over op negatieve rente                                                          | negatief       | \-1   | 0.6952989 |
| 150285890 |    0 |   \-1 | Waartoe dient het handelsverdrag?                                                                            | handelsverdrag | \-1   | 0.5902042 |
| 150761251 |    0 |   \-1 | Arbeidsverhoudingen Zzp-aftrek verdeelt vakbonden ; Economie Kort                                            | vakbond        | \-1   | 0.5667592 |
| 150285233 |    0 |   \-1 | Net sluit zich rond Speed Events                                                                             | rond           | \-1   | 0.5456509 |
| 150282410 |    0 |     1 | Nerd in de lift, manager buitenspel                                                                          | lift           | 1     | 0.5406090 |
| 150287829 |    0 |   \-1 | Advies: verzacht de bezuiniging op cultuur                                                                   | bezuiniging    | \-1   | 0.5311232 |
| 150284361 |    0 |   \-1 | Maar we zijn hier in Emmen wel heel gelukkig                                                                 | we             | \-1   | 0.4937360 |
| 150285134 |    0 |   \-1 | We hebben dus de pest aan ouderen                                                                            | we             | \-1   | 0.4937360 |
| 150290877 |    0 |   \-1 | Voorstel komt te snel, eerst even uitblazen                                                                  | even           | \-1   | 0.4834903 |
| 150282229 |    0 |   \-1 | Onderzoek rentebeleid banken                                                                                 | onderzoek      | \-1   | 0.4802033 |
| 148571717 |    0 |     1 | Help\! De prijzen dalen\!; Staat van de Nederlandse economie Bestendige groei, hoge werkloosheid en deflatie | dalen          | \-1   | 0.4669020 |
| 150291524 |    0 |   \-1 | In 2030 geen import energie meer door VS                                                                     | door           | \-1   | 0.4655315 |
| 148571717 |    0 |     1 | Help\! De prijzen dalen\!; Staat van de Nederlandse economie Bestendige groei, hoge werkloosheid en deflatie | werkloosheid   | 1     | 0.4621316 |
| 148571717 |    0 |     1 | Help\! De prijzen dalen\!; Staat van de Nederlandse economie Bestendige groei, hoge werkloosheid en deflatie | groei          | 1     | 0.4577019 |
| 148571717 |    0 |     1 | Help\! De prijzen dalen\!; Staat van de Nederlandse economie Bestendige groei, hoge werkloosheid en deflatie | economie       | 1     | 0.4414231 |
| 150761251 |    0 |   \-1 | Arbeidsverhoudingen Zzp-aftrek verdeelt vakbonden ; Economie Kort                                            | economie       | 1     | 0.4414231 |
| 164107571 |    0 |   \-1 | Het gevecht voor 15 dollar per uur                                                                           | dollar         | \-1   | 0.4161503 |
| 150285134 |    0 |   \-1 | We hebben dus de pest aan ouderen                                                                            | oud            | \-1   | 0.4139071 |
|     30591 |    0 |   \-1 | Wall Street opent vrijwel onveranderd                                                                        | openen         | \-1   | 0.4084662 |
| 150285233 |    0 |   \-1 | Net sluit zich rond Speed Events                                                                             | sluiten        | \-1   | 0.4059416 |
| 150285233 |    0 |   \-1 | Net sluit zich rond Speed Events                                                                             | zich           | \-1   | 0.3982812 |
| 150284361 |    0 |   \-1 | Maar we zijn hier in Emmen wel heel gelukkig                                                                 | heel           | \-1   | 0.3780876 |
| 164107571 |    0 |   \-1 | Het gevecht voor 15 dollar per uur                                                                           | per            | \-1   | 0.3731564 |

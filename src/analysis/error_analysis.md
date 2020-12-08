Economic Sentiment: Error analysis
================

Read performance data

``` r
source(here("src/lib/functions.R"))
headlines = read_csv(here("data/raw/gold_sentences.csv")) %>% select(id, headline)
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

Sentences misclassified as positive

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

Sentences misclassified as negative

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

Sentences misclassified as neutral (high confidence)

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

Sentences misclassified as neutral (low confidence)

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

# Error analysis of NRC dictionary

Get dictionary, use corpustools to apply at token level

``` r
nrc <- read_csv(here("data/raw/dictionaries/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.csv")) %>%
  select(c(Eng = `English (en)`, NL = `Dutch (nl)`, Positive, Negative, Fear, Trust))
d = quanteda::dictionary(list(positive = c(nrc$NL[nrc$Positive==1], nrc$NL[nrc$Trust==1]),
                    negative = c(nrc$NL[nrc$Negative==1], nrc$NL[nrc$Fear==1])))

df <- read_csv(here("data/raw/gold_sentences.csv"))
tc = corpustools::create_tcorpus(df %>% select(doc_id=id, text=dutch_lemmas))
tc$code_dictionary(d)
```

Texts that were misclassified as positive

``` r
fp = perf %>% filter(variable == "nrc_nl", value ==1,  gold==-1) %>% pull(id)
corpustools::browse_texts(tc$subset(copy=T, subset_meta=doc_id %in% fp), category="code") 
```

Texts that were misclassified as negative

``` r
fn = perf %>% filter(variable == "nrc_nl", value ==-1,  gold==1) %>% pull(id)
corpustools::browse_texts(tc$subset(copy=T, subset_meta=doc_id %in% fn), category="code") 
```

List of mismatched tokens and sentences in gold standard: misclassified
as positive

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
as negative

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

Positive tokens in texts misclassified as positive

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

Negative tokens in texts misclassified as negative

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

Non-neutral tokens in misclassified neutral texts

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

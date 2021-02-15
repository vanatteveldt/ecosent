# Crowd coding instructions

We used Figure Eight for crowd coding. 
As described in the article, each headline from the gold standard was coded by 5 crowd coders.
A set of 66 "quiz" questions were used in an initial quiz and with one quiz question per page.
Pages consisted of 5 headlines to code, with a $0.10 payment per page. 
Coders that dropped below 70% accuracy were removed. 

For technical reasons, the headlines were split over multiple jobs. 
In one job, there were 9 initial contributors, 7 of which who passed the quiz and one dropping out during the work.
The remaining 6 coders contributed 492 sentiment judgments of 97 headlines. 

# Job wording

The text of the question was:

```
Hieronder staat de kop of titel van een artikel uit de krant of van online nieuws. Lees deze kop aandachtig door.

{{headline}}

Is deze kop positief of negatief over de economie?
() Positief
() Neutraal
() Negatief
```

Informal translation: "Below there is a headline or title of a newspaper or online news article. Read this headline carefully" .. "Is this headline positive or negative about the economy?"

# Instructions

Below is the text that was used to instruct the coders: 

Deze taak gaat over de toon van krantenkoppen of titels van online nieuwsitems over economisch nieuws. Van elke kop willen we weten of de kop negatief of positief is. Een kop is alleen negatief of positief als er een duidelijk en expliciet oordeel wordt gegeven over economische ontwikkelingen. Je mag ook aangeven dat een kop neutraal is. 
Een kop is positief als bijvoorbeeld gesteld wordt dat de economie groeit, of het consumentenvertrouwen stijgt, er meer banen komen, of als een bedrijf groeit, winst maakt, of de productie uitbreidt. 
Een kop is negatief als er bijvoorbeeld staat dat het slecht gaat met de economie, de werkloosheid toeneemt, de huizenverkoop afneemt, of een bedrijf failliet gaat om mensen ontslaat. 
Als een kop alleen maar feiten noemt zonder daar een oordeel bij te geven is het artikel neutraal. Bijvoorbeeld als de werkloosheid 7% is, maar als er niet staat of dat veel of weinig is. 

Bijvoorbeeld:
*Werkloosheid is 7%*
deze kop is neutraal, er wordt alleen een feit genoemd

*Werkloosheid is toegenomen tot 7%*
deze kop is negatief: de werkloosheid is afgenomen

*Werkloosheid is lager dan gevreesd *
deze kop is positief: de werkloosheid is laag
 
Als een artikel gemengd is of als het onduidelijk is of het positief of negatief is dan wordt het als neutraal gecodeerd:
Economie groeit maar salarissen stagneren
deze kop is neutraal, want er staat zowel een negatief (salaris stagneert) als positief (economie groeit) oordeel. 
 
Als het niet duidelijk is of de kop over de economie gaat, maar wel duidelijk is dat het positief of negatief is, codeer de kop dan als positief of negatief. Bijvoorbeeld:

*Bar en boos*
Deze kop is negatief. We weten niet zeker of het over de economie gaat, maar het is zeker negatief.
 
Soms zijn er koppen waarin er iets positiefs of negatiefs wordt gezegd over een specifiek persoon zonder dat het iets zegt over de economie. Deze codeer je als neutraal. Als een kop echter zegt dat het goed (of slecht) gaat met een bedrijf dan codeer je het als positief (of juist negatief). Als bedrijven winst maken gaat het immers meestal goed met de economie. 

*Janssen verkozen tot ondernemer van het jaar*
Deze kop is neutraal: ook in slechte jaren is er een ondernemer van het jaar. Dit zegt dus niets over of het slecht of goed gaat.


*Pietersen nieuwe topman KPN*
Deze kop is ook neutraal: het is goed nieuws voor Pietersen, maar of het goed voor de economie is weten we niet. Ook in slechte tijden kan een bedrijf een nieuwe topman krijgen


*Winst Google met 9% gegroeid*
Deze kop is positief: het gaat goed met Google, en dus (vermoedelijk) met de economie.


*KPN neemt Telfort over*
Deze kop is neutraal. Misschien is dit goed voor KPN en Telfort, maar misschien ook niet.


Het gaat in deze taak om het oordeel van de schrijver over de economie, en niet om wat jij persoonlijk vindt van de economie. 

*BTW wordt verhoogd naar 9%*
Deze kop is neutraal.  In de kop staat niet of dit  goed of slecht is voor de economie. Misschien is het vervelend als de BTW omhoog gaat, maar misschien is het juist een goede maatregel.


*Economie krimpt door BTW verhoging *
Dit is wel negatief:  hier wordt duidelijk gesteld dat de economie zal krimpen door de verhoging. 

## Translated Instructions

For convenience, below is the **unchecked** deepl.com translation of the instructions:

```
This task is about the tone of newspaper headlines or titles of online news items about economic news. Of each headline, we want to know whether the headline is negative or positive. A headline is negative or positive only if it makes a clear and explicit judgment about economic developments. You may also indicate that a headline is neutral. 
A headline is positive if, for example, it states that the economy is growing, or consumer confidence is rising, or there are more jobs, or if a company is growing, making profits, or expanding production. 
A headline is negative if, for example, it says that the economy is doing badly, unemployment is rising, home sales are falling, or a company is going bankrupt or laying people off. 
If a headline just states facts without giving an opinion, the article is neutral. For example, if unemployment is 7%, but it does not say whether that is a lot or a little. 
For example:
Unemployment is 7%
this headline is neutral, it just states a fact


Unemployment has increased to 7%
this headline is negative: unemployment has decreased


Unemployment is lower than feared 
this headline is positive: unemployment is low
 
If an article is mixed or it is unclear whether it is positive or negative then it is coded as neutral:
Economy grows but salaries stagnate
this headline is neutral because it contains both a negative (wages stagnate) and positive (economy grows) opinion. 
 
If it is not clear whether the headline is about the economy, but it is clear that it is positive or negative, code the headline as positive or negative. For example:
Bar and Angry
This headline is negative. We're not sure if it's about the economy, but it's definitely negative.
 
Sometimes there are headlines where it says something positive or negative about a specific person without saying anything about the economy. You code these as neutral. However, if a headline says that a company is doing well (or badly) then you code it as positive (or negative). After all, if companies make a profit, the economy is usually doing well. 
Janssen elected entrepreneur of the year
This headline is neutral: even in bad years there is an entrepreneur of the year. This says nothing about whether things are going well or badly.


Pietersen new KPN CEO 
This headline is also neutral: it is good news for Pietersen, but whether it is good for the economy we do not know. Even in bad times a company can get a new topman


Google Profits Grow by 9%
This headline is positive: Google is doing well, and thus (presumably) the economy.


KPN takes over Telfort
This headline is neutral. Maybe this is good for KPN and Telfort, but maybe not.


The task at hand is the writer's assessment of the economy, not what you personally think of the economy. 
VAT will be increased to 9%
This headline is neutral.  The headline does not say whether this is good or bad for the economy. Maybe it is annoying when the VAT goes up, but maybe it is a good measure.


Economy shrinks due to VAT increase 
This is negative: it clearly states that the economy will shrink because of the increase.

Translated with www.DeepL.com/Translator (free version)
```






'''
DANEW implementation based on :

@article{Moors2013,
abstract = {This article presents norms of valence/pleasantness, activity/arousal, power/dominance, and age of acquisition for 4,300 Dutch words, mainly nouns, adjectives, adverbs, and verbs. The norms are based on ratings with a 7-point Likert scale by independent groups of students from two Belgian (Ghent and Leuven) and two Dutch (Rotterdam and Leiden-Amsterdam) samples. For each variable, we obtained high split-half reliabilities within each sample and high correlations between samples. In addition, the valence ratings of a previous, more limited study (Hermans {\&} De Houwer, Psychologica Belgica, 34:115-139, 1994) correlated highly with those of the present study. Therefore, the new norms are a valuable source of information for affective research in the Dutch language.},
author = {Moors, Agnes and {De Houwer}, Jan and Hermans, Dirk and Wanmaker, Sabine and van Schie, Kevin and {Van Harmelen}, Anne-Laura and {De Schryver}, Maarten and {De Winne}, Jeffrey and Brysbaert, Marc},
doi = {10.3758/s13428-012-0243-8},
issn = {1554-3528},
journal = {Behavior Research Methods},
month = {mar},
number = {1},
pages = {169--177},
title = {{Norms of valence, arousal, dominance, and age of acquisition for 4,300 Dutch words}},
url = {https://doi.org/10.3758/s13428-012-0243-8},
volume = {45},
year = {2013}
}

copied from https://github.com/bobvdvelde/economic_sentiment/blob/master/scripts_r2/DANEW.py
'''
import os
import csv
import logging
import re
import pandas
import numpy

class DANEW():
    """Class to generate Dutch Affective Norms for English Words list

    Based on the paper "Norms of valence, arousal, dominance, and age of acquisition for 4,300 Dutch words".

    """

    def __init__(self, lexicon_file_path, splitter = '\W'):
        """Load DANEW lexicon and propare text splitter
        """
        # pre-compile regex to split text
        self.splitter = re.compile(splitter)

        # load lexicon
        danew = pandas.read_csv(lexicon_file_path)

        # Center scores around 0
        centered_danew = danew
        centered_danew[danew.mean().index] = centered_danew[danew.mean().index] - danew.mean()
        centered_danew.index = centered_danew.Words
        self.lexicon = centered_danew.T

    #private method to check whether an object is iterable
    def is_iterable(self, thing):
        try:
            len([i for i in thing])
            return 1
        except:
            return 0



    def classify(self, text, group='All',fill_value=numpy.nan):
        """Calculate arousal, power and complexity metrics based the DANEW lexicon

        Parameters
        ----
        text : string
            The string (UTF-8) for which DANEW scores should be calculated
        group : string (default="All")
            A string indicating which DANEW sub-group should be used. Can include
            "Women", "Men" or "All".
        fill_value : numeric
            The value to use for words that do not feature in the DANEW lexicon.
            Defaults to NaN, which entails ignoring unknown words. Setting the
            fill_value to 0 implies that unknown words pull the mean sentiment
            closer to 0, reducing the sentiment scores for longer texts.

        Returns
        ----
        dict
            positive : int
                The number of words in the text with a positive arousal mean
            negate : int
                The number of words in the text with a negative arousal mean
            score : int
                The number of words with a positive arousal mean minus the number
                of negative arousal mean.
            subjectivity : float
                The number of non-zero words in the text found in DANEW, divided
                by the total number of words in the text.
            power : float
                The mean of mean power scores for each word in the text, with
                the fill_value used for unknown words.
            arousal : float
                The mean of mean arousal scores for each word in the text, with
                the fill_value used for unknown words.
            complexity : float
                The mean of mean power scores for each word in the text, with
                the fill_value used for unknown words.

        """
        if type(text)==str:
            tokens = self.splitter.split(text.lower())
        else:
            tokens = text

        if not self.is_iterable(text):
            return {
                    'positive':numpy.nan,
                    'negative': numpy.nan,
                    'score':numpy.nan,
                    'subjectivity':numpy.nan,
                    'power':numpy.nan,
                    'arousal':numpy.nan,
                    'complexity': numpy.nan
                    }

        scores = [self.lexicon.get(word)['{group}_mean_valence'.format(group=group)] for word in tokens if word and
                  not self.lexicon.get(word,pandas.DataFrame()).empty ] + [fill_value for word in tokens if
                   self.lexicon.get(word,pandas.DataFrame()).empty ]

        pos = sum([score for score in scores if score > 0 ] )
        neg = sum([score for score in scores if score < 0 ] )
        sub = (len(tokens) - len([score for score in scores if score !=0]))/ len(tokens)

        arousal    = numpy.nanmean([self.lexicon.get(word)['{group}_mean_arousal'.format(group=group)] for word in tokens if
                    not self.lexicon.get(word,pandas.DataFrame()).empty ] + [fill_value for word in tokens if
                    self.lexicon.get(word, pandas.DataFrame()).empty])

        power      = numpy.nanmean([self.lexicon.get(word)['{group}_mean_power'.format(group=group)] for word in tokens if word and
                    not self.lexicon.get(word,pandas.DataFrame()).empty ] + [fill_value for word in tokens if
                    self.lexicon.get(word, pandas.DataFrame()).empty])


        complexity = numpy.nanmean([self.lexicon.get(word)['{group}_mean_age_of_acquisition'.format(group=group)] for
                    word in tokens if word and
                    not self.lexicon.get(word,pandas.DataFrame()).empty ] + [fill_value for word in tokens if
                    self.lexicon.get(word, pandas.DataFrame()).empty])



        return {
                'positive':pos,
                'negative': neg,
                'score':(pos+neg)/len(tokens),
                'subjectivity':sub,
                'power':power,
                'arousal':arousal,
                'complexity': complexity
                }

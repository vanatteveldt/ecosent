"""
Sentiment lexicon for Dutch Economic News (SDEN) based on Kleinnijenhuis et al (2013).
Copied from https://github.com/bobvdvelde/economic_sentiment/blob/master/scripts_r2/boukinator.py
"""
import json
import re

class Boukinator():

    def __init__(self, dict_file):
        """Initialize functionality
        Defines regular expressions to match positive, negative and exceptions
        """
        dict = json.load(open(dict_file))

        # Convert query list to regular expressions for matching
        # define positive sentiment expressions
        self.posre = []
        for match in dict['positive']['list']:
            self.posre.append(re.compile("(\b?{word})".format(word=match).replace("*","(\B)?")))

        # define exceptions to positive sentiment expressions
        self.notpos = []
        for match in dict['positive']['except_when']:
            self.notpos.append(re.compile("(\b?{word})".format(word=match).replace("*","(\B)?")))

        # define negative sentiment expressions
        self.notneg = []
        for match in dict['negative']['except_when']:
            self.notneg.append(re.compile("(\b?{word})".format(word=match).replace("*","(\B)?")))

        # define exceptions to negative sentiment expressions
        self.negre = []
        for match in dict['negative']['list']:
            self.negre.append(re.compile("(\b?{word})".format(word=match).replace("*","(\B)?")))

        # define text splitter
        self.splitter = re.compile('\W')

    # private function to apply all expressions in a list to a word
    def _walk(self, t,re_list):
        n = 0
        for regex in re_list:
            if regex.search(t):
                n+=1
        return n

    def classify(self, text):
        """Sentiment classification method
        Parameters
        ----
        text : string
            A string of text (expected to be UTF-8) for which to classify
            sentiment
        Returns
        ----
        dict
            positive : the number (int) of positive expressions detected in the text
            negative : the number (int) of negative expressions detected in the text
            score    : the number (int) of positive minus negative expressions
                       detected in the text
            subjectivity : the number (int) of expressions of either kind detected
                           in the text
        """
        # lower and split the text using the splitter method
        t = self.splitter.split(text.lower())

        #
        pos = len([w for w in t if self._walk(w, self.posre) and not self._walk(w, self.notpos)])
        neg = len([w for w in t if self._walk(w, self.negre) and not self._walk(w, self.notneg)])
        sub = (len([w for w in t if w]) - (pos+neg)) / len(t)

        return {'postive':pos, 'negative':neg, 'score':pos-neg, 'subjectivity':sub}
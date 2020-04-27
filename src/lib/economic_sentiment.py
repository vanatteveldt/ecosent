# Reproduction code for Boukes et al, 2019
# adapted from https://github.com/bobvdvelde/economic_sentiment/blob/master/scripts_r2/analyze.py
import logging
from boukinator import Boukinator
from polyglot.text import Text
from pattern.nl import sentiment
from DANEW import DANEW

def add_sentiments(data, field='headline', boukinator_path=None, danew_path=None):
    """Add sentiments to data frame"""
    text = data[field]

    if boukinator_path:
        logging.info('adding Boukes et al')
        boukinator = Boukinator(boukinator_path)
        data['boukes'] = text.map(lambda t: boukinator.classify(t)['score'])

    logging.info('adding "recessie" classifier')
    # classify messages containing the word 'recessie' (EN: recession) as negative (-1)
    data['recessie'] = text.str.contains('recessie').map(float) * -1

    def polygloter(t):
        try:
            return Text(t, hint_language_code='NL').polarity
        except ZeroDivisionError:
            logging.warning("Polgyglot failed: Divide by zero")
            return 0
    logging.info('adding Polyglot')
    data['polyglot'] = text.map(polygloter)


    logging.info('adding Pattern')
    data['pattern'] = text.map(lambda t: sentiment(t)[0])

    if danew_path:
        logging.info('adding DANEW')
        danew = DANEW(danew_path)
        data['DANEW'] = text.map(lambda t: danew.classify(t)['score'])
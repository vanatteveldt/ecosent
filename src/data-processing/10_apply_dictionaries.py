#! /usr/bin/env python3
#DESCRIPTION: Reproduce dictionary scores from Boukes et al., 2019; see lib/economic_sentiment.py
#DEPENDS: data/raw/{gold_sentences.csv,dictionaries/{boukinator.json,DANEW.csv}}
#CREATES: data/intermediate/dictionary_output_quanteda.csv

"""
Calls the dictionaries on the gold data using the code copied/adapted from the bobvdvelde/economic_sentiment github.
See lib/economic_sentiment.py for more details
"""

from pathlib import Path
import pandas as pd
from economic_sentiment import add_sentiments

# Find path of ecosent data files
DATA = Path.cwd()/"data"

# read gold data and meta, only keep headlines from articles in gold
data = pd.read_csv(DATA/"raw"/"gold_sentences.csv")[["id", "headline"]]

add_sentiments(data, "headline",
               boukinator_path=DATA/"raw"/"dictionaries"/"boukinator.json",
               danew_path=DATA/"raw"/"dictionaries"/"DANEW.csv")


data = data.drop("headline", 1)
data = pd.melt(data, id_vars=["id"], var_name="variable", value_name="value")
data.insert(1, "method", "dictionary")
data.to_csv(DATA/"intermediate"/"dictionary_output.csv", index=False)

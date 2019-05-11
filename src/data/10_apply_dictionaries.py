# Calls the dictionaries on the gold data using the code from the bobvdvelde/economic_sentiment github. 
#
# To install:
# git clone git@github.com:vanatteveldt/economic-sentiment
# cd economic_sentiment
# python3 -m venv env
# source env/bin/activate
# pip install -r Requirements
# polyglot download sentiment2.nl

import sys
import os
import pandas as pd

# Find path of ecosent data files
base_path = os.path.dirname(sys.argv[0])
data_path = os.path.abspath(os.path.join(base_path, "..", "..", "data", "intermediate"))

# Find path of economic_sentiment installation
# This assumes the venv is within the repository, adapt as needed
run_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "..", ".."))
print("Running dictionaries from ", run_path, "; using data path ", data_path)

os.chdir(run_path)
sys.path.insert(0, run_path)

# read gold data and meta, only keep headlines from articles in gold 
gold = pd.read_csv(open(os.path.join(data_path, "gold.csv")))
ids = set(gold.id)

meta = pd.read_csv(open(os.path.join(data_path, "metadata.csv")))
meta = meta[meta.ID.isin(ids)][["ID", "headline"]]

# add sentiments and save
from scripts_r1.analyze import add_sentiments
add_sentiments(meta, "headline")

meta.to_csv(os.path.join(data_path, "dictionary_output.csv"))


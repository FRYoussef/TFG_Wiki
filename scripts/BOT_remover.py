"""
This script removes the BOT users in a corpus of Wiki articles
"""

#
# Authors: Ignacio Garcia Sanchez-Migallon
# Date: 24/05/2019
# Distributed under the terms of the GPLv3 license. 
#

import numpy as np
import pandas as pd

corpus = pd.read_csv('data/corpus/corpus.csv')


botless_corpus = pd.DataFrame(columns = corpus.columns)

for editor,i in zip(corpus['org:resource'], corpus.index):
    if 'bot' in editor.lower():
        corpus = corpus.drop(index = i)

corpus.to_csv(path_or_buf = 'data/corpus/botless_corpus.csv', index = False)


import numpy as np
import pandas as pd


corpus = pd.read_csv('data/corpus/editor_count.csv')

cluster = []

for row in corpus['n_edits']:

    if row == 1:
        cluster.append('1')
    elif row >= 2 and row < 5:
        cluster.append('[2-5)')
    elif row >= 5 and row < 10:
        cluster.append('[5-10)')
    elif row >= 10 and row < 20:
        cluster.append('[10-20)')
    elif row >= 20 and row < 50:
        cluster.append('[20-50)')
    elif row >= 50 and row < 100:
        cluster.append('[50-100)')
    elif row >= 100:
        cluster.append('+100')

corpus = corpus.drop('n_edits', axis = 1)
corpus['cluster'] = cluster

corpus.to_csv(path_or_buf = 'data/corpus/editor_count.csv', index = False)

print(corpus.head)
        

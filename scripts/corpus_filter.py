"""
This script filter a Wikipedia corpus of articles based on different parameters

This script supports the following command line parameters:

    -filter:#     The kind of filter to apply  (e.low/intermediate/high)
        -low:#     Select only the editors with less than 5 editions  
        -intermediate: Select only the editors that performed between 5 and 50 editions
        -high: Select only the editors with more than 50 editions

"""
#
# Authors: Ignacio Garcia Sanchez-Migallon
# Date: 24/05/2019
# Distributed under the terms of the GPLv3 license. 
#


import numpy as np
import pandas as pd
import sys
import os


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: unicode
    """
    opts = {}
    local_args = sys.argv[1:]
    for arg in local_args:
        option, sep, value = arg.partition(':')
        if option.startswith('-'):
            option = option[1:]
            if option == 'filter':
                opts[option] = value or input(
                    'Enter the filter type: ')
                continue
    filtro_corpus = corpus_filter(opts)
    filtro_corpus.filterApplier()

    return 0

def low_filter(self):

    for i in range(0,len(self.count)):
        if self.count[i] == '1' or self.count[i] == '[2-5)':
            self.editors_to_keep.append(self.editors[i])

    corpus = self.corpus.loc[self.corpus['resource'].isin(self.editors_to_keep)]
    
    corpus.to_csv(path_or_buf = 'data/corpus/low_editors.csv', index = False)

def intermediate_filter(self):
    
    for i in range(0,len(self.count)):
        if self.count[i] != '1' and self.count[i] != '[2-5)' and self.count[i] !='[50-100)' and self.count[i] !='+100':
            self.editors_to_keep.append(self.editors[i])

    corpus = self.corpus.loc[self.corpus['resource'].isin(self.editors_to_keep)]
    
    corpus.to_csv(path_or_buf = 'data/corpus/intermediate_editors.csv', index = False)
    
def best_filter(self):
    for i in range(0,len(self.count)):
        if self.count[i] != '1' and self.count[i] != '[2-5)' and self.count[i] != '[5-10)' and self.count[i] != '[10-20)' and self.count[i] !='[20-50)':
            self.editors_to_keep.append(self.editors[i])

    corpus = self.corpus.loc[self.corpus['resource'].isin(self.editors_to_keep)]
    
    corpus.to_csv(path_or_buf = 'data/corpus/best_editors.csv', index = False)

def casual_filter(self):

    for i in range(0,len(self.count)):
        if self.count[i] == '1' or self.count[i] == '[2-5)':
            self.editors_to_keep.append(self.editors[i])
    for j in range(0,len(self.corpus)):
        if self.corpus.iloc[j,6] in self.editors_to_keep:
            self.corpus.iloc[j,6] = 'Casual'
    
    self.corpus.to_csv(path_or_buf = 'data/corpus/corpus_casual.csv', index = False)

    
class corpus_filter():
    
    filtro = {'filter':''}

    corpus = pd.read_csv('data/corpus/corpus.csv')

    editor_count = pd.read_csv('data/corpus/editor_count.csv')

    count = editor_count['cluster'].values

    editors = editor_count['resource'].values

    editors_to_keep = []

    def __init__(self,params):

        self.filtro['filter'] = params['filter']

    def filterApplier(self):

        call =  self.filtro['filter']
        if call == 'low':
            low_filter(self)
        elif call == 'intermediate':
            intermediate_filter(self)
        elif call == 'high':
            best_filter(self)
        elif call == 'casual':
            casual_filter(self)
        else:
            print("Introduzca un filtro de entre [low, intermediate, best, casual]")
        
main()


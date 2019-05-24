"""
This script generate predictions of intentions behind each revision
based on the Wikipedia's diff results.

This script supports the following command line parameters:

    -file:#     The output of Wikipedia's diff  (e.g revision_ids_leche_featured)
    -base_file:#      The original article's name (e.g leche)

"""
#
# Authors: Ignacio Garcia Sanchez-Migallon
# Date: 24/05/2019
# Distributed under the terms of the GPLv3 license. 
#


import numpy as np
import pandas as pd
from sklearn.externals import joblib
import sys
import os


title = ''

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
            if option == 'file':
                opts[option] = value or input(
                    'Enter the file: ')
                continue
            if option == 'base_file':
                opts[option] = value or input(
                    'Enter the base file: ')
                continue
    predictions_process = predictions_generator(opts)
    predictions_process.generate_predictions()

    return 0

class predictions_generator():
    
    article = {'file':'','base_file':''}

    def __init__(self,params):

        self.article['file'] = params['file']
        self.article['base_file'] = params['base_file']
                   

    def generate_predictions(self):

        base_file_name = self.article['file']
        base_file = pd.read_csv(base_file_name, error_bad_lines=False)

        intentions = ['counter-vandalism','fact-update','refactoring','copy-editing','wikification',
              'vandalism','simplification','elaboration','verifiability','process','clarification','disambiguation',
              'point-of-view']
        
        #Load all the classifiers for each intention
        classifiers = {}
        for intention in intentions:
            model = joblib.load('trained_models/' + intention + '_classificator.plk')
            classifiers[intention] =  model
        
        #To store the predicted values of each intention
        results = {'revision_id':[],'counter-vandalism':[],'fact-update':[],'refactoring':[],'copy-editing':[],'wikification':[],
            'vandalism':[],'simplification':[],'elaboration':[],'verifiability':[],'process':[],'clarification':[],'disambiguation':[],
            'point-of-view':[]}
        
        #We add the revision_id to the results to know the revision of each
        results['revision_id'] = base_file.iloc[:,0]
        #Load the features as X to predict
        X = base_file.iloc[:, :-14]
        for intention in intentions:
    
            print("Predicting labels for " + intention)
            predictions_file = classifiers[intention].predict(X)
            for line in predictions_file:
                results[intention].append(line)
                
        print("Labels predicted")
        results_dataframe = pd.DataFrame.from_dict(results) 
        output = pd.read_csv(self.article['base_file'], sep=',')
        #create array of Nones to store the labels with the appropiate format (one single column for all intentions
        labels = [None] * len(results_dataframe.index)
    
        for intention in intentions:
    
            offset = 0
    
            for line in results[intention]:
    
                if labels[offset] == None:
                    labels[offset] = str(results['revision_id'][offset]) + ':'
                if line == 1:
                    labels[offset] = labels[offset] + intention + ','
        
                offset += 1

        labels_dataframe = pd.DataFrame(columns=['revision_id', 'intentionality'])
        for line in labels:

            data = line.split(':')
            data_id = data[0]
            data_intention = data[1].split(',')
            data_intention.remove('')
    
            data = pd.DataFrame({'revision_id':[data_id],'intentionality':[data_intention]})
            labels_dataframe = labels_dataframe.append(data)


        labels_dataframe['revision_id']=labels_dataframe['revision_id'].astype(int)
        output = output.merge(labels_dataframe, on = 'revision_id', how = 'inner')


        output.to_csv(path_or_buf = self.article['base_file'], index = False) 

main()

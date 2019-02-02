import numpy as np
import pandas as pd
import sys
import os

article = pd.read_csv('leche/leche.csv')

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
            if option == 'article':
                opts[option] = value or input(
                    'Enter the article: ')
                continue
    article_ids = revision_extractor(opts)
    article_ids.revision_id_extractor()

    return 0

class revision_extractor():
    
    article = {'article':''}

    def __init__(self,params):

        self.article['article'] = params['article']

    def revision_id_extractor(self):

        base_file_name = self.article['article'] + '/' + self.article['article'] + '.csv'
        base_file = pd.read_csv(base_file_name)

        output_file_name = 'revision_ids_' + self.article['article'] + '.csv'
        output_file = pd.DataFrame(columns = ['rev_id','labels'])

        for rev in base_file['revision_id']:
            
            output_file = output_file.append({'rev_id': rev, 'labels':0}, ignore_index=True)
            
        output_file.to_csv(path_or_buf = 'revision_ids_files/' + output_file_name, index = False)

        print('Revision ids file of ' + self.article['article'] + ' created')
        
        

    def dummy_labels_adder(filename):
        return 0        

os.mkdir('revision_ids_files')
main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script downloads wikipedia's dumps

This script supports the following command line parameters:

    -article:#     The article's name to download (e.g. Scene7)

    -list:#        The list of articles to download

    -storepath:#   The stored file's path (without extension, it´s going to store as .xml)

    -lang:#        The language of the wiki to use, default "es"

"""
#
# Authors: Youssef El Faqir El Rhazoui, Ignacio Garcia Sanchez-Migallon
# Date: 21/09/2018
# Distributed under the terms of the GPLv3 license.
#
# Based on: https://phabricator.wikimedia.org/diffusion/PWBC/browse/master/scripts/maintenance/download_dump.py 
#

from __future__ import absolute_import, division, unicode_literals
import xml.dom.minidom as minidom
import binascii
import os.path
import sys
import requests
import datetime
import shutil
from os import remove, symlink, urandom


try:
    from os import replace
except ImportError:   # py2
    if sys.platform == 'win32':
        import os

        def replace(src, dst):
            """Rename a file or directory, overwriting the destination."""
            try:
                os.rename(src, dst)
            except OSError:
                remove(dst)
                os.rename(src, dst)
    else:
        from os import rename as replace

class Dump_downloader():

    part = 1
    final_timestamp = 'undefined'
    curr_timestamp = 'first'
    total_size = 0
    url = ''
    availableOptions = {
    'wikiname': 'Wikipedia',
    'article': '',
    'list': '',
    'lang': 'es',
    'storepath': './',
    'download_limit': '$wgExportMaxHistory'
    }

    def __init__(self, params):

        
        self.availableOptions['article'] = params['article']
        if('storepath' in params):
            self.availableOptions['storepath'] = params['storepath'] + '/' + params['article']
        else:
            self.availableOptions['storepath'] += params['article']
        if('lang' in params):
            self.availableOptions['lang'] = params['lang']
        self.url = 'https://' + self.availableOptions['lang'] + '.wikipedia.org/w/index.php?title=Special:Export'

    def download_chunk(self, download_file, data_request):
        """
        It downloads maxHistory of revisions as a part of final file
        """

        #print('Downloading dump from ' + self.availableOptions['wikiname'])
        # download_file = '{article}_part{part}.xml'.format(
        #     article=self.availableOptions['article'],
        #     part=self.part)
        temp_file = download_file + '-' + \
            binascii.b2a_hex(urandom(8)).decode('ascii') + '.part'

        file_final_storepath = os.path.join(
            self.availableOptions['storepath'], download_file)
        file_current_storepath = os.path.join(
            self.availableOptions['storepath'], temp_file)

        # First iteration for atomic download with temporary file
        # Second iteration for fallback non-atomic download
        for non_atomic in range(2):
            try:
                print('Downloading file from: {}'.format(self.url))
                response = requests.post(self.url, data_request)
                if response.status_code == 200:
                    with open(file_current_storepath, 'wb') as result_file:
                        for data in response.iter_content(100 * 1024):
                            result_file.write(data)
                elif response.status_code == 404:
                    print(
                        'File with name "{article}", '
                        'and wiki "{wikiname}" ({url}) isn\'t '
                        'available'.format(
                            article=self.availableOptions['article'],
                            url=self.url,
                            wikiname=self.availableOptions['wikiname']))
                    return
                else:
                    return
                # Rename the temporary file to the target file
                # if the download completes successfully
                if not non_atomic:
                    replace(file_current_storepath, file_final_storepath)
                    break
            except (OSError, IOError):
                print('Error' + (OSError.strerror or IOError.strerror))

                try:
                    remove(file_current_storepath)
                except (OSError, IOError):
                    print('Error' + (OSError.strerror or IOError.strerror))

                # If the atomic download fails, try without a temporary file
                # If the non-atomic download also fails, exit the script
                if not non_atomic:
                    print('Cannot make temporary file, falling back to non-atomic download')
                    file_current_storepath = file_final_storepath
                else:
                    return False

        size = (sum(len(chunk) for chunk in response.iter_content(8196)))/1000000
        self.total_size += size
        print('\nDone! File stored as {}\nTotal: {}MB'.format(file_final_storepath, round(size, 3)))
        return

    def get_final_timestamp(self):
        """
        It gets the last article´s revision and updates the final timestamp
        """
        ret = 0
        data={'pages': self.availableOptions['article'], 'curonly': 'true',
              'action': 'submit'}
        file_name = '{}_temp.xml'.format(self.availableOptions['article'])
        self.download_chunk(file_name, data)

        # Now, we are going to find the revision´s timestamp.
        file_name = os.path.join(self.availableOptions['storepath'], file_name)
        doc = minidom.parse(file_name)
        if not doc.getElementsByTagName('timestamp').length:
            print('Timestamp not found')
            ret=1
        else:
            self.final_timestamp = timestamp_to_datetime(
                doc.getElementsByTagName('timestamp')[0].firstChild.nodeValue)
        remove(file_name)
        self.total_size = 0
        print('Removed the file {}'.format(file_name))
        return ret


    def join_chunks(self):
	    """
	    This method joins the different chunks of one article into one xml file
	    """
	    print('Joining chunks....')
	    file_name = os.path.join(self.availableOptions['storepath'], '{}.xml'.format(self.availableOptions['article']))
	    
	    with open(file_name,'w+', encoding='utf8') as file:
	        for i in range (1, self.part):
	            chunk_name = os.path.join(self.availableOptions['storepath'], '{0}_part{1}.xml'
	            	.format(self.availableOptions['article'], i))
	            with open(chunk_name,encoding='utf8', errors = 'ignore') as chunk_file:
	               content = chunk_file.read().splitlines()
	               if i != 1:
	                   content = content[44:]
	               for line in content:
	                    if i != self.part - 1:
	                        if( "</page>" not in line and "</mediawiki>" not in line):
	                            file.write(line + '\n')
	                    else:
	                        file.write(line + '\n')
	                        
	            os.remove(chunk_name)
	    
	    print('----------------------------------------------------------------------------------')
	    print('The article {} has been merged into one file'.format(self.availableOptions['article']))
	    print('----------------------------------------------------------------------------------')


    def run(self):
        """
        It manages article´s download joining the parts
        """
        if not os.path.exists(self.availableOptions['storepath']):
            os.makedirs(self.availableOptions['storepath'])

        if self.get_final_timestamp():
            print('The article \"{}\" isn´t available'.format(self.availableOptions['article']))
            return 1
        else:
            curr=''
            while curr == '' or self.final_timestamp > curr:
                file_name = '{art}_part{part}.xml'.format(art=self.availableOptions['article'], 
                            part=self.part)
                data={'pages': self.availableOptions['article'], 'offset': self.curr_timestamp, 
                      'limit': self.availableOptions['download_limit'], 'action': 'submit'}
                self.download_chunk(file_name, data)
                timestamps = minidom.parse(os.path.join(self.availableOptions['storepath'], 
                    file_name)).getElementsByTagName('timestamp')
                if not timestamps.length:
                    #No timestamps, you have to handle the error
                    return 1
                else:
                    curr = timestamp_to_datetime(timestamps[timestamps.length-1].firstChild.nodeValue) 
                    + datetime.timedelta(seconds=1)
                    self.curr_timestamp = '{0}-{1}-{2}T{3}:{4}:{5}Z'.format(curr.strftime('%Y'), 
                        curr.strftime('%m'), curr.strftime('%d'), curr.strftime('%H'), 
                        curr.strftime('%M'), curr.strftime('%S'))
                self.part += 1

            print('----------------------------------------------------------------------------------')
            print('The article \"{0}\" has been downloaded as {1} chunks in {2}'
                .format(self.availableOptions['article'], self.part, self.availableOptions['storepath']))
            print('Total downloaded: {}MB'.format(round(self.total_size), 3))
            print('----------------------------------------------------------------------------------')
            self.join_chunks()




def timestamp_to_datetime(timestamp):
    """ 
    It takes a ISO 8601 date from text and returns a object datetime
    """
    timestamp = timestamp.split('T')
    date = timestamp[0].split('-')
    time = timestamp[1].replace('Z', '').split(':')
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]), 0)



def dump_list(name):
    """
    This method process the file with the list of articles to download
    It reads the file splitting it in lines and stores each article name

    """
    
    with open(name) as file:
        content = file.read().splitlines()

    articleList = []

    for line in content:
        split = line.split('/')
        #Directions are "https://en.wikipedia.org/wiki/articleName hence the split[4] hardcoded.
        articleList.append(split[4])

    return articleList

def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: unicode
    """
    opts = {}
    unknown_args = []

    local_args = sys.argv[1:]
    for arg in local_args:
        option, sep, value = arg.partition(':')
        if option.startswith('-'):
            option = option[1:]
            if option == 'article':
                opts[option] = value or input(
                    'Enter the article: ')
                continue
            elif option == 'list':
                opts[option] = value or input(
                    'Enter the list of articles: ')
                continue
            elif option == 'storepath':
                opts[option] = os.path.abspath(value) or input(
                    'Enter the store path: ')
                continue
            elif option == 'lang':
                opts[option] = value or input(
                    'Enter the language of the wiki to use: ')
                continue

        unknown_args += [arg]

    missing = []
    if 'list' not in opts and 'article' not in opts:
        missing += ['-article']
        missing += ['-list']

    if missing or unknown_args:
        print('HELP: python script_path -article:article_name [-storepath:path]')
        print('HELP: It is also possible to use -list instead of -article for lists of articles')
        return 1
    
    if 'list' in opts:
        print('Processing list of links')
        if 'storepath' not in opts:
            folder = opts['list']
            folderName = folder.split('.')
            if os.path.exists(folderName[0]) :
               shutil.rmtree(folderName[0])
            os.mkdir(folderName[0])
            opts['storepath'] = folderName[0]
                              
        articleList = dump_list(opts['list'])
        for article in articleList:
            opts['article'] = article
            dump_down = Dump_downloader(opts)
            dump_down.run()
        return 2
    else:
        dump_down = Dump_downloader(opts)
        dump_down.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())

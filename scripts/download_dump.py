#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This script downloads wikipedia's dumps

This script supports the following command line parameters:

    -article:#     The article's name to download (e.g. Scene7)

    -storepath:#    The stored file's path (without extension, it´s going to store as .xml)

"""
#
# Authors: Youssef El Faqir El Rhazoui,
# Date: 21/09/2018
# Distributed under the terms of the GPLv3 license.
#
# Based on: https://phabricator.wikimedia.org/diffusion/PWBC/browse/master/scripts/maintenance/download_dump.py 
#

from __future__ import absolute_import, division, unicode_literals

import binascii

import os.path
import sys
import requests

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

    availableOptions = {
    'wikiname': 'Wikipedia',
    'article': '',
    'storepath': './',
    'download_offset': '1',
    'download_limit': '$wgExportMaxHistory'
    }

    def __init__(self, params):
        self.availableOptions['article'] = params['article']
        if('storepath' in params):
            self.availableOptions['storepath'] = params['storepath']


    def run(self):

        print('Downloading dump from ' + self.availableOptions['wikiname'])
        download_file = '{article}.xml'.format(
            article=self.availableOptions['article'])
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
                url = 'https://en.wikipedia.org/w/index.php?title=Special:Export'
                print('Downloading file from: ' + url)
                response = requests.post(url, data={'pages': self.availableOptions['article'], 
                    'offset': self.availableOptions['download_offset'], 
                    'limit': self.availableOptions['download_limit'], 'action': 'submit'})

                if response.status_code == 200:
                    with open(file_current_storepath, 'wb') as result_file:
                        print('')
                        for data in response.iter_content(100 * 1024):
                            result_file.write(data)
                        print('')

                elif response.status_code == 404:
                    print(
                        'File with name "{article}", '
                        'and wiki "{wikiname}" ({url}) isn\'t '
                        'available'.format(
                            article=self.availableOptions['article'],
                            url=url,
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
        print('Done! File stored as ' + file_final_storepath +
              '\nTotal: ' + str(size) + 'MB')
        return


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
            elif option == 'storepath':
                opts[option] = os.path.abspath(value) or input(
                    'Enter the store path: ')
                continue

        unknown_args += [arg]

    missing = []
    if 'article' not in opts:
        missing += ['-article']

    if missing or unknown_args:
        print('HELP: python script_path -article:article_name [-storepath:path]')
        return 1

    dump_down = Dump_downloader(opts)
    dump_down.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())

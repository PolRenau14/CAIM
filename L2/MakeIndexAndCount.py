import os
import argparse

"""
:Description: MakeIndexAndCount

    This script calls to IndexFilesPreprocess.py, and after that calls CountWords.py
    saving document in Output Path, and then clear terminal and show in terminal the
    output of CountWords.py

:Authors:
    pol

:Version:

:Date: 04/10/2019
"""


__author__ ='pol'

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--path',required=True, default=None, help='Path to the files')
    parser.add_argument('--index', required=True, default=None, help='Index for the files')
    parser.add_argument('--token', required=False,default='standard',choices=['standard','whitespace', 'classic', 'letter'],
                        help='Text tokenizer')

    parser.add_argument('--filter', required=False,default=['lowercase'], nargs=argparse.REMAINDER, help='Text tokenizer: lowercase, '
                                                                                          'asciifolding, stop, porter_stem, kstem, snowball')
    parser.add_argument('--output', required=True, default=None)

    args = parser.parse_args()

    path = args.path
    index = args.index

    token = args.token
    if len(args.filter):
        filter = ' '.join(args.filter)

    outputPath = args.output
    print(outputPath)

    added =""
    if token != None:

        added = " \\--token " + token + " --filter " + filter
    else:
        added = " \\--filter " + filter

    command = "python3 IndexFilesPreprocess.py --index "+index + " --path "+ path + added
    os.system(command)
    command = "python3 CountWords.py --index " + index +" > " + outputPath
    os.system(command)

    command= "cat " + outputPath
    os.system("clear")
    os.system(command)

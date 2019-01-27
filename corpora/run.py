#!/usr/bin/python3
"""
Front end for `algorithm.py`.
"""


from algorithm import Opts, collect_corpus

import getopt
import sys


def print_help_and_exit():
    print('Usage: ./run.sh [OPTIONS]'
         ,'\n' 'Option               GNU long option         Meaning'
         ,'\n' '-h                   --help                  Print this message and exit.'
         ,'\n' '-f <path>            --female-names=<path>   Text file with one female name per line (default ./female).'
         ,'\n' '-m <path>            --male-names=<path>     Text file with one male name per line (default ./male).'
         ,'\n' '-o <path>            --output=<path>         File name to write creted corpus (default ./corpus).'
         ,'\n' '-w <num>             --max-tweets=<num>      Retreave the last <num> tweets by every user (default 200, max 3200).'
         ,'\n'
         ,'\n' 'Filter Options'
         ,'\n' 'If NO options are specified, the following default is used: OPTIONS = -t10 -ekv'
         ,'\n' 'But if any opion is explicitly mentioned, the default is: everything off.'
         ,'\n' '-e                   --is-en                 Check if user profile language is English.'
         ,'\n' '-k                   --is-known              Discard users who we are unable to label.'
         ,'\n' '-t <num>             --min-tweets=<num>      Users with fewer tweets are discarded (default 10).'
         ,'\n' '-s                   --starts-with           Try to exclude people, posing as the opposite gender.'
         ,'\n' '-v                   --is-verified           Exclude users for who Twitter reports verified=false.'
         ,'')
    sys.exit()


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:]
                                  ,"hf:m:o:w:ekt:sv"
                                  ,["female-names=","male-names=", 'output=', 'max-tweets', 'is-en', 'is-known', 'min-tweets=', 'starts-with', 'is-verified'])
    except getopt.GetoptError:
        print_help_and_exit()

    temp = Opts(Opts.EMPTY)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help_and_exit()
        elif opt in ("-f", "--female-names"):
            temp.female_names = arg
        elif opt in ("-m", "--male_names"):
            temp.male_names = arg
        elif opt in ("-o", "--output"):
            temp.output = arg
        elif opt in ("-w", "--max-tweets"):
            temp.max_tweets = arg
        elif opt in ("-e", "--is-en"):
            temp.is_en = True
        elif opt in ("-k", "--is-known"):
            temp.is_known = True
        elif opt in ("-t", "--min-tweets"):
            temp.min_tweets = arg
        elif opt in ("-s", "--starts-with"):
            temp.starts_with = True
        elif opt in ("-v", "--is-verified"):
            temp.is_verified = True


    if temp == Opts(Opts.EMPTY):
        collect_corpus(Opts(Opts.DEFAULT))
    else:
       collect_corpus(temp)

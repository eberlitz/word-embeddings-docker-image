#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import bz2
import time
import glob
import argparse


def read(dirname):
    filepaths = glob.glob(dirname)
    filepaths.sort()
    for fp in filepaths:
        with bz2.BZ2File(fp, 'r') as input:
            for line in input:
                yield line.decode('utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="ptwiki-compressed-text-folder")
    parser.add_argument("-o", "--output", default="text.txt.bz2",
                        help="output file")
    args = parser.parse_args()
    wiki_text_dump_path = args.input + '/**/*.bz2'
    output_filename = args.output
    start_time = time.time()
    with open(output_filename, 'w', buffering=65536, encoding='utf-8') as output:
        for line in read(wiki_text_dump_path):
            output.write(line)
    elapsed_time = time.time() - start_time
    print('Time elapsed: {0}'.format(elapsed_time))

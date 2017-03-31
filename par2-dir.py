#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import sys

def parse_args():
    operations = ['create', 'c', 'verify', 'v', 'repair', 'r']

    parser = argparse.ArgumentParser(
        description='Par2 with directory and recursive scanning support.',
        epilog='See "man 3 par2" for flags supported by Par2.')

    parser.add_argument('op', choices=operations, action='store')
    parser.add_argument('--directory', '-d', help='directory to archive')
    parser.add_argument('--rename', help='Rename the checksum file using a given prefix', default='checksum')
    parser.add_argument('flags', nargs=argparse.REMAINDER)

    # Second level parser because the -d arg get eaten by the flags
    # positional arguments
    parser2 = argparse.ArgumentParser()
    parser2.add_argument('--directory', '-d', help='directory to archive')
    parser2.add_argument('--rename', help='Rename the checksum file using a given prefix', default='checksum')
    parser2.add_argument('flags', nargs=argparse.REMAINDER)

    # Merge.
    args = parser.parse_args()
    args2, unknown = parser2.parse_known_args(args.flags)
    args.flags = args2.flags + unknown
    args.directory = args2.directory
    args.rename = args2.rename

    return args


def main():
    args = parse_args()

    # If we don't specify a directory, then files should be specified
    # in the arguments already.
    files = []
    if args.directory:
        files = []
        for root, _, all_files in os.walk(args.directory):
            for f in all_files:
                if not f.endswith('.par2'):
                    files.append(os.path.join(root, f))

    cmd = ['par2', args.op] + args.flags
    if args.directory:
        print('Running: %s <files>' % ' '.join(cmd))
    else:
        print('Running: %s' % ' '.join(cmd))

    res = subprocess.call(cmd + files)
    if res:
        print('Error: return code=%d' % res)
        sys.exit(res)

    # Rename output files to make them more understandly refer to the
    # directory. By default par files will take the name of ones of the files.
    pattern = re.compile(r'^(.+?)(\.vol[0-9]+\+[0-9]+)?\.par2$')
    for item in os.listdir(args.directory):
        if os.path.isfile(item) and item.endswith('.par2'):
            m = re.match(pattern, item)
            if m:
                suffix = m.group(2) if m.group(2) else ''
                new_name = '%s%s.par2' % (args.rename, suffix)
                os.rename(item, new_name)

if __name__ == '__main__':
    main()

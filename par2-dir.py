#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

def parse_args():
    operations = ['create', 'c', 'verify', 'v', 'repair', 'r']

    parser = argparse.ArgumentParser(
        description='Par2 with directory and recursive scanning support.',
        epilog='See "man 3 par2" for flags supported by Par2.')

    parser.add_argument('op', choices=operations, action='store')
    parser.add_argument('--directory', '-d', help='directory to archive')
    parser.add_argument('flags', nargs=argparse.REMAINDER)

    # Second level parser because the -d arg get eaten by the flags
    # positional arguments
    parser2 = argparse.ArgumentParser()
    parser2.add_argument('--directory', '-d', help='directory to archive')
    parser2.add_argument('flags', nargs=argparse.REMAINDER)

    # Merge.
    args = parser.parse_args()
    args2 = parser2.parse_args(args.flags)
    args.flags = args2.flags
    args.directory = args2.directory

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

    cmd = ['par2', args.op] + args.flags + files
    print('Running: %s' % ' '.join(cmd))
    res = subprocess.call(cmd)
    sys.exit(res)


if __name__ == '__main__':
    main()

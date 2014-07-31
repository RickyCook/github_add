#!/usr/bin/env python
import argparse
import base64
import hashlib
import json

from os.path import expanduser, isfile
from urllib import quote
from urllib2 import urlopen

def fingerprint(line):
    key = base64.b64decode(line.strip().split()[1].encode('ascii'))
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))

parser = argparse.ArgumentParser(description="Add Github user keys to an authorized_keys file")
parser.add_argument('user', help="Github user to add keys for")
parser.add_argument('--file', help="file to add keys to (default: calculated. First checks ./.ssh/authorized_keys if it exists, then falls back to ~/.ssh/authorized_keys)")
args = parser.parse_args()

if args.file == None:
    if isfile('.ssh/authorized_keys'):
        args.file = '.ssh/authorized_keys'
    else:
        args.file = '%s/.ssh/authorized_keys' % expanduser('~')

print "Using file %s" % args.file

handle = urlopen('https://api.github.com/users/%s/keys' % quote(args.user))
data = json.load(handle)

with open(args.file, 'r') as fh:
    keys_set = set((line.strip() for line in fh))

with open(args.file, 'a') as fh:
    for key_obj in data:
        if key_obj['key'] not in keys_set:
            fh.write('# github user: %s\n' % args.user)
            fh.write('%s\n' % key_obj['key'])
            print "Added %s" % fingerprint(key_obj['key'])
        else:
            print "Ignoring duplicate %s" % fingerprint(key_obj['key'])

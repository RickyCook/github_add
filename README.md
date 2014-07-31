Github Add
==========
```
usage: github_add.py [-h] [--file FILE] user

Add Github user keys to an authorized_keys file

positional arguments:
  user         Github user to add keys for

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  file to add keys to (default: calculated. First checks
               ./.ssh/authorized_keys if it exists, then falls back to
               ~/.ssh/authorized_keys)
```

#!/usr/bin/env python

import argparse
from contextlib import closing
import sqlite3
import time
import re
import base64
import binascii


SPLIT_RE = '^(?P<userid>\d+?)\-\|\-(?P<username>.*?)\-\|\-(?P<email>.+?)\-\|\-(?P<hash>.*?)\-\|\-(?P<hint>.*)\|\-\-$'


def import_users(db_name, user_file):
    totaltime = time.time()

    split_re = re.compile(SPLIT_RE)

    insert_query = """
        INSERT INTO users (userid, username, email, hash, hint)
        VALUES (:userid, :username, :email, :hash, :hint)
    """

    with sqlite3.connect(db_name) as db_con:
        with closing(db_con.cursor()) as cur:
            with open(user_file, 'r') as users:
                cur_line = 0
                prev_line = None
                for line in users:
                    cur_line += 1
                    line = line.rstrip("\r\n")
                    row = None
                    match = split_re.match(line)
                    if match:
                        prev_line = None
                        row = match.groupdict()
                    else:
                        if line is not None and line != '':
                            print('invalid: %d:%s' % (cur_line, line))
                            if prev_line is not None:
                                line = prev_line + line
                                match = split_re.match(line)
                                if match:
                                    prev_line = None
                                    row = match.groupdict()
                                    print('fixed: %s' % line)
                                else:
                                    prev_line = line
                            else:
                                prev_line = line
                    if row is not None:
                        if row['username'] == '':
                            row['username'] = None
                        if row['hash']:
                            try:
                                row['hash'] = buffer(base64.b64decode(row['hash']))
                            except (binascii.Error, TypeError) as exc:
                                print('%s: %d:%s' % (exc, cur_line, line))
                                row['hash'] = None
                        else:
                            row['hash'] = None
                        cur.execute(insert_query, row)
                    if (cur_line % 100000) == 0:
                        print(cur_line)
    print('Lines imported: %d' % cur_line)
    print('Done in %.2f seconds' % (time.time() - totaltime))


def main():
    parser = argparse.ArgumentParser(description='Import user file')
    parser.add_argument('user_file')
    parser.add_argument('-d', '--database', help='database file', default='data/database.sqlite')
    args = parser.parse_args()
    import_users(args.database, args.user_file)


if __name__ == '__main__':
    main()

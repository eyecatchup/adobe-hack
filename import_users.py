#!/usr/bin/env python

import argparse
from contextlib import closing
import sqlite3
import time
import re
import base64
import binascii


def import_users(db_name, user_file):
    totaltime = time.time()

    split_re = re.compile('^(\d+?)\-\|\-(.*?)\-\|\-(.+?)\-\|\-(.*?)\-\|\-(.*)\|\-\-$')

    insert_query = """
        INSERT INTO users (userid, username, email, hash, hint)
        VALUES (?, ?, ?, ?, ?)
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
                        row = [v.strip() for v in match.groups()]
                    else:
                        if line is not None and line != '':
                            print('invalid: {}:{}'.format(cur_line, line))
                            if prev_line is not None:
                                line = prev_line + line
                                match = split_re.match(line)
                                if match:
                                    prev_line = None
                                    row = [v.strip() for v in match.groups()]
                                    print('fixed: {}'.format(line))
                                else:
                                    prev_line = line
                            else:
                                prev_line = line
                    if row is not None:
                        if row[1] == '':
                            row[1] = None
                        if row[3]:
                            try:
                                row[3] = buffer(base64.b64decode(row[3]))
                            except (binascii.Error, TypeError) as exc:
                                print('{}: {}:{}'.format(exc, cur_line, line))
                                row[3] = None
                        else:
                            row[3] = None
                        cur.execute(insert_query, row)
                    if (cur_line % 100000) == 0:
                        print(cur_line)
    print('Lines imported: {}'.format(cur_line))
    print('Done in {:.2f} seconds'.format(time.time() - totaltime))


def main():
    parser = argparse.ArgumentParser(description='Import user file')
    parser.add_argument('user_file')
    parser.add_argument('-d', '--database', help='database file', default='data/database.sqlite')
    args = parser.parse_args()
    import_users(args.database, args.user_file)


if __name__ == '__main__':
    main()

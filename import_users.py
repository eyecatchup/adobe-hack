#!/usr/bin/env python

import argparse
from contextlib import closing
import sqlite3
import time
import re


SPLIT_RE = '^(?P<uniqueid>.*)\-\|\-(?P<field_2>.*)\-\|\-(?P<email>.*)\-\|\-(?P<hash>.*)\-\|\-(?P<hint>.*)\|\-(?P<field_6>.*)\-$'


def import_users(db_name, user_file):
    totaltime = time.time()

    split_re = re.compile(SPLIT_RE)

    insert_query = """
        INSERT INTO users (uniqueid, field_2, email, hash, hint, field_6)
        VALUES (:uniqueid, :field_2, :email, :hash, :hint, :field_6)
    """

    db_con = sqlite3.connect(db_name)

    with db_con:
        with closing(db_con.cursor()) as cur:
            with open(user_file, 'r') as users:
                cur_line = 0
                for line in users:
                    cur_line += 1
                    line = line.strip()
                    match = split_re.match(line)
                    if match:
                        row = match.groupdict()
                        cur.execute(insert_query, row)
                        if (cur_line % 1000) == 0:
                            print(cur_line)
                    else:
                        print('invalid line: %d:"%s"' % (cur_line, line))
                if cur_line % 1000:
                    print(cur_line)

    print('> Done in %.2f seconds' % (time.time() - totaltime))


def main():
    parser = argparse.ArgumentParser(description='Import user file')
    parser.add_argument('user_file')
    parser.add_argument('-d', '--database', help='database file', default='data/database.sqlite')
    args = parser.parse_args()
    import_users(args.database, args.user_file)


if __name__ == '__main__':
    main()

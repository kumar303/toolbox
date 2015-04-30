#!/usr/bin/env python

import argparse
from cStringIO import StringIO
import csv
import re
from subprocess import check_call, check_output


def main():
    p = argparse.ArgumentParser(
        description='start a shell on a docker container')
    p.add_argument(
        'container', type=str,
        help='i.e. what you see in NAMES from `docker ps`')
    args = p.parse_args()

    container_id = None
    for row in docker_ps():
        if row['NAMES'] == args.container:
            container_id = row['CONTAINER ID']

    if not container_id:
        p.error('Could not find a running container named {n}'
                .format(n=args.container))

    check_call(['docker', 'exec', '-ti', container_id, 'bash'])


def docker_ps():
    """
    Iterate over each running docker process as a dictionary.

    Example of one dictionary record:

        {'CREATED ': 'About an hour ago',
         'IMAGE ': 'mozillamarketplace/solitude:latest',
         'PORTS ': '2602/tcp',
         'COMMAND ': '"supervisord -n -c /',
         'NAMES': 'paymentsenv_solitude_1',
         'CONTAINER ID': '55a158d344c6',
         'STATUS ': 'Up About an hour'}
    """
    info = check_output(['docker', 'ps']).splitlines()
    key = get_header_key(info.pop(0))

    space_map = sorted(key.keys())
    space_map.reverse()

    for chunk in info:
        row = {}
        # Walk the string backwards and slice out the values using the
        # header whitespace map.
        for offset in space_map:
            part = chunk[offset:]
            chunk = chunk[:offset]
            row[key[offset]] = part.strip()

        yield row


def get_header_key(header):
    """
    Map whitespace offsets for the `docker ps` header so the rest can be parsed
    """
    key = {}
    # This only supports headers like ONE or ONE TWO.
    # Any header with more than one space will cause it to fail.
    header_map = re.compile(r'([A-Z]+\s?[A-Z]*)(\s*)')

    offset = 0
    for name, space in header_map.findall(header):
        key[offset] = name
        offset += len(name) + len(space)

    return key


if __name__ == '__main__':
    main()

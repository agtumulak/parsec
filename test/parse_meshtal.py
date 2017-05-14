#!/usr/bin/env python
"""Test parsing of formatted output."""

from  __future__ import division, absolute_import, print_function, unicode_literals

from pprint import pprint
from src.parsec import parsec
import os
import re


def version_number(head, line):
    pattern = re.compile(r'version\s+(\d)')
    match = pattern.findall(line)
    if match:
        head.update({
            'version' : match[0]})


def extents(head, line):
    pattern = re.compile(r'(-?\d+\.\d+)\s+(-?\d+\.\d+)')
    match = pattern.findall(line)
    if match:
        head.update({
            'min' : match[0][0],
            'max' : match[0][1],})


def named(head, line):
    pattern = re.compile(r'\s+(?P<X>-?\d+\.\d+)'
                          '\s+(?P<Y>-?\d+\.\d+)'
                          '\s+(?P<Z>-?\d+\.\d+)'
                          '\s+(?P<Result>\d\.\d{5}E(?:\+|-)\d{2})'
                          '\s+(?P<RelError>\d\.\d{5}E(?:\+|-)\d{2})')
    match = pattern.search(line)
    if match:
        head.update(match.groupdict())


_format = {
        re.compile(r'^(mcnp\s+version)') : version_number,
        re.compile(r' Mesh Tally Number\s+(\d{1,8})') : {
            re.compile(r'^\s+(\w) direction') : extents,
            re.compile(r'^\s+(X\s+Y\s+Z\s+Result\s+Rel Error)') : named,
            },
        re.compile(r'made_up') : 's',
        }


if __name__ == '__main__':
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'meshtal')
    with open(test_file, 'rb') as inputfile:
        pprint(parsec(inputfile, _format))

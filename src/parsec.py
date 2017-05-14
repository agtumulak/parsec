#!/usr/bin/env python
"""A general purpose parser for formatted data output.""" 
from  __future__ import division, absolute_import, print_function, unicode_literals

import re


def traverse(tree, path):
    """Access node in tree specified by path."""
    for node in path:
        tree = tree[node]
    return tree


def search_down(line, pattern_tree, pattern_path, result_tree, result_path):
    """Check for matches that make the path deeper."""
    pattern_node = traverse(pattern_tree, pattern_path)
    if callable(pattern_node):
        pattern_node(traverse(result_tree, result_path), line)
        return True
    for pattern in pattern_node.keys():
        match = pattern.match(line)
        if match:
            pattern_path.append(pattern)
            while len(result_path) >= len(pattern_path):
                result_path.pop()
            result = match.groups()[0]
            traverse(result_tree, result_path).setdefault(result, dict())
            result_path.append(result)
            search_down(line, pattern_tree, pattern_path, result_tree, result_path)
            return True
    return False


def search(line, pattern_tree, pattern_path, result_tree, result_path):
    """Check for pattern matches in pattern_path."""
    node = (node for node in pattern_path[:])
    pattern_path[:] = [] # Start search at root
    while not search_down(line, pattern_tree, pattern_path, result_tree, result_path):
        try:
            pattern_path.append(node.next())
        except StopIteration:
            break


def parsec(formatted_file, pattern_tree):
    """Parse formatted_file according to pattern_tree and return result_tree."""
    pattern_path = []
    result_tree = {}
    result_path = []
    for line in formatted_file:
        search(line, pattern_tree, pattern_path, result_tree, result_path)
    return result_tree

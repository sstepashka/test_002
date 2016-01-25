#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

# from [a, b, c] to [1, elem, b, elem, c]
def join_collection(l, elem):
    result = []
    for e in l:
        result.append(e)
        result.append(elem)
    result.pop()

    return result

# split string to tokens by operations
# tokens include used operations
def tokenize_by_operation(expression, operation):
    tokens = expression.split(operation)

    return [x for x in join_collection(tokens, operation) if len(x) > 0]

# parse list of tokens by operations
def token_collection_by_operation(expressions, operation):
    colls =  [tokenize_by_operation(x, operation) for x in expressions]

    return list(itertools.chain(*colls))

# split string to token
# for example, 'A+B/C' tokenized to ['A', '+', 'B' + '/' + 'C']
# for tokenize user operations: +, -, *, /
def tokenize(expression):
    operations = ['+', '-', '*', '/']

    return reduce(lambda res, elem: token_collection_by_operation(res, elem), operations, [expression])
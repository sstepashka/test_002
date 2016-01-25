#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import StringIO


from tokenize import tokenize
from cycles import graph_find_cycles
from cells import *

# convert two dimensional array of 
# cells to named array cells like ('a1', 12), ('a2', 13) ...
def get_named_cells(cells):
    named_cells = []

    for i in xrange(0, len(cells)):
        for j in xrange(0, len(cells[i])):
            name = chr(ord('a') + j) + chr(ord('1') + i)
            cell = cells[i][j]

            named_cells.append((name, cell))

    return named_cells

def parse_cell(named_cell):
    name, cell = named_cell

    if cell.startswith('='):
        return (name, ExpressionCell(tokenize(cell[1:])))
    elif cell.startswith('\''): 
        return (name, StringCell(cell[1:]))
    elif cell.startswith("\"\""):
        return (name, EmptyCell())
    else:
        if cell.isdigit():
            return (name, ConstCell(cell))
        else:
            return (name, ErrorCell("#PARSE"))

def get_references(named_cell):
    name, cell = named_cell
    if isinstance(cell, ExpressionCell):
        return (name, [reference.lower() for reference in cell.get_references()])

    return (name, [])

def error_cell_if_in_cycle(named_cell, cycles):
    name, cell = named_cell

    if name in cycles:
        return (name, ErrorCell("#CYCLE"))

    return named_cell

def eval_expression(expression):
    try:
        return eval(''.join(expression))
    except:
        return "#EVAL"

def evaluate(cells):
    sheet = dict(cells)

    result = []

    for name, cell in cells:
        result.append(cell.eval(sheet))

    return result


def showCell(named_cell):
    name, cell = named_cell

    if isinstance(cell, ErrorCell):
        return cell.error
    elif isinstance(cell, ExpressionCell):
        return ''.join(cell.expression)
    elif isinstance(cell, ConstCell):
        return cell.value
    elif isinstance(cell, StringCell):
        return cell.string
    elif isinstance(cell, EmptyCell):
        return ""
    else:
        raise

def parseContentAndEvaluate(content_string):
    # input string to stream
    content = StringIO.StringIO(content_string)

    # get size from firsl line
    (height, width) = map(lambda value: int(value), content.readline().split())

    # get cells content with format [[ element ]]
    source_cells = map(lambda line: 
                                line.split(), 
                                content.readlines())

    # convert source cells to cells with name, 
    # like ('a1', <data>), ('a1', <data>), ..
    named_cells = get_named_cells(source_cells)


    #convert named cell to data with format: ('a1', <cell class>), ...
    parsed_cells = map(lambda cell: parse_cell(cell), named_cells)

    # find cycles in sheet
    # return set with nodes contains in all cycles
    cycles = graph_find_cycles(dict(map(lambda cell: get_references(cell), parsed_cells)))

    # replace cycled nodes for error cell with message $CYCLE
    replaced_cycles = map(lambda cell: error_cell_if_in_cycle(cell, cycles), parsed_cells)

    # print replaced_cycles
    eval_result = evaluate(replaced_cycles)

    for i in xrange(0, height):
        # print height
        # print len(eval_result)
        print '\t'.join(eval_result[i * width: (i + 1) * width])


def getInputData():
    return sys.stdin.read()

def main():
    content = getInputData()
    parseContentAndEvaluate(content)

if __name__ == '__main__':
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for large table should be replaced 
# to non-recursive version of algorithm
def findCycles(graph, begin, current, path = None, paths = None):
    if path is None:
        path = []
    
    if paths is None:
        paths = []

    path.append(current)

    current_node_refs = graph.get(current, [])

    for related in current_node_refs:
        if related == begin and len(path) >= 1:
            paths.append(list(path))
            
        if related not in path:
            paths = findCycles(graph, begin, related, path, paths)

    path.pop()        
    return paths

# unpack 2 dimensional list to 1 dimensional
def flatten(l):
    return [value for sublist in l for value in sublist]

# try find cycles for all nodes of graph
def graph_find_cycles(graph):
    nodes = set()
    for key in graph.keys():
        nodes.update(set(flatten(findCycles(graph, key, key))))

    return list(nodes)

# test code
def main():
    a = {
        '1': ['2', '4'],
        '2': ['3', '5'],
        '3': ['1'],
        '4': ['1'],
        '5': ['6'],
        '6': ['4']
        }

    print graph_find_cycles(a)

if __name__ == '__main__':
    main()
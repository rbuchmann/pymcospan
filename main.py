import pymc as pm
import networkx as nx

import matplotlib.pyplot as plt

def pushout(g, h, cospan_mapping):
    result = nx.union(g, h)
    for source, (param, target) in cospan_mapping.items():
        result.add_edge(source, target, param=param)
    return result

def construct(g):
    ordered_nodes = nx.topological_sort(g)
    constructed = {}
    random_vars = []
    for node in ordered_nodes:
        props = g.nodes[node]
        inputs = g.predecessors(node)
        params = {}
        for in_node in inputs:
            params[g.edges[(in_node, node)]['param']] = constructed[in_node]
        construction_fn = props['fn']
        constructed_node = construction_fn(**params)
        constructed[node] = constructed_node
        random_vars.append(constructed_node)
    return(random_vars)

def constant(name, value):
    return ('name', {'fn':  lambda : value})

def construct_test():
    g = nx.DiGraph()

    g.add_node('a', fn=lambda: 5)
    g.add_node('b', fn=lambda: 6)

    g.add_node('sum', fn=lambda a,b: a+b)

    g.add_edge('a','sum', param='a')
    g.add_edge('b', 'sum', param='b')

    print(construct(g))

def main():
    construct_test()

if __name__ == '__main__':
    main()

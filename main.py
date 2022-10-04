import pymc as pm
import networkx as nx

import matplotlib.pyplot as plt


# Example
# alpha = 1.0 / count_data.mean()  # Recall count_data is the
#                                # variable that holds our txt counts
# lambda_1 = pm.Exponential("lambda_1", alpha)
# lambda_2 = pm.Exponential("lambda_2", alpha)

# tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)

# @pm.deterministic
# def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
#     out = np.zeros(n_count_data)
#     out[:tau] = lambda_1  # lambda before tau is lambda1
#     out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
#     return out

# observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)

# model = pm.Model([observation, lambda_1, lambda_2, tau])

# mcmc = pm.MCMC(model)
# mcmc.sample(40000, 10000, 1)


def pushout(g, h, cospan_mapping):
    result = nx.union(g, h)
    for k, v in cospan_mapping.items():
        equivalent = list(v)
        while len(equivalent) > 1:
            result = nx.contracted_nodes(result, equivalent[0], equivalent[1])
            equivalent.pop(0)

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

def gtest():
    alpha = 0.5

    g1 = nx.DiGraph()

    g1.add_node('l1', kind='exponential')
    g1.add_node('l2', kind='exponential')

    g1.add_edge('l1', 'l2', param='alpha')

    g2 = nx.DiGraph()

    print(g1.in_edges('l2'))
    print(g1.nodes['l2'])

    g2.add_node('l3', kind='poisson')
    g2.add_node('l4', kind='poisson')

    g2.add_edge('l3', 'l4')

    inverse_mapping = {'a' : {'l2', 'l3'}}

    return pushout(g1, g2, inverse_mapping)

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

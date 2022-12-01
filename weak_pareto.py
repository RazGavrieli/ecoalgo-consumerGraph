import networkx as nx
import logging

def find_weak_pareto_improvment(
allocation: list[list[float]],
valuations: list[list[float]],
cycle: list
):
    print_io(allocation, valuations, cycle)
    print(allocation[0])
    consumerGraph = nx.Graph()
    A = []
    B = []
    for index, _agent in enumerate(allocation):
        consumerGraph.add_node(("agent", index), bipartite=1)
        A.append(("agent", index))
    for index, _itemAllocatedToPlayer in enumerate(allocation[0]):
        consumerGraph.add_node(("item", index), bipartite=0)
        B.append(("item", index))

    for indexOfAgent, allocationToAgent in enumerate(allocation):
        for indexOfIem, allocatonValue in enumerate(allocationToAgent):
            if allocatonValue > 0:
                consumerGraph.add_edge(("agent", indexOfAgent), ("item", indexOfIem))

    pos = nx.bipartite_layout(consumerGraph, A)
    print_graph(consumerGraph, pos)
    pass

def print_io(
allocation: list[list[float]],
valuations: list[list[float]],
cycle: list
):
    for i in allocation:
        for j in i:
            print(j, end=" ")
        print()
    print()
    for i in valuations:
        for j in i:
            print(j, end=" ")
        print()
    print()
    for i in cycle:
        print(i)

def print_graph(g1, pos):
    import matplotlib.pyplot as plt
    nx.draw_networkx(g1, pos= pos)
    plt.show()

if __name__ == "__main__":
    allocations = [
    [0, 1, 0.2],
    [1, 0, 0.25] , 
    [0, 0, 0.55]
     ]
    valuations = [
    [20, 50, 30],
    [50, 18, 32],
    [15,15,70]
    ]
    cycle = [0,11,1, 12, 0]
    find_weak_pareto_improvment(allocation=allocations, valuations=valuations, cycle=cycle)
    pass
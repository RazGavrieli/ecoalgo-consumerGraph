import networkx as nx
import logging
e = 0.01
def find_weak_pareto_improvment(allocation: list[list[float]],valuations: list[list[float]],cycle: list):
    print_io(allocation, valuations, cycle)
    A, B, consumerGraph = create_consumerGraph(allocation)

    changeGraph = create_changeGraph(allocation, valuations, A)

    pos = nx.bipartite_layout(consumerGraph, A)
    print_graph(consumerGraph, pos)
    pos = nx.circular_layout(changeGraph)
    print_graph(changeGraph, pos, weight=True)
    prodOfFirstCircle = 1
    prodOfSecondCircle = 1
    for index in range(0,len(cycle)-2, 2):
        key = "agent"
        prodOfFirstCircle *= valuations[cycle[index]][cycle[index+1]]/valuations[cycle[index+2]][cycle[index+1]]
        prodOfSecondCircle *= valuations[cycle[len(cycle)-1-index]][cycle[len(cycle)-2-index]]/valuations[cycle[len(cycle)-3-index]][cycle[len(cycle)-2-index]]

    newAllocations = allocation
    if prodOfFirstCircle == 1 and prodOfSecondCircle == 1:
        print("can have weak pareto improvment as both prods are 1")
    elif prodOfFirstCircle < 1:
        flag = True
        while flag:
            rollingProd = 1
            for index in range(0, len(cycle)-2, 2):
                agentA = cycle[index]
                agentB = cycle[index+2]
                currItem = cycle[index+1]

                currR = valuations[agentA][currItem]/valuations[agentB][currItem]
                newAllocations[agentA][currItem] -= e/rollingProd
                if newAllocations[agentA][currItem] < 0:
                    jump = newAllocations[agentA][currItem]*(-1)
                    newAllocations[agentB][currItem] += jump
                    newAllocations[agentA][currItem] = 0
                    flag = False
                    break
                newAllocations[agentB][currItem] += e/rollingProd
                rollingProd *= currR
    elif prodOfSecondCircle < 1:
        flag = True
        while flag:
            rollingProd = 1
            for index in range(len(cycle)-1, 0, -2):
                agentA = cycle[index]
                agentB = cycle[index-2]
                currItem = cycle[index-1]

                currR = valuations[agentA][currItem]/valuations[agentB][currItem]
                newAllocations[agentA][currItem] -= e/rollingProd
                if newAllocations[agentA][currItem] < 0:
                    jump = newAllocations[agentA][currItem]*(-1)
                    newAllocations[agentB][currItem] += jump
                    newAllocations[agentA][currItem] = 0
                    flag = False
                    break
                newAllocations[agentB][currItem] += e/rollingProd
                rollingProd *= currR

    A, _, improvedConsumerGraph = create_consumerGraph(newAllocations)
    pos = nx.bipartite_layout(improvedConsumerGraph, A)
    
    print_io(newAllocations)
    print(improvedConsumerGraph.number_of_edges(), consumerGraph.number_of_edges())
    print_graph(improvedConsumerGraph, pos)
    
    # changeGraph = create_changeGraph(newAllocations, valuations, A)
    # pos = nx.circular_layout(changeGraph)
    # print_graph(changeGraph, pos, weight=True)
    return newAllocations
    



    

def print_io(
allocation: list[list[float]] = None,
valuations: list[list[float]] = None,
cycle: list = None
):
    for i in allocation:
        for j in i:
            print(j, end=" ")
        print()
    print()
    # for i in valuations:
    #     for j in i:
    #         print(j, end=" ")
    #     print()
    print(cycle)

def print_graph(g , pos=None, weight=False):
    import matplotlib.pyplot as plt
    if pos == None:
        pos = nx.random_layout(g)
    nx.draw_networkx(g, pos=pos)
    if weight:
        edge_labels = nx.get_edge_attributes(g, "weight")
        nx.draw_networkx_edge_labels(g, pos=pos,edge_labels=edge_labels, label_pos=0.2)
    plt.show()

def create_consumerGraph(allocation: list[list[float]]):
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
    return A, B, consumerGraph

def create_changeGraph(allocation: list[list[float]],valuations: list[list[float]], A: list):
    changeGraph = nx.DiGraph()
    for i in A:
        changeGraph.add_node(i) 
               
    for _i, i in A:
        for _j, j in A:
            if i==j:
                continue
            r = []
            iValues = valuations[i]
            jValues = valuations[j]
            for index in range(len(valuations[0])):
                if allocation[i][index] == 0:
                    continue
                r.append(iValues[index]/jValues[index])
            weightOfNewEdge = min(r)
            changeGraph.add_edge((_i,i), (_j,j), weight=("{:.3f}".format(weightOfNewEdge),str(r.index(weightOfNewEdge))))

    return changeGraph

if __name__ == "__main__":
    # allocations = [
    # [0, 1, 0.2, 0.25],
    # [1, 0, 0.25, 0.25], 
    # [0, 0, 0.55, 0.5]
    # ]
    # valuations = [
    # [20, 50, 20, 10],
    # [50, 18, 22, 10],
    # [15,15,55, 15]
    # ]
    # cycle = [0, 2, 1, 3, 2, 2, 0]
    allocations = [
    [0.9, 0.1, 0],
    [0.05, 0.9, 0.1] , 
    [0.05, 0, 0.9]
     ]
    valuations = [
    [3, 1, 6],
    [6, 3, 1],
    [1, 6, 3]
    ]
    cycle = [0, 0, 1, 2, 2, 0, 0]
    newAllo = find_weak_pareto_improvment(allocation=allocations, valuations=valuations, cycle=cycle)
    for i in range(len(newAllo[0])):
        sum = 0
        for j in range(len(newAllo)):
            sum += newAllo[j][i]
        if sum > 1.1 or sum < 0.99:
            print(i, j, sum, "bad")
    pass